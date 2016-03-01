from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Category, Product
from django.shortcuts import get_object_or_404
from cart.forms import CartAddProductForm

class ShopMixin(object):
    """Adds categories and current order to render context"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        # data['order'] = get_order(self.request)
        return context


class ProductList(ShopMixin, ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def __init__(self, *args, **kwargs):
        self.category = None
        super().__init__(*args, **kwargs)
    
    def get_category(self):
        category_slug = self.kwargs.get('category_slug')
        category = None
        if category_slug:
            category = get_object_or_404(
                Category,
                slug=category_slug,
            )
            self.category = category
        return category

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.category:
            self.get_category()
        if self.category:
            queryset = queryset.filter(
                category=self.category,
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
                
        context['category'] =  self.get_category()
        return context

class ProductDetail(ShopMixin, DetailView):
    
    model = Product
    form_class = CartAddProductForm
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'
