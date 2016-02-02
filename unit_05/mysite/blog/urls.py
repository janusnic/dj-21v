from django.conf.urls import url

from . import views

urlpatterns = [
    
    # ex: /blog/
    url(r'^$', views.index, name='index'),
    url(r'^news/$', views.news, name='news'),
    url(r'^2016/$', views.special_case_2016),
    url(r'^latest/$', views.latest),
    
    # ex: /blog/5/
    url(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /blog/5/results/
    # url(r'^(?P<blog_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /blog/5/vote/
    url(r'^(?P<blog_id>[0-9]+)/vote/$', views.vote, name='vote'),

    
    url(r'^([0-9]{4})/$', views.year_archive),
    url(r'^([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),

    url(r'^(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
]
