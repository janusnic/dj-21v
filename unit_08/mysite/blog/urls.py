from django.conf.urls import url

from . import views

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
