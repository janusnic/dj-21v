# dj-21v

models.py
```

@python_2_unicode_compatible
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(User, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    entry = models.ForeignKey('Article', blank=True, related_name='comments')
    
    def __str__(self):
        return self.content

    def gravatar_url(self):
        # Get the md5 hash of the email address
        md5 = hashlib.md5(self.email.encode())
        digest = md5.hexdigest()

        return 'http://www.gravatar.com/avatar/{}'.format(digest)

```

forms.py

```
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'website', 'content',)

    def __init__(self, *args, **kwargs):
        self.entry = kwargs.pop('entry')   # the blog entry instance
        super().__init__(*args, **kwargs)

    def save(self):
        comment = super().save(commit=False)
        comment.entry = self.entry
        comment.save()
        return comment
```

views.py

```
from .forms import CommentForm
from django.views.generic import ListView

class HomeView(ListView):
    template_name = 'blog/news.html'
    queryset = Article.objects.order_by('-created_date')

```
blog/news.html

```
{% extends "news.html" %}

{% block content %}
    {% for article in article_list %}
        {% include "blog/_entry.html" with article=article only %}
    {% empty %}
        <p>No blog entries yet.</p>
    {% endfor %}
{% endblock content %}

```
blog/_entry.html

```
<article>

    <h2><a href="{{ article.get_absolute_url }}">{{ article.title }}</a></h2>

    <p class="subheader">
        <time>{{ article.publish_date|date }}</time>
    </p>

    <p></p>

    {{ article.content|linebreaks }}

</article>

```

templates/news.html
```
{% load staticfiles %}
{% load blog_tags %}
<!DOCTYPE html>
<html>
<head>
    <title>My Blog</title>
    <link rel="stylesheet" href="{% static "css/foundation.css" %}">
</head>
<body>
    <section class="row">
        <header class="large-12 columns">
            <h1><a href='/'>Welcome to My Blog</a></h1>
            <hr>
        </header>
    </section>

    <section class="row">

        <div class="large-8 columns">
            {% block content %}{% endblock %}
        </div>

        <div class="large-4 columns">
            <h3>About Me</h3>
            <p>I am a Python developer and I like Django.</p>
            <h3>Recent Entries</h3>
            {% entry_history %}
        </div>

    </section>

</body>
</html>

```
{% load blog_tags %}
```
from django import template

from ..models import Article

register = template.Library()

@register.inclusion_tag('blog/_entry_history.html')
def entry_history():
    entries = Article.objects.all()[:5]
    return {'entries': entries}

```

blog/_entry_history.html
```
<ul>
    {% for entry in entries %}
        <li>{{ entry.title }}</li>
    {% empty %}
        <li>No recent entries</li>
    {% endfor %}
</ul>

```

views.py

```

class HomeView(ListView):
    template_name = 'blog/news.html'
    queryset = Article.objects.order_by('-created_date')


class EntryDetail(CreateView):
    model = Article
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['entry'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['entry'] = self.get_object()
        return d

    def get_success_url(self):
        return self.get_object().get_absolute_url()


```

urls.py

```
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

```

blog/entry_detail.html

```
{% extends "news.html" %}

{% block content %}
    {% include "_entry.html" with entry=entry only %}
    <hr>
    <h4>Comments</h4>
    {% for comment in entry.comment_set.all %}
        <p>
            <em>Posted by {{ comment.name }}</em>
            <img src="{{ comment.gravatar_url }}" align="left">
        </p>
        {{ comment|linebreaks }}
    {% empty %}
        No comments yet.
    {% endfor %}
    <h5>Add a comment</h5>
    <form method="post">
        {% csrf_token %}
        {{ form.as_table }}
        <input type="submit" value="Create Comment">
    </form>
{% endblock %}


```

