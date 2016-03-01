# -*- coding: UTF-8 -*-
from django import template
from blog.models import Article

register=template.Library()
 
@register.inclusion_tag('blog/_popular_posts.html') # регистрируем тег и подключаем шаблон _popular_posts

def popular_posts():
    posts = Article.objects.filter(views__gte=5).filter(status='P')[:6]
    return locals()
