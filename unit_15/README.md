# dj-21v

coupon models
=============
 ./manage.py startapp coupons

models.py
---------
```
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50,
                            unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code

```


# Application definition
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
    'orders',
    'coupons',

]

./manage.py makemigrations coupons
```

coupons/admin.py
----------------
```
from django.contrib import admin
from .models import Coupon

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']

admin.site.register(Coupon, CouponAdmin)
```
coupons/forms.py
----------------
```
from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField()
```

coupons/views.py:
-----------------
```
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                    valid_from__lte=now,
                                    valid_to__gte=now,
                                    active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')

```

urls.py
-------
```
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^apply/$', views.coupon_apply, name='apply'),
]

```

main urls.py:
-------------
```
urlpatterns += [
    url(r'^$', view_home.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^users/', include('userprofiles.urls', namespace="users")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^coupons/', include('coupons.urls', namespace='coupons')),
    url(r'^shop/', include('shop.urls', namespace='shop')),

    url(r'^admin/', admin.site.urls),
]

```

cart.py:
--------

```
from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

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
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id') # we try to get the coupon_id session key from the current session and store its value in the Cart object. 


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

    # If the cart contains a coupon_id function, the Coupon object with the given id is returned.
    
    @property 
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # If the cart contains a coupon , we retrieve its discount rate and return the amount to be deducted from the total amount of the cart.
    
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    # We return the total amount of the cart after deducting the amount returned by the get_discount() method.

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()

```

cart/views.py:
--------------
```
from coupons.forms import CouponApplyForm

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    coupon_apply_form = CouponApplyForm()

    return render(request, 'cart/detail.html', {'cart': cart,
                                                'coupon_apply_form': coupon_apply_form,
                                                })
```

shop/cart/detail.html:
----------------------
```
        <tr class="total">
            <td>Total</td>
            <td colspan="4"></td>
            <td class="num">${{ cart.get_total_price }}</td>
        </tr>
```
заменим на:
```
        {% if cart.coupon %}
            <tr class="subtotal">
                <td>Subtotal</td>
                <td colspan="4"></td>
                <td class="num">${{ cart.get_total_price }}</td>
            </tr>
            <tr>
                
                    <td>
                    "{{ cart.coupon.code }}" coupon
                    ({{ cart.coupon.discount }}% off)

                    </td>
                
                <td colspan="4"></td>
                <td class="num neg">- ${{ cart.get_discount|floatformat:"2" }}</td>
            </tr>
        {% endif %}
        <tr class="total">
            <td>Total</td>
            <td colspan="4"></td>
            <td class="num">${{ cart.get_total_price_after_discount|floatformat:"2" }}</td>
        </tr>
```


Добавим:

```
    <p>Apply a coupon:</p>
    <form action="{% url "coupons:apply" %}" method="post">
        {{ coupon_apply_form }}
        <input type="submit" value="Apply">
        {% csrf_token %}
    </form>

```

shop/orders/create.html template:
----------------------------------
```
<ul>
    {% for item in cart %}
    <li>
        {{ item.quantity }}x {{ item.product.name }}
        <span>${{ item.total_price }}</span>
    </li>
    {% endfor %}
</ul>
```

заменим на:

```
        <ul>
            {% for item in cart %}
                <li>{{ item.quantity }}x {{ item.product.name }} <span>${{ item.total_price }}</span></li>
            {% endfor %}
            {% if cart.coupon %}
                <li>
                    "{{ cart.coupon.code }}" ({{ cart.coupon.discount }}% off)
                    <span>- ${{ cart.get_discount|floatformat:"2" }}</span>
                </li>
            {% endif %}
        </ul>
```

строку:

```
<p>Total: ${{ cart.get_total_price }}</p>
```

заменим на:
```
<p>Total: ${{ cart.get_total_price_after_discount|floatformat:"2" }}</p>
```

orders/models.py:
-----------------
```
from decimal import Decimal
from django.db import models
from shop.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon

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
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])
```

migration
---------
```
python manage.py makemigrations

python manage.py migrate orders
```

orders/models.py - get_total_cost():
------------------------------------
```
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))
```

orders/viewa.py
---------------
order = form.save()

Replace it with the following ones:

```
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
```

save() method 
-------------

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

            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
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

Интернационализация и локализация
=================================
https://docs.djangoproject.com/en/1.8/ref/settings/#globalization-i18n-l10n.

Целью интернационализации и локализации является обеспечение возможности отдельному веб приложению предоставлять свой контент на языке и в формате, понятном целевой аудитории.

Django обеспечивает две вещи:

- Он позволяет разработчикам и авторам шаблонов указывать какие именно части их приложений должны быть переведены или отформатированы под используемые языки и традиции.

- Он использует эти метки для локализации веб приложений под конкретного пользователя, учитывая его настройки.

Интернационализация
-------------------
Подготовка программного обеспечения для локализации. Обычно выполняется разработчиками.

Локализация
-----------
Создание переводов и локальных форматов. Обычно выполняется переводчиками.

Перевод и форматирование контролируются параметрами USE_I18N and USE_L10N соответственно. Тем не менее, оба функционала участвуют в интернационализации и локализации.

locale name
-----------
Имя локали, либо спецификация языка в виде ll или комбинация языка и спецификации страны в виде ll_CC. Примеры: it, de_AT, es, pt_BR. Языковая часть всегда указывается в нижнем регистре, а часть, определяющая страну, – в верхнем регистре. Разделителем является символ подчёркивания.

language code
-------------
Представляет имя языка. Используя этот формат, браузеры отправляют имена языков, контент на которых они предпочитают принять, в HTTP заголовке Accept-Language. Примеры: it, de-at, es, pt-br. Обе части (язык и страна) указываются в нижнем регистре, но HTTP заголовок Accept-Language регистронезависимый. Разделителем является символ тире.

```
LANGUAGE_CODE = 'en'
```

ISO Language Code Table
-----------------------
http://www.lingoes.net/en/translator/langcode.htm
```
uk  Ukrainian
uk-UA   Ukrainian (Ukraine)
```
LANGUAGE_CODE setting:
----------------------
```
LANGUAGES = (
('en', 'English'),
('uk', 'Ukrainian'),
)
```

message file
------------
Файл сообщения является обычным текстовым файлом, представляющим единственный язык, который содержит все доступные строки перевода и правила их отображения для данного языка. Файлы сообщений имеют расширение .po.

translation string
-------------------
Строка, которая может быть переведена.

format file
-----------
Файл формата является модулем языка Python и определяет форматы данных для данной локали.

Django предоставляет утилиты для извлечения переводимых строк в файл сообщений. Этот файл является удобным средством, которое позволяет переводчикам делать свою работу. После того, как перевод строк этого файла завершён, файл должен быть скомпилирован. Этот процесс обеспечивает набор средств GNU gettext.

При наличии скомпилированного ресурса с переводом строк, Django обеспечивает автоматический перевод веб приложений для каждого доступного языка, в соответствии с языковыми настройками пользователя.

Механизм интернационализации Django включен по умолчанию, т.е. в определённых местах фреймворка всегда присутствует небольшая трата ресурсов на его работу. Если вы не используете интернационализацию, то вам следует потратить пару секунд на установку USE_I18N = False в файле конфигурации. Это позволит Django выполнять некоторую оптимизацию, не подгружая библиотеки интернационализации.

Есть также независимый, но связанный параметр USE_L10N, который управляет применением локального форматирования для данных.

Удостоверьтесь, что вы активировали механизм перевода для вашего проекта, для этого достаточно проверить наличие django.middleware.locale.LocaleMiddleware в параметре конфигурации MIDDLEWARE_CLASSES. 

```
MIDDLEWARE_CLASSES = (
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.locale.LocaleMiddleware',
'django.middleware.common.CommonMiddleware',
# ...
)
```
Как Django находит переводы
----------------------------
Во время своей работы Django создаёт в памяти унифицированный каталог с переводами. Для этого он использует следующий алгоритм, учитывая порядок нахождения путей для загрузки файлов сообщений (.mo) и приоритет множества перевода для одного слова:

Каталоги, указанные в LOCALE_PATHS, имеют повышенный приоритет, список представлен по убыванию приоритета.

```
LOCALE_PATHS = (
os.path.join(BASE_DIR, 'locale/'),
)
```

Затем происходит поиск каталога locale в каждом установленном приложении, указанном в INSTALLED_APPS. Тут тоже приоритет идёт по убыванию.

Наконец, используется базовый перевод Django из django/conf/locale.

Поиск переводов для JavaScript строк происходит аналогично, но с небольшими отличиями. 
Имя каталога, содержащего перевод, должно быть названо в соответствии соглашению по наименованию локалей. Т.е. en, uk и так далее.

```
locale/
       en/
       uk/
```


Интернационализация в коде
==========================
Обычный перевод
---------------
Укажите переводимую строку с помощью функции ugettext(). Удобно импортировать её с помощью краткого псевдонима, _ (символ подчеркивания), чтобы сократить затраты на ввод.

Модуль gettext стандартной библиотеки языка Python определяет _() в качестве псевдонима для gettext() в глобальном пространстве имён.

Символ подчёркивания (_) используется в интерактивном интерпретаторе Python и в доктестах в качестве “результата предыдущей операции”. Определение глобальной функции _() приведёт к путанице. Явное импортирование ugettext() в виде _() решает эту проблему.

```
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'uk' # uk-UA   Ukrainian

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

from django.utils.translation import gettext_lazy as _

# uk-UA   Ukrainian

LANGUAGES = (
    ('en', _('English')),
    ('uk', _('Ukrainian')),
)

```

orders/models.py:
-----------------
```
from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    first_name = models.CharField(_('first name'),
                                  max_length=50)
    last_name = models.CharField(_('last name'),
                                 max_length=50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'),
                               max_length=250)
    postal_code = models.CharField(_('postal code'),
                                   max_length=20)
    city = models.CharField(_('city'),
                            max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))


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

Ленивый перевод
---------------
Используйте ленивые версии функций перевода из django.utils.translation (их легко опознать по суффиксу lazy в их именах) для отложенного перевода строк – перевод производится во время обращения к строке, а не когда вызывается функция.

Эти функции хранят ленивую ссылку на строку, не на её перевод. Сам перевод будет выполнен во время использования строки в строковом контексте, например, во время обработки шаблона.

Это полезно, когда функция перевода вызывается при загрузке модуля.

Такое может легко произойти во время определения моделей, форм или модельных форм, так как в Django их поля реализованы в виде атрибутов класса. По этой причине, надо использовать ленивый перевод в следующих случаях:

- Поля модели и связанные с ними значения атрибутов verbose_name и help_text
Например, для перевода подсказки для поля first name в модели:

```
from django.utils.translation import ugettext_lazy as _

class Order(models.Model):
    first_name = models.CharField(_('first name'),
                                  max_length=50, help_text=_('This is the help text'))
    last_name = models.CharField(_('last name'),
                                 max_length=50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'),
                               max_length=250)
    postal_code = models.CharField(_('postal code'),
                                   max_length=20)
    city = models.CharField(_('city'),
                            max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

```

Вы можете перевести имена связей ForeignKey, ManyToManyField или OneToOneField с помощью их атрибута verbose_name:

```
from django.utils.translation import ugettext_lazy as _

class Order(models.Model):
    first_name = models.CharField(_('first name'),
                                  max_length=50, help_text=_('This is the help text'))
    last_name = models.CharField(_('last name'),
                                 max_length=50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'),
                               max_length=250)
    postal_code = models.CharField(_('postal code'),
                                   max_length=20)
    city = models.CharField(_('city'),
                            max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               verbose_name=_('order')
                               null=True,
                               blank=True)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

```

Значения для подписи модели
---------------------------
Рекомендуется всегда предоставлять явные значения для verbose_name и verbose_name_plural, а не надеяться на механизм их автоматического определения через имя класса:

```
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Order(models.Model):
    first_name = models.CharField(_('first name'),
                                  max_length=50, help_text=_('This is the help text'))
    last_name = models.CharField(_('last name'),
                                 max_length=50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'),
                               max_length=250)
    postal_code = models.CharField(_('postal code'),
                                   max_length=20)
    city = models.CharField(_('city'),
                            max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               verbose_name=_('order')
                               null=True,
                               blank=True)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-created',)
```

Значения атрибута short_description у методов модели

Для методов модели вы можете с помощью атрибута short_description предоставить перевод для Django и интерфейса администратора:
```
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Order(models.Model):
    first_name = models.CharField(_('first name'),
                                  max_length=50, help_text=_('This is the help text'))
    last_name = models.CharField(_('last name'),
                                 max_length=50)
    email = models.EmailField(_('e-mail'))
    address = models.CharField(_('address'),
                               max_length=250)
    postal_code = models.CharField(_('postal code'),
                                   max_length=20)
    city = models.CharField(_('city'),
                            max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               verbose_name=_('order')
                               null=True,
                               blank=True)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('-created',)
    
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))
    get_total_cost.short_description = _('It is a total cost')

```

Локализация: как создать языковые файлы
========================================
После того, как текстовые ресурсы приложения были помечены для перевода, следует выполнить (или получить) сам перевод.

Файлы сообщений
----------------
Первым шагом будет создание файла сообщений для нового языка. Файл сообщений является простым текстовым файлом, предоставляющим один язык, который содержит все переводимые строки и правила их представления на этом языке. Файлы сообщений имеют расширение .po.

Django поставляется с утилитой, django-admin makemessages, которая автоматизирует создание и обновление этих файлов.

Утилиты Gettext
---------------
Команда makemessages использует команды из утилит набора GNU gettext: xgettext, msgfmt, msgmerge и msguniq.

Для создания или обновления файла сообщений запустите эту команду:
```
django-admin makemessages -l uk
```
где uk является названием локали для создаваемого файла сообщений. 

Этот скрипт должен быть запущен из одного из двух мест:

- Корневой каталог вашего Django проекта (который содержит manage.py)
- Корневой каталог одного из приложений Django.

Скрипт просматривает дерево исходного кода вашего проекта или приложения и извлекает все строки, помеченные для перевода(смотрите Как Django находит переводы и убедитесь что LOCALE_PATHS настроен правильно). Затем скрипт создаёт (или обновляет) файл сообщений в каталоге locale/LANG/LC_MESSAGES. В случае примера с uk, файл будет создан в locale/uk/LC_MESSAGES/django.po.

При запуске makemessages из корневого каталога вашего проекта, извлечённые строки будут автоматически размещены в соответствующих файлах сообщений. Таким образом, строка, полученная из файла приложения, которое обладает каталогом locale, будет размещена в файле сообщений в этом каталоге. А строка, полученная из файла приложения, у которого нет каталога locale, будет размещена в файле сообщений в каталоге, который первым упомянут в LOCALE_PATHS или будет выведена ошибка если LOCALE_PATHS пуст.

По умолчанию, django-admin makemessages просматривает каждый файл с расширениями .html или .txt. Если вам надо изменить это поведение, используйте опцию --extension или -e для указания нужного расширения для просматриваемых файлов:
```
django-admin makemessages -l uk -e txt
```
Разделяйте множество расширений с помощью запятой и/или используйте опцию многократно:
```
django-admin makemessages -l uk -e html,txt -e xml
```

Если у вас не установлены утилиты gettext, тогда makemessages создаст пустые файлы. Если вы столкнулись с такой проблемой, тогда либо установите утилиты gettext, либо скопируйте файл сообщений для английского языка (locale/en/LC_MESSAGES/django.po), если он доступен, и используйте его как стартовую точку; это просто пустой файл переводов.

Формат .po файлов несложен. Каждый .po файл содержит небольшой заголовок, например, контактную информацию ответственного. Но основная часть файла является списком сообщений – простое сопоставление переводимых строк с переводами на конкретный язык.

.po файлы: Кодировка и использование BOM
----------------------------------------
Django поддерживает .po файлы только в кодировке UTF-8 и без меток BOM (Byte Order Mark). Если ваш редактор по умолчанию добавляет такие метки в начало файла, вам следует изменить это поведение.

gettext на Windows
==================

- Скачайте следующие архивы с серверов GNOME https://download.gnome.org/binaries/win32/dependencies/
```
gettext-runtime-X.zip
gettext-tools-X.zip
```
X является версией, мы требуем версию 0.15 или выше.

- Извлеките содержимое каталогов bin\ обоих архивов в такой же каталог на вашей системе (т.е. C:\Program Files\gettext-utils).

- Обновите системный PATH:
```
Control Panel > System > Advanced > Environment Variables.
```
В списке System variables, выберите Path, затем Edit.

- Добавьте ;C:\Program Files\gettext-utils\bin в конец поля Variable value.

Вы также можете использовать бинарники gettext, взятые где-то, если команда xgettext --version работает правильно. Не пытайтесь выполнять команды Django, использующие пакет gettext, если команда xgettext --version, введённая в консоли Windows, выбрасывает окно с текстом “xgettext.exe has generated errors and will be closed by Windows”.

Настройка команды makemessages
------------------------------
Если вам требуется передать дополнительные параметры в xgettext, вам следует создать свою команду makemessages и переопределить её атрибут xgettext_options:
```
from django.core.management.commands import makemessages

class Command(makemessages.Command):
    xgettext_options = makemessages.Command.xgettext_options + ['--keyword=mytrans']
```

Все репозитории с файлами сообщений имеют одинаковую структуру:
---------------------------------------------------------------
Во всех указанных путях в параметре конфигурации LOCALE_PATHS происходит поиск 
```
<language>/LC_MESSAGES/django.(po|mo)

$APPPATH/locale/<language>/LC_MESSAGES/django.(po|mo)
$PYTHONPATH/django/conf/locale/<language>/LC_MESSAGES/django.(po|mo)
```

Для создания файлов сообщений надо использовать django-admin makemessages. 
--------------------------------------------------------------------------
```
./manage.py makemessages --all

processing locale en
processing locale uk

en/
LC_MESSAGES/
django.po

uk/
LC_MESSAGES/
django.po

```

uk/LC_MESSAGES/django.po:
--------------------------
```
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the PACKAGE package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"Report-Msgid-Bugs-To: \n"
"POT-Creation-Date: 2016-03-09 15:41+0000\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"Language: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n"
"%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"

#: common/arrayfields.py:33
msgid "Character varying array"
msgstr ""

#: common/arrayfields.py:44
msgid "Text array"
msgstr ""

#: common/arrayfields.py:53
msgid "Integer array"
msgstr ""

#: mysite/settings.py:136
msgid "English"
msgstr ""

#: mysite/settings.py:137
msgid "Ukrainian"
msgstr ""

#: orders/models.py:10
msgid "first name"
msgstr "ім'я"

#: orders/models.py:12
msgid "last name"
msgstr "прізвище"

#: orders/models.py:14
msgid "e-mail"
msgstr ""

#: orders/models.py:15
msgid "address"
msgstr "адреса"

#: orders/models.py:17
msgid "postal code"
msgstr "поштовий індекс"

#: orders/models.py:19
msgid "city"
msgstr "місто"

```
перевод
-------
- msgid является переводимой строкой, которая определена в исходном коде. Не изменяйте её.

- msgstr является местом, где вы пишите свой перевод. Обычно оно пустое, именно вы отвечаете за его наполнение. Удостоверьтесь, что вы сохранили кавычки вокруг перевода.
```
#: mysite/settings.py:136
msgid "English"
msgstr "Англійська"

#: mysite/settings.py:137
msgid "Ukrainian"
msgstr "Українська"
```

Для удобства, каждое сообщение включает, в виде закомментированной строки, размещенной выше строки msgid, имя файла и номер строки из которой была получена переводимая строка.

Укажите свою кодировку
----------------------
Из-за особенностей внутренней работы утилит пакета gettext и нашего желания позволить использование не-ASCII символов в строках кода Django и ваших приложений, вы должны использовать UTF-8 в качестве кодировки ваших PO файлов (по умолчанию при их создании). Это означает, что все будут использовать одинаковую кодировку, что очень важно в момент, когда Django обрабатывает PO файлы.
Для повторного прохода по всему исходному коду и шаблонам в поисках новых переводимых строк и для обновления всех файлов с сообщениями для всех языков, выполните это:
```
django-admin makemessages -a
```

Комментарии для переводчиков
-----------------------------
Если необходимо дать переводчикам подсказку по переводимой строке, вы можете добавить комментарий с префиксом Translators в строке предшествующей переводимой, например:
```
def my_view(request):
    # Translators: This message appears on the home page only
    output = ugettext("Welcome to my site.")
```
Комментарий появится в результирующем .po файле, который связан с переводимой конструкцией расположенной далее, и должен быть отображён большинством средств перевода.

Для полноты изложения приведём соответствующий фрагмент .po файла:
```
#. Translators: This message appears on the home page only
# path/to/python/file.py:123
msgid "Welcome to my site."
msgstr ""
```
Пометка строк как no-op
------------------------
Используйте функцию django.utils.translation.ugettext_noop() для пометки строки как переводимой, но не переводя её. Такая строка будет переведена позже с помощью переменной.


coupons/forms.py:
-----------------
```
from django import forms
from django.utils.translation import gettext_lazy as _

class CouponApplyForm(forms.Form):
    code = forms.CharField(label=_('Coupon'))
    
```

Интернационализация: в коде шаблонов
====================================
Для перевода текста в шаблонах Django используют два шаблонных тега и немного отличающийся от Python синтаксис. Чтобы воспользоваться этими тегами, поместите {% load i18n %} в начало шаблона. Аналогично остальным шаблонным тегам, данный тег должен быть указан во всех шаблонах, которые применяют механизм переводов, даже в тех, которые расширяются из других шаблонов, имеющих в себе тег i18n.

Шаблонный тег trans
-------------------
Шаблонный тег {% trans %} может переводить как обычную строку, заключенную в одинарные или двойные кавычки, так и содержимое переменой:
```
{% extends "shop/base.html" %}
{% load i18n %}

{% block title %}
    {% trans "Checkout" %}
{% endblock %}
```

При использовании опции noop, обращение к переменной происходит, но перевод не выполняется. Это удобно, когда надо пометить контент для перевода в будущем:

```
{% extends "shop/base.html" %}
{% load i18n %}

{% block title %}
    {% trans "Checkout" noop %}
{% endblock %}
```

```

Перевод подстроки выполняется с помощью функции ugettext().
-----------------------------------------------------------
В случае передачи шаблонной переменой в тег, тег сначала преобразовывает её в строку, а затем ищет для неё перевод в каталогах сообщений.

Невозможно использовать шаблонные переменные внутри строки для тега {% trans %}. Если же ваш перевод требует наличия переменой в строке, используйте шаблонный тег {% blocktrans %}.

Шаблонный тег blocktrans
------------------------
В отличии от тега trans, тег blocktrans позволяет отмечать сложные предложения, состоящие из строк и переменных, обеспечивая перевод с помощью подстановок.

Для перевода шаблонных выражений с доступом к атрибутам объекта или с использованием шаблонных фильтров, потребуется связать выражение с локальной переменной для использования внутри переводимого блока. Примеры:
```
<div class="order-info">
        <h3>{% trans "Your order" %}</h3>
        <ul>
            {% for item in cart %}
                <li>{{ item.quantity }}x {{ item.product.name }} <span>${{ item.total_price }}</span></li>
            {% endfor %}
            {% if cart.coupon %}
                <li>
                    {% blocktrans with code=cart.coupon.code discount=cart.coupon.discount %}
                        "{{ code }}" ({{ discount }}% off)
                    {% endblocktrans %}
                    <span>- ${{ cart.get_discount|floatformat:"2" }}</span>
                </li>
            {% endif %}
        </ul>
        <p>{% trans "Total" %}: ${{ cart.get_total_price_after_discount|floatformat:"2" }}</p>
    </div>

```

Внутри тега blocktrans запрещается использовать другие блочные теги (например {% for %} или {% if %}).

Длинные сообщения являются особым случаем. Так, первая строка сразу после msgstr (или msgid) всегда пустая. Затем идёт длинный перевод, разбитый на несколько строк. Эти строки будут собраны в одну. Не забывайте вставлять завершающие пробелы, иначе итоговая строка будет собрана без них!

'''
#: templates/shop/orders/create.html:5 templates/shop/orders/create.html:9
msgid "Checkout"
msgstr ""

#: templates/shop/orders/create.html:12
msgid "Your order"
msgstr ""

#: templates/shop/orders/create.html:19
#, python-format
msgid ""
"\n"
"                        \"%(code)s\" (%(discount)s%% off)\n"
"                    "
msgstr ""

#: templates/shop/orders/create.html:26
msgid "Total"
msgstr ""

#: templates/shop/orders/create.html:31
msgid "Place order"
msgstr ""

#: templates/shop/orders/created.html:5 templates/shop/orders/created.html:9
msgid "Thank you"
msgstr ""

#: templates/shop/orders/created.html:10
#, python-format
msgid ""
"\n"
"        <p>Your order has been successfully completed. Your order number is "
"<strong>%(order_id)s</strong>.</p>\n"
"    "
msgstr ""

'''

Если невозможно вычисление хотя бы одного из аргументов блока, тогда тег переключается на язык по умолчанию с помощью функции deactivate_all().

Другой особенностью {% blocktrans %} является поддержка опции trimmed. Эта опция удаляет символы завершения строки из начала и конца содержимого данного тега, убирая пробелы в начале и конце строк и объединяя все строки в одну, разделяя их пробелами. Это очень удобно при форматировании контента тега с помощью отступов, так как эти пробелы не попадают в содержимое PO файлов, упрощая процесс перевода.

Например, следующий тег {% blocktrans %}:
```
{% blocktrans trimmed %}
  First sentence.
  Second paragraph.
{% endblocktrans %}
```
выразится в записи``”First sentence. Second paragraph.”`` внутри PO файла, что несравнимо с "\n  First sentence.\n  Second sentence.\n", в случае когда опция trimmed не используется.

Компиляция файлов с сообщениями
===============================
После того, как вы создали файл с сообщениями, а также после каждого его обновления, вам следует скомпилировать этот файл, чтобы позволить gettext его использовать. Сделайте это с помощью утилиты django-admin compilemessages.

Эта команда обрабатывает все имеющиеся .po файлы и создаёт на их основе .mo файлы, которые являются бинарными файлами, оптимизированными для использования gettext. Запускать django-admin compilemessages надо в том же каталоге, что и django-admin makemessages, вот так:
```
django-admin compilemessages
````
Ваш перевод готов к использованию.

django-admin compilemessages
-----------------------------
Для компиляции файлов перевода надо использовать django-admin compilemessages, это приведёт к созданию бинарных .mo файлов, которые нужны для работы gettext.

django-admin compilemessages --settings=path.to.settings

```
./manage.py compilemessages
processing file django.po in /home/janus/github/dj-21v/unit_15/mysite/locale/en/LC_MESSAGES
processing file django.po in /home/janus/github/dj-21v/unit_15/mysite/locale/uk/LC_MESSAGES


en/
LC_MESSAGES/
django.mo
django.po

uk/
LC_MESSAGES/
django.mo
django.po
```

Измените urls.py
================
Для поддержки нескольких языков в URL нужно использовать i18n_patterns вместо patterns в urls.py
```
from django.conf.urls.i18n import i18n_patterns

urlpatterns += i18n_patterns(
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^coupons/', include('coupons.urls', namespace='coupons')),

    url(r'^admin/', admin.site.urls),
    )

```
base.html
----------
```
{% load i18n %}
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>{% block title %}{% trans "My shop" %}{% endblock %}</title>
    <link href="{% static "css/base.css" %}" rel="stylesheet">
</head>
<body>
    <div id="header">
        <a href="/" class="logo">{% trans "My shop" %}</a>
        
        {% get_current_language as LANGUAGE_CODE %}
        {% get_available_languages as LANGUAGES %}
        {% get_language_info_list for LANGUAGES as languages %}
        <div class="languages">
            <p>{% trans "Language" %}:</p> 
            <ul class="languages">
            {% for language in languages %}
                <li>
                    <a href="/{{ language.code }}/shop" {% if language.code == LANGUAGE_CODE %} class="selected"{% endif %}>
                    {{ language.name_local }}
                    </a>
                </li>
            {% endfor %}
            </ul> 
        </div>
    </div>
    <div id="subheader">
        <div class="cart">
            {% with total_items=cart|length %}
                {% if cart|length > 0 %}
                    {% trans "Your cart" %}: 
                    <a href="{% url "cart:cart_detail" %}">
                        {% blocktrans with total_items_plural=total_items|pluralize total_price=cart.get_total_price %}
                            {{ total_items }} item{{ total_items_plural }}, ${{ total_price }}
                        {% endblocktrans %}
                    </a>
                {% else %}
                    {% trans "Your cart is empty." %}
                {% endif %}
            {% endwith %}
        </div>
    </div>
    <div id="content">
        {% block content %}
        {% endblock %}
    </div>
</body>
</html>
```
