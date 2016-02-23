from django.conf.urls import url
from django.contrib.auth.decorators import login_required as auth

from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    #url(r'^news/$', views.news, name='news'),
    url(r'^news/$', views.HomeView.as_view(), name='news'),

    url(r'^latest/$', views.latest),
    url(r"^archive/(\d+)/(\d+)/$", views.monthly_archive , name='archive'),
    url(r'^category/(?P<categoryslug>.*)/$', views.category, name='category' ),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)-(?P<slug>[-\w]*)/$', views.EntryDetail.as_view(), name='entry_detail'),
    
    url(r'^(?P<postslug>.*)/$', views.detail, name='detail' ),

]
