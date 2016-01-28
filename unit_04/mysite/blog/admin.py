from django.contrib import admin

from .models import Category, Tag, Article

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
