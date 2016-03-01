# dj-21v

shop
====

```
./manage.py startapp shop
```

Application definition
-----------------------
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',

    'ckeditor',
    'ckeditor_uploader',
    'blog',
    'userprofiles',
    'shop',
]
```
models.py
```
from django.db import models
from django.core.urlresolvers import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

```
makemigrations
--------------
```
./manage.py makemigrations shop
./manage.py migrate
Operations to perform:
  Apply all migrations: contenttypes, userprofiles, auth, admin, blog, sessions, shop
Running migrations:
  Rendering model states... DONE
  Applying shop.0001_initial... OK

```
admin.py
--------
```
from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)

```

Функционал Class Based Views
============================
1. get_context_data - формирует данные для вывода в шаблон;
2. get_queryset - отправляет запрос в базу;
3. get_template_name - определяет шаблон.

ListView
=========
- служит для вывода списка моделей;
- поддерживает разбитие на страницы (pagination).

DetailView
===========
- служит для вывода одной модели.

Список товаров 1
----------------

views.py
--------
```
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Category, Product

class ProductList(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    
    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.filter(available=True)
        return context

```

shop/product/list.html
----------------------
```
{% extends "shop/base.html" %}
{% load static %}

{% block title %}
    {% if category %}{{ category.name }}{% else %}Products{% endif %}
{% endblock %}

{% block content %}
    <div id="sidebar">
        <h3>Categories</h3>
        <ul>
            <li {% if not category %}class="selected"{% endif %}>
                <a href="{% url "shop:product_list" %}">All</a>
            </li>
        {% for c in categories %}
            <li {% if category.slug == c.slug %}class="selected"{% endif %}>
                <a href="{{ c.get_absolute_url }}">{{ c.name }}</a>
            </li>
        {% endfor %}
        </ul>
    </div>
    <div id="main" class="product-list">
        <h1>{% if category %}{{ category.name }}{% else %}Products{% endif %}</h1>
        {% for product in products %}
            <div class="item">
                
                    <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                
               {{ product.name }}<br>
                ${{ product.price }}
            </div>
        {% endfor %}
    </div>
{% endblock %}
```

mysite/urls.py
--------------
```
urlpatterns += [
    url(r'^$', view_home.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^shop/', include('shop.urls', namespace="shop")),
    url(r'^users/', include('userprofiles.urls', namespace="users")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^admin/', admin.site.urls),
]

```

shop/urls.py
------------
```
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ProductList.as_view(), name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList.as_view(), name='product_list_by_category'),

]

```
При́месь (mix in)
================
При́месь (mix in) — элемент языка программирования (обычно класс или модуль), реализующий какое-либо чётко выделенное поведение. Используется для уточнения поведения других классов, не предназначен для порождения самостоятельно используемых объектов. В объектно-ориентированных языках программирования является способом реализации классов, отличным от широко используемых принципов, пришедших из языка программирования Simula. Механизм впервые реализован в Flavors. Преимуществом примесей является то, что повышая повторную используемость текстов программ, этот метод избегает многих проблем множественного наследования. Однако при этом метод накладывает свои ограничения.
При́месь Python
==============
Принцип ООП - наследование - дочерний класс наследует от родительского все свойства и методы. Python позволяют делать наследование от нескольких родительских классов. Тогда в дочернем классе как бы смешиваются (mix) родительские. 

Принцип микс-инов - базовый родительский класс всегда один, а остальные должны быть всего лишь примесями (mixin). Отличительная особенность микс-ина в том, что он должен быть как можно проще, чтобы затрагивать только необходимый минимум функциональности, иначе он может повредить логику базового класса.

В случае стандартного наследования можно применить ParentClass.method_name(self, **kwargs).

Встроенный метод super().
-------------------------
Он позволяет определить родителя в иерархии микс-инов:
```
def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
```
иерархия в случае микс-инов считается слева направо. Наибольший приоритет у самого класса, дальше у самого левого миксина, и в конце справа базовый класс.

микс-ин в class-based views.
----------------------------
На микс-инах выстроен весь модуль django.views.generic. Например, базовым классом для всех CBV является класс View. Он обеспечивает только методы as_view() и dispatch(). Если его смешать с TemplateMixin, то мы получим дополнительно свойство template_name и метод get_template_names(). Потом примешав к ним FormMixin, можно получить класс FormView, который обладает свойствами не только представления в целом и представления с шаблонами, но и представления с формами. А если примешать FormMixin к DetailView, то мы получим основу для CreateView и UpdateView.

Основная цель микс-инов — найти функционал, который пересекается между разнородными представлениями, и объединить его. Тогда, чтобы добавить этот функционал, достаточно будет примешать нужный микс-ин к необходимому классу.

Добавляем в контекст параметр categories, который будет содержать все категории нашего shop:
```
class ShopMixin(object):
    """Adds categories to render context"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context
```
get_context_data(**kwargs)
--------------------------
Возвращает данные контекста для отображения списка объектов.

Встроенная реализация этого метода требует чтобы атрибут object был установлен в представлении(пускай даже в None). 

И дальше этот микс-ин начинает работать в остальных классах:
------------------------------------------------------------
```
class ProductList(ShopMixin, ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

```
Контекст
--------
Часто бывает необходимо изменить имя переменной, под которой наш объект (или список объектов) доступен в шаблоне. Метод, отвечающий за данную функциональность носит имя get_context_object_name. Данный метод принимает в качестве аргумента объект (или список объектов). В случае с отдельным объектом имя переменной в шаблоне по умолчанию будет именем самого объекта. В случае со списком объектов это будет имя объекта с суффиксом _list. Например для объекта Post иимена переменных будут post и post_list для отдельного объекта и списка объектов соответственно. Мы можем явно указать имя переменной, если присвоим ее значение атрибуту context_object_name.
context_object_name
-------------------
object: объект, отображаемый данным представлением. Если указан атрибут context_object_name, то эта переменная будет также добавлена в контекст, с тем же значением, что и у object.

Список товаров views.py
------------------------
```
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Category, Product
from django.shortcuts import get_object_or_404

class ShopMixin(object):
    """Adds categories and current order to render context"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
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

```
class ProductDetail(ShopMixin, DetailView)
==========================================
views.py
---------
```
class ProductDetail(ShopMixin, DetailView):
    
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'
```
urls.py
-------
```
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.ProductList.as_view(), name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.ProductList.as_view(), name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.ProductDetail.as_view(), name='product_detail'),
]

```
shop/product/list.html
-----------------------
```
{% extends "shop/base.html" %}
{% load static %}

{% block title %}
    {% if category %}{{ category.name }}{% else %}Products{% endif %}
{% endblock %}

{% block content %}
    <div id="sidebar">
        <h3>Categories</h3>
        <ul>
            <li {% if not category %}class="selected"{% endif %}>
                <a href="{% url "shop:product_list" %}">All</a>
            </li>
        {% for c in categories %}
            <li {% if category.slug == c.slug %}class="selected"{% endif %}>
                <a href="{{ c.get_absolute_url }}">{{ c.name }}</a>
            </li>
        {% endfor %}
        </ul>
    </div>
    <div id="main" class="product-list">
        <h1>{% if category %}{{ category.name }}{% else %}Products{% endif %}</h1>
        {% for product in products %}
            <div class="item">
                <a href="{{ product.get_absolute_url }}">
                    <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                </a>
                <a href="{{ product.get_absolute_url }}">{{ product.name }}</a><br>
                ${{ product.price }}
            </div>
        {% endfor %}
    </div>
{% endblock %}
```
shop/product/detail.html
------------------------
```
{% extends "shop/base.html" %}
{% load static %}

{% block title %}
    {{ product.name }}
{% endblock %}

{% block content %}
    <div class="product-detail">
        <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
        <h1>{{ product.name }}</h1>
        <h2><a href="{{ product.category.get_absolute_url }}">{{ product.category }}</a></h2>
        <p class="price">${{ product.price }}</p>
        
        {{ product.description|linebreaks }}
    </div>
{% endblock %}

```
cart
====
```
./manage.py startapp cart
```

forms.py
--------
```
from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

```
settings.py
------------
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',

    'ckeditor',
    'ckeditor_uploader',
    'blog',
    'userprofiles',
    'shop',
    'cart',
]

```
shop/views.py
-------------
```
from cart.forms import CartAddProductForm

class ProductDetail(ShopMixin, DetailView):
    model = Product
    form_class = CartAddProductForm
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

```

templates/shop/product/detail.html
----------------------------------
```
{% block content %}
    <div class="product-detail">
        <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
        <h1>{{ product.name }}</h1>
        <h2><a href="{{ product.category.get_absolute_url }}">{{ product.category }}</a></h2>
        <p class="price">${{ product.price }}</p>
        <form  method="post">
            {{ form }}
            {% csrf_token %}
            <input type="submit" value="Add to cart">
        </form>
        
        {{ product.description|linebreaks }}
    </div>
{% endblock %}
```

cart:cart_add
-------------
```
{% block content %}
    <div class="product-detail">
        <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
        <h1>{{ product.name }}</h1>
        <h2><a href="{{ product.category.get_absolute_url }}">{{ product.category }}</a></h2>
        <p class="price">${{ product.price }}</p>
        <form action="{% url "cart:cart_add" product.id %}" method="post">
            {{ form }}
            {% csrf_token %}
            <input type="submit" value="Add to cart">
        </form>
        
        {{ product.description|linebreaks }}
    </div>
{% endblock %}
```

cart/urls.py
------------
```
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    
]

```

mysite/urls.py
--------------
```
urlpatterns += [
    url(r'^$', view_home.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^shop/', include('shop.urls', namespace="shop")),
    url(r'^cart/', include('cart.urls', namespace="cart")),
    url(r'^users/', include('userprofiles.urls', namespace="users")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^admin/', admin.site.urls),
]

```
cart/views.py
-------------
```
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

```
templates/cart/detail.html
--------------------------
```
{% extends "shop/base.html" %}
{% load static %}

{% block title %}
    Your shopping cart
{% endblock %}

{% block content %}
    <h1>Your shopping cart</h1>
    <table class="cart">
        <thead>
            <tr>
                <th>Image</th>
                <th>Product</th>
                <th>Quantity</th>
                <th>Remove</th>
                <th>Unit price</th>                
                <th>Price</th>
            </tr>
        </thead>
        <tbody>
        {% for item in cart %}
            {% with product=item.product %}
            <tr>
                <td>
                    <a href="{{ product.get_absolute_url }}">
                        <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                    </a>
                </td>
                <td>{{ product.name }}</td>
                <td>
                    <form action="{% url "cart:cart_add" product.id %}" method="post">
                        {{ item.update_quantity_form.quantity }}
                        {{ item.update_quantity_form.update }}
                        <input type="submit" value="Update">
                        {% csrf_token %}
                    </form>
                </td>
                <td><a href="{% url "cart:cart_remove" product.id %}">Remove</a></td>
                <td class="num">${{ item.price }}</td>
                <td class="num">${{ item.total_price }}</td>
            </tr>
            {% endwith %}
        {% endfor %}
        <tr class="total">
            <td>Total</td>
            <td colspan="4"></td>
            <td class="num">${{ cart.get_total_price }}</td>
        </tr>
        </tbody>
    </table>
    <p class="text-right">
        <a href="{% url "shop:product_list" %}" class="button light">Continue shopping</a>
    </p>
{% endblock %}

```