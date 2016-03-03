# dj-21v

shop
====
shop/models.py
--------------
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

cart/cart.py
--------------
```
from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

```

cart/forms.py
-------------
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

urls.py
-------
```
urlpatterns += [
    url(r'^$', view_home.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^users/', include('userprofiles.urls', namespace="users")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^shop/', include('shop.urls', namespace='shop')),

    url(r'^admin/', admin.site.urls),
]

```
shopt/urls.py
-------------
```
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.product_list, name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
]

```
shopt/views.py
-------------
```
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

```
cart/urls.py
------------
```
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]

```

cart/views.py
-------------
```
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'shop/cart/detail.html', {'cart': cart})

```
cart/processors/context_processors.py
-------------------------------------
```
from ..cart import Cart

def cart(request):
    return {'cart': Cart(request) }

```
settings.py
-----------
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.processors.context_processors.cart',
            ],
        },
    },
]

```
Система шаблонов
================

Django использует высокоуровневый API, который не привязан к конкретному бэкенду:

- Для каждого бэкенда DjangoTemplates из настройки the TEMPLATES, Django создает экземпляр Engine. DjangoTemplates оборачивает Engine, чтобы адаптировать его под API конкретного бэкенда шаблонов.
- Модуль django.template.loader предоставляет функции, такие как get_template(), для загрузки шаблонов. Они возвращают django.template.backends.django.Template, который оборачивает django.template.Template.
- Template, полученный на предыдущем шаге, содержит метод render(), который оборачивает контекст и запрос в Context и делегирует рендеринг основному объекту Template.

Настройка бэкенда
------------------

При создании Engine все аргументы должны передаваться как именованные:

- dirs – это список каталого, в которых бэкенд ищет файлы шаблонов. Используется для настройки filesystem.Loader. По умолчанию равен пустому списку.
- app_dirs влияет только на значение loaders по умолчанию. По умолчанию False.
- context_processors – список путей Python для импорта функций, которые используются для наполнения контекста шаблонов, если он рендерится с объектом запроса. Эти функции принимают объект запроса и возвращают dict значений, которые будут добавлены в контекст. По умолчанию равен пустому списку.
- debug – булево значение, которое включает и выключает режим отладки. При True шаблонизатор сохраняет дополнительную отладочную информацию, которая может использоваться для отображения информации ошибки, которая возникла во время рендеринга. По умолчанию False.
- loaders – список загрузчиков шаблонов, указанных строками. Каждый класс Loader знает как загрузить шаблоны из определенного источника. Вместо строки можно указать кортеж. Первым элементом должен быть путь к классу Loader, вторым – параметры, которые будут переданы в Loader при инициализации.
По умолчанию содержит список:
```
'django.template.loaders.filesystem.Loader'
'django.template.loaders.app_directories.Loader', только если app_dirs равен True.
```
- string_if_invalid значение, которые шаблонизатор выведет вместо неправильной переменной(например, с опечаткой в назчании). По умолчанию – пустая строка.
- file_charset – кодировка, которая используется при чтении файла шаблона с диска. По умолчанию 'utf-8'.

Процессоры контекста
====================
список процессоров контекста по умолчанию:
------------------------------------------
1. django.contrib.auth.context_processors.auth
Если включить этот процессор, в RequestContext будут добавлены следующие переменные:
- user – объект auth.User текущего авторизованного пользователя или объект AnonymousUser, если пользователь не авторизованный).
- perms – объект django.contrib.auth.context_processors.PermWrapper, которые содержит права доступа текущего пользователя.

2. django.template.context_processors.debug
Если включить этот процессор, в RequestContext будут добавлены следующие переменные, но только при DEBUG равном True и, если IP адрес запроса (request.META['REMOTE_ADDR']) указан в INTERNAL_IPS:
- debug – True. Вы можете использовать эту переменную, чтобы определить DEBUG режим в шаблоне.
- sql_queries – список словарей {'sql': ..., 'time': ...}, который содержит все SQL запросы и время их выполнения, которые были выполнены при обработке запроса. Список отсортирован в порядке выполнения SQL запроса.

3. django.template.context_processors.i18n
Если включить этот процессор, в RequestContext будут добавлены следующие переменные:
- LANGUAGES – значение настройки LANGUAGES.
- LANGUAGE_CODE – request.LANGUAGE_CODE, если существует. Иначе значение LANGUAGE_CODE.

4. django.template.context_processors.media
Если включить этот процессор, в RequestContext будет добавлена переменная MEDIA_URL, которая содержит значение MEDIA_URL.

5. django.template.context_processors.static
Если включить этот процессор, в RequestContext будет добавлена переменная STATIC_URL, которая содержит значение STATIC_URL.

6. django.template.context_processors.csrf
Этот процессор добавляет токен, который используется тегом csrf_token для защиты от CSRF атак.

7. django.template.context_processors.request
Если включить этот процессор, в RequestContext будет добавлена переменная request, содержащая текущий HttpRequest.

8. django.contrib.messages.context_processors.messages
Если включить этот процессор, в RequestContext будут добавлены следующие переменные:
- messages – список сообщений (строки), которые были добавлены с помощью фреймворка сообщений.
- DEFAULT_MESSAGE_LEVELS – словарь приоритетов сообщений и их числовых кодов.

Как создать свой процессор контекста
------------------------------------
Интерфейс процессора контекста - это функция Python, которая принимает один аргумент, объект HttpRequest, и возвращает словарь, которая будет добавлен в контекст шаблона. Процессор контекста обязательно должен возвращать словарь.

Код процессора может находится где угодно. Главное не забыть указать его в опции 'context_processors' настройки:setting:TEMPLATES, или передать аргументом context_processors в Engine.


Orders
======
orders/models.py
---------------
```
from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

```
orders/admin.py
--------------
```
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    
admin.site.register(Order, OrderAdmin)

```
orders/views.py
--------------
```
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch task
            order_created(order.id)
            return render(request, 'shop/orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/orders/create.html', {'cart': cart,
                                                        'form': form})
```
orders/forms.py
---------------
```
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

```
orders/tasks.py
---------------
```
from django.core.mail import send_mail
from .models import Order

def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                             order.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent

```

shop/orders/create.html
-----------------------
```
{% extends "shop/base.html" %}

{% block title %}
    Checkout
{% endblock %}

{% block content %}
    <h1>Checkout</h1>
    
    <div class="order-info">
        <h3>Your order</h3>
        <ul>
            {% for item in cart %}
                <li>{{ item.quantity }}x {{ item.product.name }} <span>${{ item.total_price }}</span></li>
            {% endfor %}
        </ul>
        <p>Total: ${{ cart.get_total_price }}</p>
    </div>
    
    <form action="." method="post" class="order-form">
        {{ form.as_p }}
        <p><input type="submit" value="Place order"></p>
        {% csrf_token %}
    </form>
{% endblock %}

```
shop/orders/created.html
------------------------
```
{% extends "shop/base.html" %}

{% block title %}
    Thank you
{% endblock %}

{% block content %}
    <h1>Thank you</h1>
    <p>Your order has been successfully completed. Your order number is <strong>{{ order.id }}</strong>.</p>
{% endblock %}

```
orders/urls.py
-------------
```
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
]

```
urls.py
--------
```
urlpatterns += [
    url(r'^$', view_home.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^users/', include('userprofiles.urls', namespace="users")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^orders/', include('orders.urls', namespace='orders')),

    url(r'^admin/', admin.site.urls),
]
```

shop/product/detail.html
------------------------
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
        <a href="{% url "orders:order_create" %}" class="button">Checkout</a>
    </p>
{% endblock %}

```

Отправка электронных писем
===========================
Код находится в модуле django.core.mail.

Пример
```
from django.core.mail import send_mail

send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['to@example.com'], fail_silently=False)
```
Письмо отправлено через SMTP хост и порт, которые указаны в настройках EMAIL_HOST и EMAIL_PORT. Настройки EMAIL_HOST_USER и EMAIL_HOST_PASSWORD, если указаны, используются для авторизации на SMTP сервере, а настройки EMAIL_USE_TLS и EMAIL_USE_SSL указывают использовать ли безопасное соединение.

При отправке письма через django.core.mail будет использоваться кодировка из DEFAULT_CHARSET.
send_mail()
```
send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
```
Самый простой способ отправить письмо – использовать django.core.mail.send_mail().

Параметры subject, message, from_email и recipient_list являются обязательными.
-------------------------------------------------------------------------------
1. subject: строка.
2. message: строка.
3. from_email: строка.
4. recipient_list: список строк, каждая является email. Каждый получатель из recipient_list будет видеть остальных получателей в поле “To:” письма.
5. fail_silently: булево. При False send_mail вызовет smtplib.SMTPException. 
6. auth_user: необязательное имя пользователя, которое используется при авторизации на SMTP сервере. Если не указано, Django будет использовать значение EMAIL_HOST_USER.
7. auth_password: необязательный пароль, который используется при авторизации на SMTP сервере. Если не указано, Django будет использовать значение EMAIL_HOST_PASSWORD.
8. connection: необязательный бэкенд, который будет использоваться для отправки письма. Если не указан, будет использоваться бэкенд по умолчанию. 
9. html_message: если html_message указано, письмо будет с multipart/alternative, и будет содержать message с типом text/plain, и html_message с типом text/html.

Возвращает количество успешно отправленных писем (которое будет 0 или 1, т.к. функция отправляет только одно письмо).

Пример
------
Отправляет одно письмо john@example.com и jane@example.com, они оба указаны в “To:”:
```
send_mail('Subject', 'Message.', 'from@example.com',
    ['john@example.com', 'jane@example.com'])
```

Бэкенды для отправки электронной почты
---------------------------------------
Непосредственная отправка электронного письма происходит в бэкенде.

Django предоставляет несколько бэкендов. Эти бэкенды, кроме SMTP (который используется по умолчанию), полезны только при разработке или тестировании. Вы можете создать собственный бэкенд.

SMTP бэкенд
===========

Это бэкенд по умолчанию. Почта отправляется через SMTP сервер. Адрес сервера и параметры авторизации указаны в настройках EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, EMAIL_USE_SSL, EMAIL_TIMEOUT, EMAIL_SSL_CERTFILE и EMAIL_SSL_KEYFILE.

SMTP бэкенд используется в Django по умолчанию. Если вы хотите указать его явно, добавьте в настройки:
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
Dummy бэкенд
------------
Этот бэкенд ничего не делает с почтой. Чтобы указать этот бэкенд, добавьте следующее в настройки:
```
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
```
Этот бэкенд не следует использовать на боевом сервере, он создавался для разработки.

Настройка почты при разработке
==============================

Самый простой способ настроить почту для разработки – использовать бэкенд console. Этот бэкенд перенаправляет всю почту в stdout, позволяя увидеть содержимое писем.

Также можно использовать file. Этот бэкенд сохраняет содержимое каждого SMTP-соединения в файл.

Еще один способ – использовать локальный SMTP-сервер, который принимает письма и выводит их в консоль, но никуда их не оправляет. Python позволяет создать такой сервер одной командой:
```
python -m smtpd -n -c DebuggingServer localhost:1025
```
Эта команда запускает простой SMTP-сервер, который слушает 1025 порт на localhost. Этот сервер выводит заголовки и содержимое полученных писем в консоль. Вам необходимо указать в настройках EMAIL_HOST и EMAIL_PORT. Подробности об этом SMTP-сервер смотрите в документации Python к модулю smtpd.

settings.py
-----------
```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'janusnic@gmail.com'
EMAIL_PORT = 1025

```
Пароли приложений Gmail
=======================
https://support.google.com/accounts/
Если вы пользуетесь двухэтапной аутентификацией, то специальные пароли понадобятся вам для входа в некоторые приложения (например, Outlook или почтовый клиент на iPhone/Mac). Вам не нужно запоминать эти пароли – наша система сгенерирует их автоматически. Подробнее...

Откройте настройки аккаунта Google на своем устройстве и введите шестнадцатизначный пароль, указанный выше.
Этот пароль открывает приложению или устройству доступ к вашему аккаунту Google (как и обычный пароль). Его не нужно запоминать. Также просим вас не записывать его и никому не показывать.


Create an Application specific password
---------------------------------------
- Visit your Google Account security page.
- In the 2-Step Verification box, click Settings(if there is no settings link, you may want to create a new one. you can skip step 3 & 4).
- Click the tab for App-specific passwords.
- Click Manage your application specific passwords.
- Under the Application-specific passwords section, enter a descriptive name for the application you want to authorize, such as "Django gmail" then click Generate application-specific password button.
- note down the password. for example: smbumqjiurmqrywn 

Then add the appropriate values to settings.py:
------------------------------------------------
```
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your-username@gmail.com'
EMAIL_HOST_PASSWORD = 'Application spectific password(for eg: smbumqjiurmqrywn)'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```
You can use the shell to test it:
```
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'This is a test', 'your@email.com', ['toemail@email.com'],
     fail_silently=False)
```