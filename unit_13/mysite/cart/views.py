from django.shortcuts import render, redirect, get_object_or_404

from shop.models import Product

from .forms import CartAddProductForm

def cart_add(request, product_id):
    
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request)
    
    quantity=form['quantity']
    update_quantity=form['update']
    return redirect('cart:cart_detail')

def cart_detail(request):
    
    cart={}
    return render(request, 'cart/detail.html', {'cart': cart})
