"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from home import views as view_home
from blog import views

urlpatterns = [
    url(r'^$', view_home.home, name='home'),
    
    
    url(r'^blog/2016/$', views.special_case_2016),
    url(r'^blog/([0-9]{4})/$', views.year_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),

    url(r'^blog/', include('blog.urls', namespace="blog")),

    url(r'^blog/(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
    
    url(r'^admin/', admin.site.urls),
]
