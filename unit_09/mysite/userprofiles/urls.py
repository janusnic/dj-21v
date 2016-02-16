# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^register/$', views.RegistrationView.as_view(), name='userprofiles_registration'),
    url(r'^register/complete/$', views.RegistrationCompleteView.as_view(), name='userprofiles_registration_complete'),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

   ]
