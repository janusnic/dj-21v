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
