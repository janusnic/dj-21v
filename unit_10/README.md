# dj-21v

LoginView(FormView)
==============
views.py
----------
```
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from django.utils.http import is_safe_url
from django.contrib.auth import get_user_model
from django.views.generic import FormView, RedirectView
from django.views.generic import TemplateView, ListView, DetailView

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse

from userprofiles.utils import get_form_class
from .models import UserProfile
from .forms import UserProfileForm

class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    success_url = '/'
    form_class = AuthenticationForm
    template_name = "userprofiles/login.html"
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

```
LogoutView(RedirectView)
================
views.py
----------
```
class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
```
urls.py
--------
```
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^register/$', views.RegistrationView.as_view(), name='userprofiles_registration'),
    url(r'^register/complete/$', views.RegistrationCompleteView.as_view(), name='userprofiles_registration_complete'),

    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
   ]

```
login.html
------------
```

```

mainmenu.html
------------------
```
<ul class="nav  navbar-nav navbar-right">
  {% if user.is_authenticated %}
  <li><a href="{% url 'users:logout' %}">Logout</a></li>

  {% else %}
  <li><a href="{% url 'users:userprofiles_registration' %}">Register</a></li>
  <li><a href="{% url 'users:login' %}">Login</a></li>
{% endif %}
</ul>
```
DetailView
=======
UserProfileDetailView(DetailView)
--------------------------------------
```
class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = 'userprofiles/user_detail.html'

    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

profile = UserProfileDetailView.as_view()

```
user_detail.html
-------------------
```
{% extends "base.html" %}
{% block head_title %} {{ block.super }} - Your profile {% endblock %}

{% block content %}
{% block main %}

<h1>Your profile</h1>

<p>
    Welcome back, {{ user }}!
</p>

{% endblock main %}

{% block aside %}
 {{ block.super }}

{% endblock aside %}

{% endblock %}

```
urls.py
--------
```
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^register/$', views.RegistrationView.as_view(), name='userprofiles_registration'),
    url(r'^register/complete/$', views.RegistrationCompleteView.as_view(), name='userprofiles_registration_complete'),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),

    url(r'^profile/(?P<slug>.*)/$', views.UserProfileDetailView.as_view(), name='profile'),

   ]

```
views.py
----------
```
class LoginView(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    form_class = AuthenticationForm
    template_name = "userprofiles/login.html"
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse("users:profile", kwargs={"slug": self.request.user})

```
mainmenu.html
------------------
```
<ul class="nav  navbar-nav navbar-right">
  {% if user.is_authenticated %}
  <li><a href="{% url 'users:logout' %}">Logout</a></li>
  <li><a href="{% url 'users:profile' slug=user.username %}">{{ user.username }}</a></li>
  {% else %}
  <li><a href="{% url 'users:userprofiles_registration' %}">Register</a></li>
  <li><a href="{% url 'users:login' %}">Login</a></li>
{% endif %}
</ul>
```
PROFILE.html
----------------  
```
{% extends "base.html" %}
{% block head_title %} {{ block.super }} - Profile {% endblock %}
      {% block content %}
            {% block main %}
            {% endblock main %}
            {% block aside %}
                   <h2>Menu</h2>
                    <ul>
                      <li><a href='{% url "users:profile" user.username %}'>My profile</a></li>

                    </ul>
            {% endblock aside %}
        {% endblock content %}

```
user_detail.html
-------------------
```
{% extends "userprofiles/profile.html" %}
{% block head_title %} {{ block.super }} - Your profile {% endblock %}

{% block content %}
<div class="row">
  <div class="col-md-8">

{% block main %}

<h1>Your profile</h1>

<p>
    Welcome back, {{ user }} !
</p>

{% endblock main %}
</div>

<div class="col-md-4">
{% block aside %}
 {{ block.super }}

{% endblock aside %}
</div>
    </div>
{% endblock %}

```
UpdateView
========
forms.py
----------
```
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.user_form = UserForm(*args, **user_kwargs)
        # magic end
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.user_form.fields)
        self.initial.update(self.user_form.initial)

    def save(self, *args, **kwargs):
        self.user_form.save(*args, **kwargs)
        return super(UserProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = UserProfile
        exclude = ['user']

```

-------------------------------------
views.py
----------
```
from django.views.generic import UpdateView
class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "userprofiles/edit_profile.html"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("users:profile", kwargs={"slug": self.request.user})
```

edit_profile.html
-------------------
```
{% extends "userprofiles/profile.html" %}
{% block head_title %} {{ block.super }} - Your profile {% endblock %}

{% block content %}
<div class="row">
  <div class="col-md-8">

{% block main %}

<div class="row-fluid">
  <div class="span4 offset4">

<h2>{{ user.username }}'s Profile</h2>

<form method="post" action="">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Edit">
</form>


</div>
</div>
{% endblock main %}
</div>

<div class="col-md-4">
{% block aside %}
 {{ block.super }}

{% endblock aside %}
</div>
    </div>

{% endblock %}

```
urls.py
--------
```
# -*- coding: utf-8 -*-
from django.conf.urls import url

from django.contrib.auth.decorators import login_required as auth
from . import views

urlpatterns = [
    url(r'^register/$', views.RegistrationView.as_view(), name='userprofiles_registration'),
    url(r'^register/complete/$', views.RegistrationCompleteView.as_view(), name='userprofiles_registration_complete'),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
    url(r'^profile/(?P<slug>.*)/$', views.UserProfileDetailView.as_view(), name='profile'),

    url(r'^edit_profile/$', auth(views.UserProfileEditView.as_view()), name='edit_profile'),
   ]

```

profile.html
--------------
```
{% extends "base.html" %}
{% block head_title %} {{ block.super }} - Profile {% endblock %}
      {% block content %}
            {% block main %}
            {% endblock main %}
            {% block aside %}
                   <h2>Menu</h2>
                    <ul>
                      <li><a href='{% url "users:profile" user.username %}'>My profile</a></li>
                      <li><a href='{% url "users:edit_profile" %}'>Edit my profile</a></li>

                    </ul>
            {% endblock aside %}
        {% endblock content %}

```
field in form
--------------
```
{% for field in form %}
{{ form.non_field_errors }}
	<div class="f_row">
		{{ field.errors }}
		{{ field.label_tag }}
		<div class="f_input">
			{{ field }}
			{% if field.help_text %}<div class="note">{{ field.help_text }}</div>{% endif %}
		</div>
	</div>
{% endfor %}
```

методы as_p, as_ul и as_table вызывают метод
```
 _html_output
```
 класса BaseForm инструктируя его, как именно рисовать форму.

 добавим свой метод as_div:
 ==================
 ```
 class SuperModelForm(forms.ModelForm):
     error_css_class = 'class-error'
     required_css_class = 'class-required'
     def __init__(self, *args, **kwargs):
         super(forms.ModelForm, self).__init__(*args, **kwargs)
     def as_div(self):
         return self._html_output(
             normal_row = u'<div%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
             error_row = u'<div class="error">%s</div>',
             row_ender = '</div>',
             help_text_html = u'<div class="hefp-text">%s</div>',
             errors_on_separate_row = False)

 ```
errors_on_separate_row.
-----------------------------
Если этот параметр установлен в True, то ошибки будут выводиться отдельным блоком. Он используется, например в as_p, чтобы не запихивать ul внутрь p.

Теперь, мы можем наследовать формы от SuperModelForm и вызывать их в шаблонах с помощью {{ form.as_div }}.
```

class UserForm(SuperModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class UserProfileForm(SuperModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.user_form = UserForm(*args, **user_kwargs)
        # magic end
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.user_form.fields)
        self.initial.update(self.user_form.initial)

    def save(self, *args, **kwargs):
        self.user_form.save(*args, **kwargs)
        return super(UserProfileForm, self).save(*args, **kwargs)

    class Meta:
        model = UserProfile
        exclude = ['user']

```

свои css-классы для обязательного поля и поля с ошибкой
---------------------------------------------------------------------
```
error_css_class = 'class-error'
required_css_class = 'class-required'
```
добавить всем полям какие-то css-классы
-------------------------------------------------
```
def __init__(self, *args, **kwargs):
    super(ModelForm, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'some-class other-class'
```

SuperModelForm
-------------------
```
class SuperModelForm(forms.ModelForm):
    error_css_class = 'class-error'
    required_css_class = 'class-required'
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'some-class other-class'
    def as_div(self):
        return self._html_output(
            normal_row = u'<div%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div class="hefp-text">%s</div>',
            errors_on_separate_row = False)
```
user_detail.html
-------------------
```
<form method="post" action="">
  {% csrf_token %}
  {{ form.as_div }}
  <input type="submit" value="Edit">
</form>

```
Avatar
=====

edit_profile.html
-------------------
```
{% extends "userprofiles/profile.html" %}
{% block head_title %} {{ block.super }} - Your profile {% endblock %}

{% block content %}
<div class="row">
  <div class="col-md-8">

{% block main %}

<div class="row-fluid">
  <div class="span4 offset4">

<h2>{{ user.username }}'s Profile</h2>

<form method="post" action="" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form.as_div }}
  <input type="submit" value="Change profile">
</form>


</div>
</div>
{% endblock main %}
</div>

<div class="col-md-4">
{% block aside %}
{% if object.profile_picture %}
<img src='/media/{{ object.profile_picture }}'>
 {% endif %}
 {{ block.super }}

{% endblock aside %}
</div>
    </div>

{% endblock %}

```

models.py
------------
```
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import os.path
from django.contrib.auth.models import User

from django.db.models.signals import post_save

def get_image_path(instance, filename):
    return os.path.join('avatars', str(instance.id), filename)
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
    profile_picture = models.ImageField(upload_to=get_image_path, blank=True)

    # Override the __str__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

# Signal while saving user
post_save.connect(create_profile, sender=User)

```
forms.py
----------
```
class UserProfileForm(SuperModelForm):
    def __init__(self, *args, **kwargs):
        # magic
        self.user = kwargs['instance'].user
        user_kwargs = kwargs.copy()
        user_kwargs['instance'] = self.user
        self.user_form = UserForm(*args, **user_kwargs)
        # magic end
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields.update(self.user_form.fields)
        self.initial.update(self.user_form.initial)

    def save(self, *args, **kwargs):
        self.user_form.save(*args, **kwargs)
        return super(UserProfileForm, self).save(*args, **kwargs)

    def clean_avatar(self):
        avatar = self.cleaned_data['profile_picture']

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar

    class Meta:
        model = UserProfile
        exclude = ['user']
```
