from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=4096)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=0)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
