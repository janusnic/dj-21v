# -*- coding: UTF-8 -*-
from django import template
from blog.models import Article

register=template.Library()
 
@register.inclusion_tag('blog/_latest_posts.html') # регистрируем тег и подключаем шаблон _latest_posts

def latest_posts():
    posts = Article.objects.order_by('-publish_date').filter(status='P')[:6]
    return locals()
