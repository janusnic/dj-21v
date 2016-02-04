# dj-21v

mysite URL Configuration
=========================
```
from django.conf.urls import include, url
from django.contrib import admin
from home import views as view_home

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [
    # Root-level redirects for common browser requests
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/compressed/favicon.ico'), name='favicon.ico'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots.txt'),
]

urlpatterns += [
    url(r'^$', view_home.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
   
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    try:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Should only occur when debug mode is on for production testing
    except ImportError as e:
        import logging
        l = logging.getLogger(__name__)
        l.warning(e)
```

Category
========
blog/views.py
--------------
```

def index(request):
    blog_list = Article.objects.order_by('-publish_date')
    category_list = Category.objects.order_by('name')
        
    context = {'categories_list':category_list, 'blog_list': blog_list }

    # context = {'blog_list': blog_list}
    
    return render(request, 'blog/index.html', context)

```

blog/index.html
----------------
```
        {% if categories_list %}       
            <ul>
                {% for category in categories_list %}
                <li>{{ category.name }}</li>
                {% endfor %}
            </ul>
        {% else %}
            <strong>There are no categories present.</strong>
        {% endif %}
```
blog/urs.py
------------
```
urlpatterns = [
```    
    url(r'^$', views.index, name='index'),

    url(r'^(?P<postslug>.*)/$', views.detail, name='detail' ),
    
    # url(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='detail_by_id'),
```

blog/views.py
------------
```
def detail(request, postslug):
    # result = Article.objects.get(slug=postslug)
    result = get_object_or_404(Article, slug=postslug)
    
    return render(request, 'blog/detail.html', {'item': result})
```
blog/index.html
---------------
```
            <h2>Publications</h2>
              {% if blog_list %}
                {% for item in blog_list %}
                  <h3><a href ="{% url 'blog:detail' item.slug %}">{{ item.title }}</a></h3>
                    <p><a class="btn btn-default" href="{% url 'blog:detail' item.slug %}" role="button">View details &raquo;</a></p>
                {% endfor %}
              {% else %}
                <li>Sorry, no items in this list.</li>
              {% endif %}
```

blog/views.html
----------------
```
def category(request, categoryslug):
    name = Category.objects.get(slug=categoryslug)
    posts = Article.objects.filter(category=name)
    context = {'blog_list': posts}
    return render(request, 'blog/singlecategory.html', context)
```

blog/singlecategory.html
-------------------------
```
{% block content %} 
      <!-- row of columns -->
      <div class="row">
        <div class="col-md-8">
          <h2>Publications</h2>
            {% if blog_list %}
                <div id="categorieslist">
                    <h2>Category {{ blog_list.0.category }}</h2>
                    {% for item in blog_list %}
                      <h3><a href ="{% url 'blog:detail' item.slug %}">{{ item.title }}</a></h3>

                        <p><a class="btn btn-default" href="{% url 'blog:detail' item.slug %}" role="button">View details &raquo;</a></p>
                    {% endfor %}
                  {% else %}
                    <li>Sorry, no items in this list.</li>
                  {% endif %}

              </div>
        </div>
        <div class="col-md-4">
          <h2>Categorits</h2>
          {% if categories_list %}       
            <ul>
                {% for category in categories_list %}
                <li>{{ category.name }}</li>
                {% endfor %}
            </ul>

            {% else %}
            <strong>There are no categories present.</strong>
          {% endif %}
       </div>

  </div>

{% endblock content %}
```

blog/urls.py
------------
```
urlpatterns = [
    url(r'^category/(?P<categoryslug>.*)/$', views.category, name='category' ),
    url(r'^(?P<postslug>.*)/$', views.detail, name='detail' ),
   
]

```
blog/views.html
----------------
```
def category(request, categoryslug):
    name = Category.objects.get(slug=categoryslug)
    posts = Article.objects.filter(category=name)
    category_list = Category.objects.order_by('name')
    context = {'categories_list':category_list, 'blog_list': posts}
    return render(request, 'blog/singlecategory.html', context)

```

blog/singlecategory.html
-------------------------
```
         <h2>Categorits</h2>
          {% if categories_list %}       
            <ul>
                {% for category in categories_list %}
                <li><a href ="{% url 'blog:category' category.slug %}">{{ category.name }}</a></li>
                {% endfor %}
            </ul>
            {% else %}
            <strong>There are no categories present.</strong>
          {% endif %}

```
blog/views.html
----------------
```
def detail(request, postslug):
    
    result = get_object_or_404(Article, slug=postslug)
    category_list = Category.objects.order_by('name')
       
    return render(request, 'blog/detail.html', {'categories_list':category_list, 'item': result})

```
blog/detail.html
-----------------
```
        <div class="col-md-4">
          <h2>Categorits</h2>
          {% if categories_list %}       
            <ul>
                {% for category in categories_list %}
                <li><a href ="{% url 'blog:category' category.slug %}">{{ category.name }}</a></li>
                {% endfor %}
            </ul>
            {% else %}
            <strong>There are no categories present.</strong>
          {% endif %}
       </div>
```
category blog/detail.html
--------------------------
```
 <h2>{{ item.title }}</h2>
          {% autoescape off %}
                <p> {{ item.content }} </p>
                {% endautoescape %}
          
          <p> {{ item.publish_date }} | <a href ="{% url 'blog:category' item.category.slug %}">{{ item.category }}</a></p>
          <p><a class="btn btn-default" href="{% url 'blog:index' %}" role="button">All publications &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>Categorits</h2>
          {% if categories_list %}       
            <ul>
                {% for category in categories_list %}
                <li><a href ="{% url 'blog:category' category.slug %}">{{ category.name }}</a></li>
                {% endfor %}
            </ul>
            {% else %}
            <strong>There are no categories present.</strong>
          {% endif %}
```

Tags
====
blog/views.py
-------------
```
def index(request):
    blog_list = Article.objects.order_by('-publish_date')
    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')
    
    context = {'categories_list':category_list, 'blog_list': blog_list , 'tags_name':tags_name}

    return render(request, 'blog/index.html', context)
```
blog/index.html
---------------
```
        <h2>Tags</h2>
          {% if tags_name %}       
            <ul>
                {% for tag in tags_name %}
                <li><a href ="">{{ tag.name }}</a></li>
                {% endfor %}
            </ul>

            {% else %}
            <strong>There are no tags present.</strong>
          {% endif %}
```

blog/detail.html
-----------------
```
        <h2>{{ item.title }}</h2>
          {% autoescape off %}
                <p> {{ item.content }} </p>
                {% endautoescape %}
          
          <p> 
              {{ item.publish_date }} | <a href ="{% url 'blog:category' item.category.slug %}">{{ item.category }}</a> | 

              {% for tag in item.tags.all %}
                    <span> {{ tag.name }} </span> 
              {% endfor %}

          </p>

```

Настройки ModelAdmin
=====================
ModelAdmin очень гибкий. Он содержит ряд параметров для настройки интерфейса администратора. Все настройки определяются в подклассе ModelAdmin:
```
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish_date'
```
## ModelAdmin.actions
Список действий, которые будут включены на странице списка объектов. 

Повседневный алгоритм работы с административным интерфейсом Django выглядит как “выделить объект, затем изменить его.” Он подходит для большинства случаев. Тем не менее, когда потребуется выполнить одно и то же действие над множеством объектов.

В таких случаях административный интерфейс Django позволяет вам создать и зарегистрировать “действия” – простые функции, которые вызываются для выполнения неких действий над списком объектов, выделенных на странице интерфейса.

Если вы взгляните на любой список изменений на интерфейсе администратора, вы увидите эту возможность в действии. Django поставляется с действием “удалить выделенные объекты”, которое доступно для всех моделей. 

Создание действий
==================
Общим способом использования действий в интерфейсе администратора является пакетное изменение модели. 

Приложение для работы с новостями, которое обладает моделью Article:
```
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
    tags = models.ManyToManyField(Tag, verbose_name="the related tags", blank=True)
        
    publish_date = models.DateTimeField(auto_now=True, editable=False, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    created_date = models.DateTimeField(auto_now_add=True, editable=False)

    def was_published_recently(self):
        return self.publish_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return '%s' % (self.title)

```

Стандартной задачей, которую мы возможно будем выполнять с подобной моделью, будет изменение состояний статьи с “черновик” на “опубликовано”. Мы легко сможем выполнить это действие в интерфейсе администратора для одной статьи за раз, но если потребуется выполнить массовую публикацию группы статей, то вы столкнётесь с нудной работой. Таким образом, следует написать действие, которое позволит нам изменять состояние статьи на “опубликовано.”

## Создание функций для действий
Сначала нам потребуется написать функцию, которая вызывается при выполнении действия в интерфейсе администратора. Функции действий - это обычные функции, которые принимают три аргумента:

- Экземпляр класса ModelAdmin,
- Экземпляр класса HttpRequest, представляющий текущий запрос,
- Экземпляр класса QuerySet, содержащий набор объектов, которые выделил пользователь.

Наша функция “опубликовать-эти-статьи” не нуждается в экземпляре ModelAdmin или в объекте реквеста, но использует выборку:
```
def make_published(modeladmin, request, queryset):
    queryset.update(status=PUBLISHED)

```
В целях улучшения производительности, мы используем метод выборки update method. Другие типы действий могут обрабатывать каждый объект индивидуально. В таких случаях мы просто выполняем итерацию по выборке:
```
for obj in queryset:
    do_something_with(obj)
```

Обеспечим действие “красивым” заголовком, который будет отображаться в интерфейсе администратора. По умолчанию, это действие будет отображено в списке действий как “Make published”, т.е. по имени функции, где символы подчёркивания будут заменены пробелами. 

make_published атрибут short_description:
```
def make_published(modeladmin, request, queryset):
    queryset.update(status=PUBLISHED)
make_published.short_description = "Mark selected stories as published"

```

Добавление действий в класс ModelAdmin
---------------------------------------
Затем мы должны проинформировать наш класс ModelAdmin о новом действии. Это действие аналогично применению любой другой опции конфигурации. Таким образом, полный пример admin.py с определением действия и его регистрации будет выглядеть так:

```
def make_published(modeladmin, request, queryset):
    queryset.update(status=PUBLISHED)
make_published.short_description = "Mark selected stories as published"

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['publish_date']

    filter_horizontal = ('tags',)

    prepopulated_fields = {"slug": ("title",)}

    date_hierarchy = 'publish_date'
    readonly_fields = ('publish_date','created_date')
    fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('publish_date','created_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status')]}),
    ]

    actions = [make_published,]

admin.site.register(Article, ArticleAdmin)
```
Обработка ошибок в действиях
-----------------------------
При наличии предполагаемых условий возникновения ошибки, которая может возникнуть во время работы вашего действия, вы должны аккуратно проинформировать пользователя о проблеме. Это подразумевает обработку исключений и использование метода django.contrib.admin.ModelAdmin.message_user() для отображения описания проблемы в отклике.

Действия как методы ModelAdmin
------------------------------
так как действия связано с объектом Article, то правильнее будет внедрить это действие в сам объект ArticleAdmin.
```
class ArticleAdmin(admin.ModelAdmin):
    ...

    actions = [make_published, 'make_draft']

    def make_draft(self, request, queryset):
        queryset.update(status=DRAFT)
    make_draft.short_description = "Mark selected stories as draft"
```
это указывает классу ModelAdmin искать действие среди своих методов.

Определение действий в виде методов предоставляет действиям более прямолинейный, идеоматический доступ к самому объекту ModelAdmin, позволяя вызывать любой метод, предоставляемый интерфейсом администратора.

мы можем использовать self для вывода сообщения для пользователя в целях его информирования об успешном завершении действия:
```
class ArticleAdmin(admin.ModelAdmin):
    ...

    def make_expired(self, request, queryset):
        rows_updated = queryset.update(status=EXPIRED)
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as expired." % message_bit)
    make_expired.short_description = "Mark selected stories as expired"

```
Это обеспечивает действие функционалом, аналогичным встроенным возможностям интерфейса администратора

Отключение действий
--------------------
Иногда требуется отключать определённые действия, особенно зарегистрированные глобально, для определённых объектов. Существует несколько способов для этого:

Отключение глобального действия
--------------------------------
#### AdminSite.disable_action(name)
Если требуется отключить глобальное действие, вы можете вызвать метод AdminSite.disable_action().

Например, вы можете использовать данный метод для удаления встроенного действия “delete selected objects”:
```
admin.site.disable_action('delete_selected')
```
После этого действие больше не будет доступно глобально.

Тем не менее, если вам потребуется вернуть глобально отключенное действия для одной конкретной модели, просто укажите это действия явно в списке ModelAdmin.actions:

```
# Globally disable delete selected
admin.site.disable_action('delete_selected')

# This ModelAdmin will not have delete_selected available
class SomeModelAdmin(admin.ModelAdmin):
    actions = ['some_other_action']
    ...

# This one will
class AnotherModelAdmin(admin.ModelAdmin):
    actions = ['delete_selected', 'a_third_action']
    ...
```
Отключение всех действия для определённого экземпляра ModelAdmin
-----------------------------------------------------------------
Если вам требуется запретить пакетные действия для определённого экземпляра ModelAdmin, просто установите атрибут ModelAdmin.actions в None:
```
class MyModelAdmin(admin.ModelAdmin):
    actions = None
```
Это укажет экземпляру ModelAdmin не показывать и не позволять выполнения никаких действий, включая зарегистрированные глобально.

Условное включение и отключение действий
----------------------------------------
### ModelAdmin.get_actions(request)
Наконец, вы можете включать или отключать действия по некоему условию на уровне запроса (и, следовательно, на уровне каждого пользователя), просто переопределив метод ModelAdmin.get_actions().

Он возвращает словарь разрешённых действий. Ключами являются имена действий, а значениями являются кортежи вида (function, name, short_description).

Чаще всего вы будете использовать данный метод для условного удаления действия из списка, полученного в родительском классе. Например, если мне надо разрешить пакетное удаление объектов только для пользователей с именами, начинающимися с буквы ‘J’, то я сделаю так:
```
class MyModelAdmin(admin.ModelAdmin):
    ...

    def get_actions(self, request):
        actions = super(MyModelAdmin, self).get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

```
Действие “удалить выделенные объекты” использует метод QuerySet.delete() по соображениям эффективности, который имеет важный недостаток: метод delete() вашей модели не будет вызван.

Если вам потребуется изменить такое поведение, то просто напишите собственное действие, которое выполняет удаление в необходимой вам манере, например, вызывая Model.delete() для каждого выделенного элемента.

### ModelAdmin.actions_on_top
### ModelAdmin.actions_on_bottom
Определяет где на странице будет расположены панели с действиями. По умолчанию эта панель расположена сверху (actions_on_top = True; actions_on_bottom = False).

### ModelAdmin.actions_selection_counter
Указывает отображать ли счетчик выбранных объектов после списка действий. По умолчанию он отображается (actions_selection_counter = True).

### ModelAdmin.date_hierarchy
Укажите в date_hierarchy название DateField или DateTimeField поля вашей модели, и страница списка объектов будет содержать навигацию по датам из этого поля.
```
date_hierarchy = 'publish_date'
```
Навигация учитывает значения поля, например, если все значения будут датами из одного месяца, будут отображаться только дни этого месяца.

date_hierarchy использует внутри QuerySet.datetimes() (USE_TZ = True).

## ModelAdmin.formfield_overrides
Позволяет быстро изменить настройки отображения различных типов Field в интерфейсе администратора. formfield_overrides – словарь указывающий параметры для классов полей, которые будут передаваться в конструкторы указанных полей.

Install django-wysiwyg-redactor:
================================
https://github.com/douglasmiranda/django-wysiwyg-redactor

```
pip install django-wysiwyg-redactor

```
settings.py
-----------
```
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'redactor',

    'blog',
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/media')
MEDIA_URL = '/media/'

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = MEDIA_ROOT
```
urls.py
```
urlpatterns = [

    url(r'^redactor/', include('redactor.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
]

```
Pillow
------
```
pip install Pillow
```
admin.py
---------
```
class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': RedactorEditor(),
        }
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['title']

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('created_date','publish_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status','views_count')]}),
        ('Comments',            {'fields': ['enable_comment','comment_count']}),
    ]
    actions = [make_published,'make_draft','make_expired']

    actions_on_top = True 
    actions_on_bottom = False 
    actions_selection_counter = True

    date_hierarchy = 'publish_date'

    filter_horizontal = ('tags',)

    form = ArticleAdminForm

```

CKEDITOR
=========
settings.py
-----------
```
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YouCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'youcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YouCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join(
            [
                # you extra plugins here
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                # 'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath'
            ]),
    }
}

```
admin.py
--------
```
from ckeditor.widgets import CKEditorWidget

class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Article
        fields = '__all__'
        
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['publish_date']

    filter_horizontal = ('tags',)

    prepopulated_fields = {"slug": ("title",)}

    date_hierarchy = 'publish_date'
    readonly_fields = ('publish_date','created_date')
    fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('publish_date','created_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status')]}),
    ]

    actions = [make_published,'make_draft','make_expired']

    form = ArticleAdminForm
```

tinymce
========
urls.py
-------
```
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),

    url(r'^tinymce/', include('tinymce.urls')),
]

```
models.py:
```
from django.db import models
from tinymce.models import HTMLField

class MyModel(models.Model):
    ...
    content = HTMLField()
```

settings.py
-----------
```
# tinymce
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'plugins': "wordcount,preview,emotions,preview,spellchecker,",
    'height': "400px",
    'width': "700px",
    'theme_advanced_buttons3' : "fontselect,fontsizeselect,emotions,preview,",
    }
```
autoescape
-----------
```
<p><strong>В этом примере к начальному QuerySet</strong>, который возвращает все объекты, добавляется фильтр, затем исключающий фильтр, и еще один фильтр. Полученный <em>QuerySet</em> содержит все объекты, у которых заголовок начинается с <em>QuerySet</em>, и которые были опубликованы между 3-го января 2016 и текущей датой.</p><p><img src="/home/janus/github/dj-21v/unit_06/mysite/public/media/loshadka.png"></p><p>Отфильтрованный QuerySet – уникален</p><hr><pre>После каждого изменения QuerySet, вы получаете новый QuerySet, который никак не связан с предыдущим QuerySet. Каждый раз создается отдельный QuerySet, который может быть сохранен и использован.</pre> 
```

autoescape off
--------------
```
            {% autoescape off %}
                <p> {{ item.content }} </p>
            {% endautoescape %}
```
