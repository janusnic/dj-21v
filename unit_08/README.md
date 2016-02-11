# dj-21v
CKEditor 
========
https://github.com/django-ckeditor/django-ckeditor

```
pip install django-ckeditor
```
CKEditorWidget
===============
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
    
    'ckeditor',
    'ckeditor_uploader',
    'blog',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "public/static")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'


CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"


```

urls.py
--------
```
urlpatterns += [
    url(r'^$', view_home.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    
    url(r'^admin/', admin.site.urls),
]

```

admin.py
--------
```
from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .models import Category, Tag, Article

class ArticleAdminForm(forms.ModelForm):
    
    content = forms.CharField(widget=CKEditorWidget())
    content = forms.CharField(widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Article
        fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['publish_date']

    filter_horizontal = ('tags',)

    prepopulated_fields = {"slug": ("title",)}

    date_hierarchy = 'publish_date'
    readonly_fields = ('publish_date','created_date')
    fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('publish_date','created_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status')]}),
    ]

    actions = [make_published,'make_draft','make_expired']

    form = ArticleAdminForm

```

Аутентификация пользователей в Django
=====================================
Django поставляется с системой аутентификации пользователей. Она обеспечивает пользовательские аккаунты, группы, права и сессии на основе куки.

Система аутентификации Django отвечает за оба аспекта: аутентификацию и авторизацию. аутентификация проверяет пользователя, а авторизация определяет, что аутентифицированный пользователь может делать.

Система аутентификации состоит из:
----------------------------------
1. Пользователей

2. Прав: Бинарные (да/нет) флаги, определяющие наличие у пользователя права выполнять определённые действия.

3. Групп: Общий способ назначения меток и прав на множество пользователей.

4. Настраиваемой системы хеширования паролей

5. Инструментов для форм и представлений для аутентификации пользователей или для ограничения доступа к контенту

Поддержка аутентификации скомпонована в виде модуля в django.contrib.auth. По умолчанию, требуемые настройки уже включены в settings.py, создаваемый с помощью команды django-admin startproject, и представляют собой две записи в параметре конфигурации INSTALLED_APPS:

1. 'django.contrib.auth' содержит ядро системы аутентификации и её стандартные модели.

2. 'django.contrib.contenttypes' является фреймворком типов, который позволяет правам быть назначенными на создаваемые вами модели.

две записи в параметре конфигурации MIDDLEWARE_CLASSES:
-------------------------------------------------------
1. SessionMiddleware управляет сессиями во время запросов.

2. AuthenticationMiddleware ассоциирует пользователей с запросами с помощью сессий.

При наличии этих настроек, применение команды manage.py migrate создаёт в базе данных необходимые для системы аутентификации таблицы, создаёт права для любых моделей всех зарегистрированных приложений.

Использование системы аутентификации пользователя
=================================================

Создание пользователей
----------------------
Самый простой способ создать пользователя – использовать метод create_user():
```
from django.contrib.auth.models import User
user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

# At this point, user is a User object that has already been saved
# to the database. You can continue to change its attributes
# if you want to change other fields.
user.last_name = 'Lennon'
user.save()
```
Создание суперпользователя
--------------------------
Суперпользователя можно создать с помощью команды createsuperuser:
```
$ python manage.py createsuperuser --username=joe --email=joe@example.com
```
Команда попросит ввести пароль. Пользователь будет создан сразу же по завершению команды. Если не указывать --username или the --email, команда попросит ввести их.

UserProfile:
============
models.py
---------
```
from django.contrib.auth.models import User

@python_2_unicode_compatible
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    
    location = models.CharField(max_length=140, blank=True)  
    gender = models.CharField(max_length=140, blank=True)  
    age = models.IntegerField(blank=True)
    company = models.CharField(max_length=50, blank=True)
        
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

    # Override the __str__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

```
makemigrations
--------------
```
./manage.py makemigrations blog
./manage.py migrate
```
admin.py
--------
```
admin.site.register(UserProfile)

```
runserver
----------
```
./manage.py runserver
```

Creating the UserForm and UserProfileForm
==========================================
blog/forms.py
-------------
```
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        # fields = '__all__'

```
Объект пользователя
--------------------
Объекты User - основа системы аутентификации. Они представляют пользователей сайта и используются для проверки прав доступа, регистрации пользователей, ассоциации данных с пользователями. Для представления пользователей в системе аутентификации используется только один класс, 'superusers' или 'staff' такие же объекты пользователей, просто с определенными атрибутами.

Основные атрибуты пользователя:
--------------------------------
- username
- password
- email
- first_name
- last_name

Смена пароля
------------
Django не хранит пароль в открытом виде, только хеш. Поэтому не пробуйте менять атрибут непосредственно. Поэтому пользователь создается через специальную функцию.

Пароль можно сменить несколькими способами:
-------------------------------------------
manage.py changepassword *username* позволяет сменить пароль пользователя через командную строку. Команда требует ввести пароль дважды. Если совпадают, пароль будет изменен. Если не указать имя пользователя, команда попробует найти пользователя с именем раным текущему системному пользователю.

изменить пароль программно, используя метод set_password():
------------------------------------------------------------
```
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
```
При смене пароля будут завершены все сессии пользователя, если вы используете SessionAuthenticationMiddleware.

User Registration View and Template
====================================

Creating the register() View
-----------------------------

views.py:
---------
```
from blog.forms import UserForm, UserProfileForm

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'blog/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

```

Creating the Registration Template
==================================

templates/blog/register.html:
-----------------------------
```
{% extends "base.html" %}
{% block head_title %} {{ block.super }} - Register with Blog {% endblock %}

{% block content %}
    <h2>Register with Janus Blog</h2>
    {% if registered %}
        Janus Blog says: <strong>thank you for registering!</strong>
        <a href="/blog/">Return to the homepage.</a><br />
        {% else %}
        Janus Blog says: <strong>register here!</strong><br />

        <form id="user_form" method="post" action="/blog/register/"
                enctype="multipart/form-data">

            {% csrf_token %}

            <!-- Display each form. The as_p method wraps each element in a paragraph
                 (<p>) element. This ensures each element appears on a new line,
                 making everything look neater. -->
            {{ user_form.as_p }}
            {{ profile_form.as_p }}

            <!-- Provide a button to click to submit the form. -->
          <input type="submit" name="submit" value="Register" />
        </form>
        {% endif %}

{% endblock %}

```

Подделка межсайтового запроса (CSRF)
====================================

Промежуточный слой CSRF и шаблонный тег предоставляют легкую-в-использовании защиту против Межсайтовой подделки запроса. Этот тип атак случается, когда злонамеренный Web сайт содержит ссылку, кнопку формы или некоторый javascript, который предназначен для выполнения некоторых действий на вашем Web сайте, используя учетные данные авторизованного пользователя, который посещал злонамеренный сайт в своем браузере. Сюда также входит связанный тип атак, ‘login CSRF’, где атакуемый сайт обманывает браузер пользователя, авторизируясь на сайте с чужими учетными данными.

Первая защита против CSRF атак - это гарантирование того, что GET запросы (и другие ‘безопасные’ методы, определенные в 9.1.1 Safe Methods, HTTP 1.1, RFC 2616) свободны от побочных эффектов. Запросы через ‘небезопасные’ методы, такие как POST, PUT и DELETE могут быть защищены при помощи шагов, описанных ниже.

Для того чтобы включить CSRF защиту для ваших представлений, выполните следующие шаги:

Промежуточный слой CSRF активирован по умолчанию и находится в настройке MIDDLEWARE_CLASSES. Если вы переопределяете эту настройку, помните, что ``‘django.middleware.csrf.CsrfViewMiddleware’``должен следовать перед промежуточными слоями, которые предполагают, что запрос уже проверен на CSRF атаку.
```
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

```
Если вы отключили защиту, что не рекомендуется, вы можете использовать декоратор csrf_protect() в части представлений, которые вы хотите защитить.

{% csrf_token %}
-----------------
В любом шаблоне, который использует POST форму, используйте тег csrf_token внутри элемента form если форма для внутреннего URL, т. е.:
```
<form action="." method="post">{% csrf_token %}
```
Это не должно делаться для POST форм, которые ссылаются на внешние URL’ы, поскольку это может вызвать утечку CSRF токена, что приводит к уязвимости.

В соответствующих функциях представления, убедитесь, что 'django.template.context_processors.csrf' контекстный процессор используется. Обычно, это может быть сделано в один из двух способов:

Использовать RequestContext, который всегда использует 'django.template.context_processors.csrf' (не зависимо от параметра TEMPLATES ). Если вы используете общие представления или contrib приложения, вы уже застрахованы, так как эти приложения используют RequestContext повсюду.

Вручную импортировать и использовать процессор для генерации CSRF токена и добавить в шаблон контекста. т.е.:
```
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

def my_view(request):
    c = {}
    c.update(csrf(request))
    # ... view code here
    return render_to_response("a_template.html", c)
```

register() View URL Mapping
---------------------------

blog/urls.py:
-------------
```
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^news/$', views.news, name='news'),
    url(r'^latest/$', views.latest),
    url(r"^archive/(\d+)/(\d+)/$", views.monthly_archive , name='archive'),
    url(r'^category/(?P<categoryslug>.*)/$', views.category, name='category' ),

    url(r'^register/$', views.register, name='register'), 
    url(r'^(?P<postslug>.*)/$', views.detail, name='detail' ),
]

```

includes/mainmenu.html
-----------------------
```
          <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home <span class="sr-only">(current)</span></a></li>
            <li><a href="/blog">Blog</a></li>
            <li><a href="/blog/news">News</a></li>
          
            <li><a href="/blog/register">Register</a></li>
          </ul>
```

Login Functionality
===================

blog/views.py:
--------------
```
from django.contrib.auth import authenticate, login

from django.http import HttpResponseRedirect, HttpResponse

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
            # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/blog/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Blog account is disabled.")
        else:
       # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'blog/index.html', {})
        # return render(request, 'blog/login.html', {})
```

Creating a Login Template
=========================
templates/blog/login.html:
--------------------------

```
<!DOCTYPE html>
<html>
    <head>
        <!-- Is anyone getting tired of repeatedly entering the header over and over?? -->
        <title>Blog</title>
    </head>

    <body>
        <h1>Login to Blog</h1>

        <form id="login_form" method="post" action="/blog/login/">
            {% csrf_token %}
            Username: <input type="text" name="username" value="" size="50" />
            <br />
            Password: <input type="password" name="password" value="" size="50" />
            <br />

            <input type="submit" value="submit" />
        </form>

    </body>
</html>

```

Mapping the Login View to a URL
-------------------------------

blog/urls.py:
-------------
```
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^news/$', views.news, name='news'),
    url(r'^latest/$', views.latest),
    url(r"^archive/(\d+)/(\d+)/$", views.monthly_archive , name='archive'),
    url(r'^category/(?P<categoryslug>.*)/$', views.category, name='category' ),
    url(r'^register/$', views.register, name='register'),

    url(r'^login/$', views.user_login, name='login'), 
    url(r'^(?P<postslug>.*)/$', views.detail, name='detail' ),
]
```

includes/mainmenu.html
----------------------
```
        <form class="navbar-form navbar-right" role="form" method="post" action="/blog/login/">
            {% csrf_token %}
            <div class="form-group">
              <input type="text" placeholder="Username" name="username" class="form-control">
            </div>
            <div class="form-group">
              <input type="password" placeholder="Password" name="password" class="form-control">
            </div>
            <button type="submit" class="btn btn-success">Sign in</button>
          </form>
```

Аутентификация пользователей
============================
authenticate(**credentials)
---------------------------
Для аутентификации пользователя по имени и паролю используйте authenticate(). Параметры авторизации передаются как именованные аргументы, по умолчанию это username и password, если пароль и имя пользователя верны, будет возвращен объект User. Если пароль не правильный, authenticate() возвращает None.
```
from django.contrib.auth import authenticate
user = authenticate(username='john', password='secret')
if user is not None:
    # the password verified for the user
    if user.is_active:
        print("User is valid, active and authenticated")
    else:
        print("The password is valid, but the account has been disabled!")
else:
    # the authentication system was unable to verify the username and password
    print("The username and password were incorrect.")
```
Если вам нужно будет ограничить доступ только авторизованным пользователям, используйте декоратор login_required().


{% if user.is_authenticated %}
===============================
```
<h1>Blog says... hello {{ user.username }}!</h1>
{% else %}
<h1>Blog says... hello world!</h1>
{% endif %}
```
Restricting Access
==================
Restricting Access with a Decorator
-----------------------------------
views.py:
----------
```
from django.contrib.auth.decorators import login_required

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
```
urls.py
--------
```
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^news/$', views.news, name='news'),

    url(r'^latest/$', views.latest),
    url(r"^archive/(\d+)/(\d+)/$", views.monthly_archive , name='archive'),
    url(r'^category/(?P<categoryslug>.*)/$', views.category, name='category' ),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'), 
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^(?P<postslug>.*)/$', views.detail, name='detail' ),

]
```
logout
======
views.py:
----------
```
from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/blog/')
```

blog/urls.py:
-------------
```
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^news/$', views.news, name='news'),

    url(r'^latest/$', views.latest),
    url(r"^archive/(\d+)/(\d+)/$", views.monthly_archive , name='archive'),
    url(r'^category/(?P<categoryslug>.*)/$', views.category, name='category' ),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'), 
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^(?P<postslug>.*)/$', views.detail, name='detail' ),
]
```

includes/mainmenu.html
-----------------------
```
    <div id="navbar" class="navbar-collapse collapse">

          <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home <span class="sr-only">(current)</span></a></li>
            <li><a href="/blog">Blog</a></li>
            <li><a href="/blog/news">News</a></li>
            
          </ul>
          
          <ul class="nav  navbar-nav navbar-right">
            {% if user.is_authenticated %}
            <li><a href="/blog/logout/">Logout</a></li>
            {% else %}
            <li><a href="/blog/register">Register</a></li>

            <form class="navbar-form navbar-right" role="form" method="post" action="/blog/login/">
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
          
        </div><!--/.navbar-collapse -->
```

