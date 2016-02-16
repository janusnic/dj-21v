# dj-21v

userprofiles
========
```
./manage.py startapp userprofiles
```
settings.py
------------
```
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ckeditor',
    'ckeditor_uploader',
    'blog',
    'userprofiles',
]
```
userprofiles/models.py
--------------------------
```
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.auth.models import User

from django.db.models.signals import post_save
# Create your models here.
@python_2_unicode_compatible
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.

    location = models.CharField(max_length=140, blank=True)
    gender = models.CharField(max_length=140, blank=True)
    age = models.IntegerField(default=0, blank=True)
    company = models.CharField(max_length=50, blank=True)

    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

    # Override the __str__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

# Signal while saving user
post_save.connect(create_profile, sender=User)

```
Migrations
------------
```
./manage.py makemigrations userprofiles
Migrations for 'userprofiles':
  0001_initial.py:
    - Create model UserProfile
./manage.py migrate
Operations to perform:
  Apply all migrations: sessions, blog, admin, userprofiles, contenttypes, auth
Running migrations:
  Rendering model states... DONE
  Applying userprofiles.0001_initial... OK
```
Объект InlineModelAdmin
=================
Интерфейс администратора позволяет редактировать связанные объекты на одной странице с родительским объектом. Это называется “inlines”.

Вы можете редактировать userprofile на странице редактирования user.

Вы добавляете “inlines” к модели добавив их в ModelAdmin.inlines:
userprofiles/admin.py
-------------------------
```
from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserProfileAdmin(UserAdmin):
    inlines=(UserProfileInline, )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)

```
Django предоставляет два подкласса InlineModelAdmin:
------------------------------------------------------------------
  1. TabularInline
  2. StackedInline
  Разница между ними только в используемом шаблоне.

Создание форм в Django Класс Form
========================
```
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[\w.-]+$', error_messages={'invalid': 'This value may contain only letters, numbers and ./-/_ characters.'})
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(render_value=False))
```
Максимальное количество символом в значении мы указали с помощью параметра max_length. Он используется для двух вещей. Будет добавлен атрибут maxlength="30" в HTML тег input (теперь браузер не позволит пользователю ввести больше символов, чем мы указали). Также Django выполнит проверку введенного значения, когда получит запрос с браузера с введенными данными.

Экземпляр Form содержит метод is_valid(), который выполняет проверку всех полей формы. Если все данные правильные, это метод:
- вернет True
- добавит данные формы в атрибут cleaned_data.

После рендеринга наша форма будет выглядеть следующим образом:

```
<p><label for="id_username">Username:</label> <input class="form-control" id="id_username" maxlength="30" name="username" placeholder="Enter Your User Name" type="text" /></p>
<p><label for="id_email">E-mail:</label> <input class="form-control" id="id_email" name="email" placeholder="johndoe@company.com" type="email" /></p>
<p><label for="id_password">Password:</label> <input class="form-control" id="id_password" name="password" placeholder="Easy to remember, hard to guess" type="password" /></p>
```
Обратите внимание, она не содержит тег form, или кнопку отправки. Вам необходимо самостоятельно их добавить в шаблоне.

Представление
------------------
Данные формы отправляются обратно в Django и обрабатываются представлением, обычно тем же, которое и создает форму. Это позволяет повторно использовать часть кода.

Для обработки данных формой нам необходимо создать ее в представлении для URL, на который браузер отправляет данные формы:
```
# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView

from userprofiles.utils import get_form_class
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

class RegistrationView(FormView):
    form_class = get_form_class('userprofiles.forms.RegistrationForm')
    template_name = 'userprofiles/registration.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # return redirect(up_settings.REGISTRATION_REDIRECT)
        url = reverse('users:userprofiles_registration_complete')
        return HttpResponseRedirect(url)

registration = RegistrationView.as_view()

```
Если в представление пришел GET запрос, будет создана пустая форма и добавлена в контекст шаблона для последующего рендеринга. Это мы и ожидаем получить первый раз открыв страницу с формой.

Если форма отправлена через POST запрос, представление создаст форму с данными из запроса: form = RegistrationForm(request.POST) Это называется “привязать данные к форме” (теперь это связанная с данными форма).

Шаблон
----------
templates/userprofiles/registration.html
---------------------------------------------
```
{% extends "base.html" %}
{% block head_title %} {{ block.super }} - Register with Blog {% endblock %}

{% block content %}
<div class="container">
    <div class="row">
    <h2>Register with Janus Blog</h2>
    <form action="." method="post" class="form-horisontal" role="form">
      <div class="form-group">
        {% csrf_token %}
        <fieldset>
            {{ form.as_p }}
        </fieldset>
      </div>
      </div>
      <div class="row">
      <div class="form-group">
        <fieldset class="submit-row">
            <p><button type="submit" class="btn btn-info">Create account</button></p>
        </fieldset>
      </div>
    </form>
    </div>
</div>
{% endblock %}

```
RegistrationForm
===========
forms.py
---------
```
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[\w.-]+$', error_messages={'invalid': 'This value may contain only letters, numbers and ./-/_ characters.'})
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        new_user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email']
            )

        if hasattr(self, 'save_profile'):
            self.save_profile(new_user, *args, **kwargs)

        return new_user

```

Field.widget
--------------
Настройка классов виджета
--------------------------------
attrs
-----
Словарь, которые содержит HTML атрибуты, которые будут назначены сгенерированному виджету.

forms.py
---------
```
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[\w.-]+$', error_messages={'invalid': 'This value may contain only letters, numbers and ./-/_ characters.'})
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter Your User Name'})

        self.fields['email'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'johndoe@company.com'})

        self.fields['password'].widget.attrs.update({'class' : 'form-control'})
        self.fields['password'].widget.attrs.update({'placeholder' : 'Easy to remember, hard to guess'})

    def save(self, *args, **kwargs):
        new_user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email']
            )

        if hasattr(self, 'save_profile'):
            self.save_profile(new_user, *args, **kwargs)

        return new_user

```

Представления-классы для редактирования данных
==================================
FormView
-----------
```
class RegistrationView(FormView):
    form_class = get_form_class('userprofiles.forms.RegistrationForm')
    template_name = 'userprofiles/registration.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # return redirect(up_settings.REGISTRATION_REDIRECT)
        url = reverse('users:userprofiles_registration_complete')
        return HttpResponseRedirect(url)

registration = RegistrationView.as_view()

```
as_view()
-----------
Возвращает выполняемое(callable) представление, которое принимает запрос(request) и возвращает ответ(response):
```

registration = RegistrationView.as_view()

```

userprofiles/urls.py
---------------------
```
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.RegistrationView.as_view(), name='userprofiles_registration'),
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
    url(r'^admin/', admin.site.urls),
]

```
HttpResponseRedirect
-------------------------
Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'http://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
url
---
Этот атрибут, доступный только для чтения, содержит URL для редиректа (аналог заголовка Location).
```
url = reverse('users:userprofiles_registration_complete')
return HttpResponseRedirect(url)

```
userprofiles/views.py
------------------------
```
class RegistrationCompleteView(TemplateView):
    template_name = 'userprofiles/registration_complete.html'

    def get_context_data(self, **kwargs):
        return {
            'account_verification_active': False,
            'expiration_days': 7,
        }
registration_complete = RegistrationCompleteView.as_view()

```
userprofiles/registration_complete.html
--------------------------------------------
```
{% extends "base.html" %}
{% block head_title %} {{ block.super }} - Register with Blog {% endblock %}

{% block content %}
    <h1>Registration</h1>
    {% if account_verification_active %}
        <p>
            Your registration was successful. We send you a e-mail including a link.<br />
            Please click the link to activate your account. Thank you!<br />
            <br />
            The link is valid for {{ expiration_days }} days.
        </p>
    {% else %}
        <p>
            Your registration was successful.
        </p>
    {% endif %}
{% endblock %}

```
userprofiles/urls.py
---------------------
```
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.RegistrationView.as_view(), name='userprofiles_registration'),
    url(r'^register/complete/$', views.RegistrationCompleteView.as_view(), name='userprofiles_registration_complete'),
   ]

```

utils.py
--------
```
from django.core.exceptions import ImproperlyConfigured

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

def get_form_class(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    # except ImportError, e: # python 2.7
    except ImportError as e: # python 3.4
        raise ImproperlyConfigured( 'Error loading module %s: "%s"' % (module, e))
    try:
        form = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a form named "%s"' % (module, attr))
    return form

```

mainnavigation.HTML
------------------------
```
<ul class="nav  navbar-nav navbar-right">
  {% if user.is_authenticated %}
  <li><a href="{% url 'users:logout' %}">Logout</a></li>
  {% else %}
  <li><a href="{% url 'users:userprofiles_registration' %}">Register</a></li>

  <form class="navbar-form navbar-right" role="form" method="post" action="{% url 'users:login' %}">
  {% csrf_token %}
  <div class="form-group">
    <input type="text" placeholder="Username" name="username" class="form-control">
  </div>
  <div class="form-group">
    <input type="password" placeholder="Password" name="password" class="form-control">
  </div>
  <button type="submit" class="btn btn-success">Sign in</button>
</form>
{% endif %}
</ul>

```
