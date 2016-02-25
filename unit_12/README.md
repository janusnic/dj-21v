# dj-21v

Формы моделей(Model Forms)
==========================
Общие CBV автоматически создают класс ModelForm при работе с моделями:

- Если указано значение атрибута model, то будет использоваться этот класс модели.
- Если метод get_object() возвращает объект, то будет использоваться класс этого объекта.
- Если указан атрибут queryset, то будет использована модель этого запроса(queryset).

Представления форм, связанные с моделями, предоставляют реализацию метода form_valid(), которая автоматически сохраняет модель. Вы можете переопределить этот метод согласно вашим требованиям; 

Вы можете не устанавливать значение success_url для классов CreateView или UpdateView - они воспользуются методом get_absolute_url() объекта модели (если такой объект доступен).

Если вам необходимо специальное поведение для ModelForm (например для дополнительной валидации данных) просто установите form_class в нужное значение.

При создании пользовательского класса формы, вы по прежнему должны указать модель. Даже в том случае если в form_class используется ModelForm.
Во-первых, мы должны добавить метод get_absolute_url() в наш класс Article:

models.py
---------
```
from django.core.urlresolvers import reverse
from django.db import models

class Article(models.Model):
    ....
    def __str__(self):
        return '%s' % (self.title)

    def get_absolute_url(self):
        kwargs = {'year': self.created_date.year,
                  'month': self.created_date.month,
                  'day': self.created_date.day,
                  'slug': self.slug,
                  'pk': self.pk}
        return reverse('blog:entry_detail', kwargs=kwargs)
```
Затем мы можем использовать класс CreateView и “сотоварищей” чтобы выполнить необходимую работу. 

views.py
--------
```
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy
from .models import Article

class ArticleDetail(CreateView):
    model = Article
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

```
И наконец, мы подключаем новые представления в URLconf:

urls.py
```
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<pk>\d+)-(?P<slug>[-\w]*)/$', views.ArticleDetail.as_view(), name='entry_detail'),
]
```

Классы CreateView и UpdateView используют myapp/author_form.html

Классы DeleteView используют myapp/author_confirm_delete.html

Если вам нужно разделить шаблоны для классов CreateView и UpdateView, вы можете либо назначить атрибут template_name, либо использовать template_name_suffix в ваших классах представлений.

Модели и request.user
----------------------
Чтобы отслеживать пользователя, создавшего некий объект с помощью CreateView, вы можете использовать пользовательский класс ModelForm. Первое, добавьте внешний ключ (foreign key) к модели:

models.py
----------
```
from django.contrib.auth.models import User
from django.db import models
```
class Comment(models.Model):
    
    user = models.ForeignKey(User, null=True, blank=True)
    author_name = models.CharField(max_length=50, null=True, blank=True)

    # ...
```
В представлении удостоверьтесь, что вы не включаете user в список редактируемых полей и переопределите метод form_valid() для добавления пользователя:

Реализация по умолчанию для метода form_valid() просто осуществляет редирект на URL, хранящийся в атрибуте success_url.

views.py
--------
```
from django.views.generic.edit import CreateView
from myapp.models import Article

class ArticleDetail(CreateView):
    model = Article
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
       
        form.instance.user = self.request.user
        form.instance.author_name = self.request.user.username
        form.save()
        return super(ArticleDetail, self).form_valid(form)

```
В случае, когда форме переданы некорректные данные вызывается метод form_invalid, который по умолчанию возвращает пользователя обратно на страницу формы, передавая ей объект со списком ошибок валидации.

Модель комментария:
===================
Модель использует стандартные поля Django. Древовидность реализуется ссылкой на родителя.
```
Comment 1 - Path: {1}
    Comment 2 - Path: {1, 2}
        Comment 4 - Path: {1, 2, 4}
    Comment 3 - Path: {1, 3}

```
models.py
```
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

```

admin.py
```
from .models import Category, Tag, Article, Comment
admin.site.register(Comment)
```
Метод get_success_url
---------------------
Метод get_success_url возвращает url ссылку, на которую будет осуществляться переход после успешной обработки формы. По умолчанию данный метод возвращает атрибут success_url.

views.py
--------
```
from django.views.generic.edit import CreateView
from myapp.models import Article

class ArticleDetail(CreateView):
    model = Article
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
       
        form.instance.user = self.request.user
        form.instance.author_name = self.request.user.username
        form.save()
        return super(ArticleDetail, self).form_valid(form)

    def get_success_url(self):
        return self.get_object().get_absolute_url()

```
метод get_form_kwargs
---------------------
Часто возникает необходимость передать в форму определенные данные, например объект пользователя или заранее определенный список разделов. Для данного действия подходит метод get_form_kwargs. При переопределении данного метода необходимо соблюдать осторожность и не переписать случайно данные, передаваемые в форму по умолчанию.

views.py
--------
```
from django.views.generic.edit import CreateView
from myapp.models import Article

class ArticleDetail(CreateView):
    model = Article
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
       
        form.instance.user = self.request.user
        form.instance.author_name = self.request.user.username
        form.save()
        return super(ArticleDetail, self).form_valid(form)

    def get_form_kwargs(self):
        """
        Возвращает словарь аргументов для экземпляра формы
        """
        
        kwargs['article'] = self.get_object()
        return kwargs

    def get_success_url(self):
        return self.get_object().get_absolute_url()

```
Чтобы избежать потери данных мы должны сначала получить словарь из родительского класса, затем добавить в него требуемые данные:

super
------
class ArticleDetail(CreateView):

    def get_form_kwargs(self):
        """
        Возвращает словарь аргументов для экземпляра формы
        """
        kwargs = super().get_form_kwargs()
        kwargs['article'] = self.get_object()
        return kwargs
```

forms.py
---------
```
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author_url', 'content',)

    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article')   # the blog article instance
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        comment = super().save(commit=False)
        comment.article = self.article
        comment.save()
        return comment
```

Теперь мы можем передать объект данной формы в наше отображение. 
```
from django.views.generic.edit import CreateView

class ArticleDetail(CreateView):
    model = Article
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        
        # Мы используем forms.ModelForm, 
        # а его метод save(self, *args, **kwargs) возвращает инстанс
        # модели, связанный с формой. Аргумент commit=False говорит о том, что
        # записывать модель в базу рановато.

        instance = form.save(commit=False)

        instance.user = self.request.user
        # Теперь, когда у нас есть несохранённая модель, можно 
        # заполнить внешний ключ на auth.User.
        instance.author_name = self.request.user.username
        # А теперь можно сохранить в базу
        instance.save()
        return super(ArticleDetail, self).form_valid(form)
```

get_context_data
-----------------
передать дополнительный контекст
```
def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['article'] = self.get_object()
        return d

```
Допустим у нас есть статья, просмотр которой мы реализуем с помощью класса DetailView. Нам необходимо также получить список комментариев к данной статье. 
```
from django.views.generic.detail import DetailView
from models import Article, Comment

class PostDetail(DetailView):
    
    model = Article

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(content=self.object, delete=False).order_by('-created_at')
        return context
```

получить доступ к текущему объекту при реализации DetailView можно через атрибут object.

метод get_queryset
------------------
Прежде чем вывести информацию в шаблон нам необходимо ее получить. В этом нам поможет метод get_queryset, задача которого вернуть объект QuerySet. По умолчанию данный метод возвращает атрибут queryset если он определен, либо список всех объектов модели, которая указана в атрибуте model. Мы можем переопределить данный метод, чтобы он удовлетворял нашим задачам.

```
class HomeView(ListView):
    template_name = 'blog/news.html'
    queryset = Article.objects.order_by('-created_date')

```

forms.py

```
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    
    parent = forms.CharField(widget=forms.HiddenInput(
                            attrs={'class': 'parent'}), required=False)
    

    class Meta:
        model = Comment
        fields = ('author_url', 'content',)

    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article')   # the blog article instance
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        comment = super().save(commit=False)
        comment.article = self.article
        comment.save()
        return comment
```

views.py

```
class ArticleDetail(CreateView):
    model = Article
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def dispatch(self, *args, **kwargs):
        return super(ArticleDetail, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)

        if form['parent'].value() == '':
            instance.user = self.request.user
            instance.author_name = self.request.user.username
            
        else:
            parent = Comment.objects.get(id=int(form['parent'].value()))
            instance.parent = parent
            
            instance.user = self.request.user
            instance.author_name = self.request.user.username
            instance.depth = parent.depth + 1
            
            instance.path = parent.path
            

        instance.save()
        
        return super(ArticleDetail, self).form_valid(form)

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
    <link rel="stylesheet" href="{% static "css/main.css" %}">

    <script src="{% static "js/vendor/jquery-1.11.2.min.js" %}"></script>
    <script>
        $(document).ready(function(){
            $("#comments").on("click", ".reply", function(event){
                event.preventDefault();
                var form = $("#postcomment").clone(true);
                form.find('.parent').val($(this).parent().parent().attr('id'));
                $(this).parent().append(form);
            });
        });
    </script>
</head>
<body>
    <section class="row">
        <header class="large-12 columns">
            <h1>Welcome to My Blog</h1>
            <hr>
        </header>
    </section>

    <section class="row">

        <div class="large-8 columns">
            {% block content %}{% endblock %}
        </div>

        <div class="large-4 columns">
            <h3>About Me</h3>
            <p><a href='/'>Home Page</a></p>
            <p>I am a Python developer and I like Django.</p>
            <h3>Recent Entries</h3>
            {% entry_history %}
        </div>

    </section>

</body>
</html>

```


blog/entry_detail.html

```
{% extends "news.html" %}
{% load humanize %}
{% block content %}
    {% include "_entry.html" with article=article only %}
    <hr>

    {% if user.is_authenticated %}

    <h5>Hi {{ user }}! Add a comment</h5>
    <form id="postcomment" method="post">
        {% csrf_token %}
        {{ form.as_table }}

        <input type="submit" value="Create Comment">
    </form>
    {% endif%}

    <h4>Comments</h4>
    <ul id="comments">
    {% for comment in comment_tree %}
    {% if comment.user %}
        <li id="{{comment.id}}" class="comment" style="margin-left:{{comment.depth|add:comment.depth}}em;"><p class="poster"><span class="user">{% if comment.user.get_full_name %}{{comment.user.get_full_name}}{% else %}{{comment.user.username}}{% endif %}</span> - {{comment.modified_at|naturaltime}}</p><p>{{comment.content|safe}}</p><p><a href="" class="reply">reply</a></p></li>
    {% elif comment.name %}
        <li id="{{comment.id}}" class="comment" style="margin-left:{{comment.depth|add:comment.depth}}em;"><p class="poster">{% if comment.website %}<a href="{{comment.website}}">{{comment.name}}</a>{% else %}{{comment.name}}{% endif %} - {{comment.modified_at|naturaltime}}</p><p>{{comment.content|safe}}</p><p><a href="" class="reply">reply</a></p></li>
    {% else %}
        <li id="{{comment.id}}" class="comment" style="margin-left:{{comment.depth|add:comment.depth}}em;"><p class="poster">Anonymous - {{comment.modified_at|naturaltime}}</p><p>{{comment.content|safe}}</p><p><a href="" class="reply">reply</a></p></li>
    {% endif %}
    {% empty %}
        No comments yet.
    {% endfor %}
    </ul>

{% endblock %}

```

