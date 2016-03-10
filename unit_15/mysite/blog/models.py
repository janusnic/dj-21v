from django.db import models
import datetime
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.auth.models import User

from common.arrayfields import IntegerArrayField

from django.core.urlresolvers import reverse

from django.template.defaultfilters import slugify
import hashlib


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    description = models.TextField(max_length=4096)

    def __str__(self):
        return '%s' % (self.name)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    def __str__(self):
        return '%s' % (self.name)

@python_2_unicode_compatible
class Article(models.Model):
    ARTICLE_STATUS = (
        ('D', 'Not Reviewed'),
        ('P', 'Published'),
        ('E', 'Expired'),
    )
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    status = models.IntegerField(default=0)
    content = models.TextField()
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default='D')
    category = models.ForeignKey(Category, verbose_name="the related category")
    tags = models.ManyToManyField(Tag, verbose_name="the related tags", related_name="keyword_set", blank=True)

    views = models.IntegerField(default=0)
    publish_date = models.DateTimeField(auto_now=True, editable=False, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    def was_published_recently(self):
        return self.publish_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return '%s' % (self.title)

    def get_absolute_url(self):
        kwargs = {'year': self.created_date.year,
                  'month': self.created_date.month,
                  'day': self.created_date.day,
                  'slug': self.slug,
                  'pk': self.pk}
        return reverse('blog:entry_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

@python_2_unicode_compatible
class Comment(models.Model):
    article = models.ForeignKey('Article', blank=True, related_name='comments')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child_set')
    created_at  = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, null=True, blank=True)

    path = IntegerArrayField(blank=True, editable=False) #Can't be null as using append to path for replies and can't append to a None path
    depth = models.PositiveSmallIntegerField(default=0)
    
    content = models.TextField()

    author_name = models.CharField(max_length=50, null=True, blank=True)
    author_url = models.URLField(null=True, blank=True)

    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.content

