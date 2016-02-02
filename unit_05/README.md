# dj-21v
методы модели
=============
__unicode__
------------

Метод __unicode__() вызывается когда вы применяете функцию unicode() к объекту. Django использует unicode(obj) (или функцию str(obj)) в нескольких местах. В частности, для отображения объектов в интерфейсе администратора Django и в качестве значения, вставляемого в шаблон, при отображении объекта. 

models.py:
-----------
```
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=4096)

    def __unicode__(self):
        return u'%s' % (self.name)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=0)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.title)

```
Если вы определили метод __unicode__() и не определили __str__(), Django самостоятельно добавит метод __str__() который вызывает __unicode__(), затем преобразует результат в строку в кодировке UTF-8. Это рекомендуемый подход: определить только __unicode__() и позволить Django самостоятельно преобразовать в строку при необходимости.

__str__
--------

Метод __str__() вызывается когда вы применяете функцию str() к объекту. В Python 3 Django использует str(obj) в нескольких местах. В частности, для отображения объектов в интерфейсе администратора Django и в качестве значения, вставляемого в шаблон, при отображении объекта. 

models.py:
-----------
```
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=4096)

    def __str__(self):
        return '%s' % (self.name)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return '%s' % (self.name)

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=0)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.title)

```

В Python 2 Django использует __str__, если нужно вывести результат функции repr(). Определять метод __str__() не обязательно, если вы определили метод __unicode__().

метод __unicode__() может аналогично использоваться и в __str__():
```
from django.db import models
from django.utils.encoding import force_bytes

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=0)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return force_bytes('%s' % (self.title))
```        

В Python 3, так как все строки являются Unicode строками, используйте только метод __str__(). Если вам необходима совместимость с Python 2, Можете декорировать ваш класс модели декоратором python_2_unicode_compatible().

django.utils.encoding
======================
python_2_unicode_compatible()
------------------------------
```
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    status = models.IntegerField(default=0)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.title)

```

choices
---------
Итератор (например, список или кортеж) 2-х элементных кортежей, определяющих варианты значений для поля. При определении, виджет формы использует select вместо стандартного текстового поля и ограничит значение поля указанными значениями.

Список значений выглядит:
-------------------------
```
ARTICLE_STATUS = (
    ('DRAFT', 'Not Reviewed'),
    ('PUBLISHED', 'Published'),
    ('EXPIRED', 'Expired'),
)


```
Первый элемент в кортеже - значение хранимое в базе данных, второй элемент - отображается виджетом формы, или в ModelChoiceField. Для получения отображаемого значения используется метод get_status_display экземпляра модели. Значения лучше указать в константах внутри модели:
```
from django.db import models

class Article(models.Model):
    ARTICLE_STATUS = (
        ('D', 'Not Reviewed'),
        ('P', 'Published'),
        ('E', 'Expired'),
    )


    name = models.CharField(max_length=60)
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default='D')
    p = Article(name="Fred Flintstone", status="D")
    p.save()
    p.status

    p.get_status_display()

```
Значение по умолчанию для этого поля. 
-------------------------------------
Это может быть значение или функция. Если это функция - она будет вызвана при каждом создании объекта.
```
class Article(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    EXPIRED ='E'
    ARTICLE_STATUS = (
        (DRAFT, 'Not Reviewed'),
        (PUBLISHED, 'Published'),
        (EXPIRED, 'Expired'),
    )
    title = models.CharField(max_length=100, unique=True)
        
    status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default=DRAFT)
    
```

help_text
---------
```
    publish_date = models.DateTimeField(auto_now=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
```

SlugField
----------
```
class SlugField([max_length=50, **options])
```
Slug – газетный термин. “Slug” – это короткое название-метка, которое содержит только буквы, числа, подчеркивание или дефис. В основном используются в URL.

Как и для CharField, можно указать max_length. Если max_length не указан, Django будет использовать значение 50.

Устанавливает Field.db_index в True, если аргумент явно не указан.

Обычно значение SlugField создается на основе какого-то другого значения(например, название статьи). Это может работать автоматически в интерфейсе администрации благодаря параметру prepopulated_fields.

Полученные запросы зависят от базы данных, которую вы используете. 

Названия таблиц созданы автоматически из названия приложения(blog) и названия модели в нижнем регистре – category, tag и article. (Вы можете переопределить это.)

Первичные ключи (ID) добавлены автоматически. (Вы можете переопределить и это.)

Django добавляет "_id" к названию внешнего ключа. (вы можете переопределить это.)

Учитываются особенности базы данных, которую вы используете. Специфические типы данных такие как auto_increment (MySQL), serial (PostgreSQL), или integer primary key (SQLite) будут использоваться автоматически. Тоже касается и экранирование названий, что позволяет использовать в названии кавычки – например, использование одинарных или двойных кавычек.
Вставляем в нашу модель поле:
-----------------------------
```
slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
```
models.py
---------
```
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    
    description = models.TextField(max_length=4096)
        
    def __str__(self):
        return self.name

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
    
    publish_date = models.DateTimeField(auto_now=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.title)

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')

    def __str__(self):
        return '%s' % (self.name)
```
Параметр unique=True отвечает за то, чтоб название было уникальным.
--------------------------------------------------------------------
## Подключение к админке. 

### ModelAdmin.prepopulated_fields

Обычно значение SlugField создается на основе какого-то другого значения(например, название статьи). Это может работать автоматически в интерфейсе администрации благодаря параметру prepopulated_fields.

prepopulated_fields 
-------------------
позволяет определить поля, которые получают значение основываясь на значениях других полей:
```
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
```
Указанные поля будут использовать код JavaScript для заполнения поля значением на основе значений полей-источников. Основное применение - это генерировать значение для полей SlugField из значений другого поля или полей. Процесс генерирования состоит в объединении значений полей-источников и преобразованию результата в правильный “slug” (например, заменой пробелов на дефисы).

prepopulated_fields не принимает поля DateTimeField, ForeignKey или ManyToManyField.

# Настройки ModelAdmin
ModelAdmin очень гибкий. Он содержит ряд параметров для настройки интерфейса администратора. Все настройки определяются в подклассе ModelAdmin:
```
from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'publish_date'
```
admin.py:
---------
```
cfrom django.contrib import admin

from .models import Category, Tag, Article

class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')
    list_display_links = ('name',)
    search_fields = ['name', 'slug', 'description']

    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status')
    list_filter = ['publish_date']
    search_fields = ['title']

    ordering = ['publish_date']

    prepopulated_fields = {"slug": ("title",)}

    date_hierarchy = 'publish_date'

admin.site.register(Article, ArticleAdmin)

```
Не забудьте сделать миграцию. 

manage.py check
----------------
Эта команда ищет проблемы в вашем проекте не применяя миграции и не изменяя базу данных.

Команда migrate выполняет все миграции, которые ещё не выполнялись, (Django следит за всеми миграциями, используя таблицу в базе данных django_migrations) и применяет изменения к базе данных, синхронизируя структуру базы данных со структурой ваших моделей.

Миграции - позволяют изменять ваши модели в процессе развития проекта без необходимости пересоздавать таблицы в базе данных. Их задача изменять базу данных без потери данных. 

1. Внесите изменения в модели (в models.py).
2. Выполните python manage.py makemigrations чтобы создать миграцию для ваших изменений
3. Выполните python manage.py migrate чтобы применить изменения к базе данных.

Две команды необходимы для того, чтобы хранить миграции в системе контроля версий. Они не только помогают вам, но и могут использоваться другими программистами вашего проекта.

API для доступа к данным 
-------------------------

Django не делает первую букву прописной для verbose_name - только там, где это необходимо.
ForeignKey, ManyToManyField и OneToOneField
-------------------------------------------
первым аргументом принимает класс модели, поэтому используется keyword аргумент verbose_name

связь между моделями определяется с помощью ForeignKey.  Django поддерживает все основные типы связей: многие-к-одному, многие-ко-многим и один-к-одному.

Поля отношений
===============
Django предоставляет набор полей для определения связей между моделями.

ForeignKey
-----------
```
class ForeignKey(othermodel[, **options])
```
Связь многое-к-одному. Принимает позиционный аргумент: класс связанной модели.

Для создания рекурсивной связи – объект со связью многое-к-одному на себя – используйте models.ForeignKey('self').

Если вам необходимо добавить связь на модель, которая еще не определена, вы можете использовать имя модели вместо класса:
```
from django.db import models

class Article(models.Model):
    user = models.ForeignKey('User')
    # ...

class User(models.Model):
    # ...
    pass
```
Для связи на модель из другого приложения используйте название модели и приложения. Например, если модель User находится в приложении auth, используйте:
```
class Article(models.Model):
    user = models.ForeignKey('auth.User')
```    
Такой способ позволяет создать циклическую зависимость между моделями из разных приложений.

В базе данных автоматом создается индекс для ForeignKey. Можно указать для db_index False, чтобы отключить такое поведение. Это может пригодиться, если внешний ключ используется для согласованности данных, а не объединения(join) в запросах, или вы хотите самостоятельно создать альтернативный индекс или индекс на несколько колонок.

Не рекомендуется использовать ForeignKey из приложения без миграций к приложению с миграциями. 

## Представление в базе данных
Django добавляет "_id" к названию поля для создания названия колонки. 

### ForeignKey.related_name
Название, используемое для обратной связи от связанной модели. Также значение по умолчанию для related_query_name (название обратной связи используемое при фильтрации результата запроса). 

Если вы не хотите, чтобы Django создавал обратную связь, установите related_name в '+' или добавьте в конце '+'. Например, такой код создаст связь, но не добавит обратную связь в модель Category:
```
category = models.ForeignKey(Category, verbose_name="the related category", related_name='+')
```
ForeignKey.related_query_name
-----------------------------
Название обратной связи используемое при фильтрации результата запроса. По умолчанию используется related_name, или название модели:
```
# Declare the ForeignKey with related_query_name
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='slug')
    article = models.ForeignKey(Article, related_name="tags", related_query_name="tag")

    def __str__(self):
        return '%s' % (self.name)

# That's now the name of the reverse filter
Article.objects.filter(tag__name="django")
```
## ForeignKey.to_field
Поле связанной модели, которое используется для создания связи между таблицами. По-умолчанию, Django использует первичный ключ.

## ForeignKey.db_constraint
Указывает создавать ли “constraint” для внешнего ключа в базе данных. По умолчанию True и в большинстве случает это то, что вам нужно. Указав False вы рискуете целостностью данных. Некоторые ситуации, когда вам может быть это необходимо:

- Вам досталась в наследство нецелостная база данных
- Вы используете шардинг базы данных.

При False, если связанный объект не существует, при обращении к нему будет вызвано исключение DoesNotExist.

## ForeignKey.on_delete
Когда объект, на который ссылается ForeignKey, удаляется, Django по-умолчанию повторяет поведение ограничения ON DELETE CASCADE в SQL и удаляет объекты, содержащие ForeignKey. Такое поведение может быть переопределено параметром on_delete. Например, если ваше поле ForeignKey может содержать NULL и вы хотите, чтобы оно устанавливалось в NULL после удаления связанного объекта:
```
category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
```
Возможные значения для on_delete находятся в django.db.models:

- CASCADE
Каскадное удаление, значение по умолчанию.

- PROTECT
Препятствует удалению связанного объекта вызывая исключение django.db.models.ProtectedError`(подкласс :exc:`django.db.IntegrityError).

- SET_NULL
Устанавливает ForeignKey в NULL; возможно только если null равен True.

- SET_DEFAULT
Устанавливает ForeignKey в значение по умолчанию; значение по-умолчанию должно быть указано для ForeignKey.

- SET()
Устанавливает ForeignKey в значение указанное в SET(). Если указан выполняемый объект, результат его выполнения. Вызываемый объект можно использовать, чтобы избежать запросов во время импорта 

- DO_NOTHING
Ничего не делать. Если используемый тип базы данных следит за целостностью связей, будет вызвано исключение IntegrityError, за исключением, когда вы самостоятельно добавите SQL правило ON DELETE для поля таблицы (возможно используя загрузочный sql).

## ManyToManyField
class ManyToManyField(othermodel[, **options])

Связь многие-ко-многим. Принимает позиционный аргумент: класс связанной модели. Работает так же как и ForeignKey, включая рекурсивную и ленивую связь.

Связанные объекты могут быть добавлены, удалены или созданы с помощью RelatedManager.

Не рекомендуется использовать ManyToManyField из приложения без миграций к приложению с миграциями.

### Представление в базе данных
Django самостоятельно создаст промежуточную таблицу для хранения связи многое-ко-многим. По-умолчанию, название этой таблицы создается из названия поля и связанной модели. Так как некоторые базы данных не поддерживают длинные названия таблиц, оно будет обрезано до 64 символов и будет добавлен уникальный хеш. Это означает что вы можете увидеть такие названия таблиц author_books_9cdf4; это нормально. Вы можете указать название промежуточной таблицы, используя параметр db_table.

## Параметры
ManyToManyField принимает дополнительные аргументы – все не обязательны – которые определяют как должна работать связь.

- ManyToManyField.related_name
Аналогично ForeignKey.related_name.

- ManyToManyField.related_query_name
Аналогично ForeignKey.related_query_name.

- ManyToManyField.limit_choices_to
Аналогично ForeignKey.limit_choices_to.

- limit_choices_to``не работает для ``ManyToManyField переопределенной через through промежуточной моделью.

## ManyToManyField.symmetrical
Используется только при рекурсивной связи.

## ManyToManyField.through
Django автоматически создает промежуточную таблицу для хранения связи. Однако, если вы хотите самостоятельно определить промежуточную таблицу, используйте параметр through указав модель Django, которая будет хранить связь между моделями.

Обычно используют для хранения дополнительных данных.

Если вы не указали through модель, вы все равно может обратиться к неявно промежуточной модели, которая была автоматически создана. Она содержит три поля, связывающие модели.

Если связанные модели разные, создаются следующие поля:
```
id: первичный ключ для связи.

<containing_model>_id: id модели, которая содержит поле ManyToManyField.

<other_model>_id: id модели, на которую ссылается ManyToManyField.
```
Если ManyToManyField ссылается на одну и ту же модель, будут созданы поля:
```
id: первичный ключ для связи.

from_<model>_id: id объекта основной модели (исходный объект).

to_<model>_id: id объекта, на который указывает связь (целевой объект).
```
Этот класс может использоваться для получения связей.

## ManyToManyField.db_table
Имя промежуточной таблицы для хранения связей многое-ко-многим. Если не указан, Django самостоятельно создаст название по умолчанию используя название таблицы определяющей связь и название поля.

## ManyToManyField.db_constraint
Указывает создавать ли “constraint” для внешних ключей в промежуточной таблице в базе данных. По умолчанию True и в большинстве случает это то, что вам нужно. Указав False вы рискуете целостностью данных. Некоторые ситуации, когда вам может быть это необходимо:

- Вам досталась в наследство нецелостная база данных

- Вы используете шардинг базы данных.

Нельзя указать db_constraint и through одновременно.

## ManyToManyField.swappable

Управляет поведением миграций, если ManyToManyField ссылается на подменяемую(swappable) модель. При True - значение по умолчанию - если ManyToManyField ссылается на модель, указанную через settings.AUTH_USER_MODEL (или другую настройку, определяющую какую модель использовать), связь в миграции будет использовать настройку, а не саму модель.

Вам может понадобится значение False только, если связь должна указывать на какую-то конкретную модель, игнорируя настройку - например, если это модель профиля пользователя для какой-то конкретной модели пользователя и не будет работать с любой моделью из настройки.

Если вы не уверены какое значение выбрать, используйте значение по умолчанию True.

## ManyToManyField.allow_unsaved_instance_assignment

Работает аналогично ForeignKey.allow_unsaved_instance_assignment.

ManyToManyField не поддерживает validators.

null не влияет на работу поля т.к. нет способа сделать связь обязательной на уровне базы данных.

Admin
=====
## Добавим приложение blog в интерфейс администратора

blog/admin.py
```
from django.contrib import admin
from .models import Category

admin.site.register(Category)
```

Поля формы формируются на основе описания модели Category.

```
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='name')
    
    description = models.TextField(max_length=4096)

    def __unicode__(self):
        return self.name

```
Для различных типов полей модели (TextField, CharField, IntegerField) используются соответствующие HTML поля. Каждое поле знает как отобразить себя в интерфейсе администратора.

```
from django.contrib import admin

# Register your models here.
from .models import Category, Tag, Article

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)
```

При использовании auto_now или auto_now_add со значением True будут установлены параметры editable=False и blank=True.

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
        
    publish_date = models.DateTimeField(auto_now=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.title)
```

К полям DateTimeField добавлен JavaScript виджет. Для даты добавлена кнопка “Сегодня” и календарь, для времени добавлена кнопка “Сейчас” и список распространенных значений.

Если значение “Publish date” не совпадает с временем создания объекта, возможно, вы неверно определили настройку TIME_ZONE. Измените ее и перезагрузите страницу.

Измените “Publish date”, нажав “Today” и “Now”. Затем нажмите “Save and continue editing.” Теперь нажмите “History” в правом верхнем углу страницы. Вы увидите все изменения объекта, сделанные через интерфейс администратора, время изменений и пользователя, который их сделал:

Please use the following format: YYYY-MM-DD.
```
publish_date = models.DateTimeField(auto_now=False, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
```
ModelAdmin.fields
==================
Если вам необходимо внести небольшие изменения форму на странице редактирования и добавления, например, изменить список отображаемых полей, их порядок или сгруппировать их, вы можете использовать настройку fields (сложные изменения можно выполнить используя настройку fieldsets). 

После регистрации модели Article, используя admin.site.register(Article), Django создал форму для модели. 

порядок полей в форме. 
----------------------
```
'title','status','enable_comment','content','category','tags','publish_date','created_date','views_count','comment_count'
```
Замените admin.site.register(Article) на:

blog/admin.py
```
from django.contrib import admin

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    fields = ['title','category','content','created_date','publish_date','tags','status','enable_comment','views_count','comment_count']

admin.site.register(Article, ArticleAdmin)
```
Создаем объект ModelAdmin и предаем его в admin.site.register().

Теперь поле “Publication date” отображается перед полем “Tag”:

fields может содержать поля указанные в ModelAdmin.readonly_fields, они не будут доступны для редактирования.

Параметр fields, в отличии от list_display, может содержать только названия полей модели или полей определенных в form. Можно указать названия функций, если они указаны в readonly_fields.

Чтобы поля отображались в одной строке, укажите их в кортеже вместе.
```
fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('created_date','publish_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status','views_count')]}),
        
    ]
```
blog/admin.py
```
from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status')

    ordering = ['publish_date']
    prepopulated_fields = {"slug": ("title",)}

    date_hierarchy = 'publish_date'
    readonly_fields = ('publish_date','created_date')
    fieldsets = [
        ('Item',             {'fields': [('title','slug'),'category','content']}),
        ('Date information', {'fields': [('publish_date','created_date')], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': [('status')]}),
    ]

admin.site.register(Article, ArticleAdmin)
```
Первый элемент кортежа в fieldsets – название группы полей.

Если не определен ни атрибут fields, ни fieldsets, Django покажет все поля с editable=True кроме AutoField, в одном наборе полей в порядке, в котором они указанные в модели.

Словарь field_options может содержать следующие ключи:
-------------------------------------------------------
- fields
Кортеж с названиями полей. Этот ключ обязателен.

```
{'fields': [('title','slug'),'category','content']}
```
Как и в атрибуте fields, чтобы отобразить поля в одной строке, добавьте их в один кортеж. В этом примере, поля title и slug будут показаны в одной строке

fields может содержать значения из ModelAdmin.readonly_fields, чтобы отображать поля без возможности их редактирования.

Добавление функции в fields аналогично добавлению в параметр fields - функция должна быть указанна в readonly_fields.
- classes
Список содержащий CSS классы, которые будут добавлены в группу полей.
```
{
'classes': ('wide', 'extrapretty'),
}
```
Django предоставляет два класса для использования: collapse и wide. Группа полей с классом collapse будет показа в свернутом виде с кнопкой “развернуть”. Группа полей с классом wide будет шире по горизонтали.

- description
Необязательный текст, который будет отображаться под названием группы полей. Этот текст не отображается для TabularInline.

текст не будет экранирован. Это позволяет добавить HTML на страницу.

добавить HTML классы для каждой группы полей. 
---------------------------------------------
класс "collapse", который отображает группу полей изначально скрытой. Это полезно, если форма содержит поля, которые редко редактируются:

blog/admin.py
```
from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Item',             {'fields': ['title','category','content']}),
        ('Date information', {'fields': ['created_date','publish_date'], 'classes': ['collapse']}),
        ('Related tags',     {'fields': ['tags']}),
        ('Metas',            {'fields': ['status']}),
    ]

admin.site.register(Article, ArticleAdmin)

```
### ModelAdmin.list_display_links
Используйте list_display_links, чтобы указать какие поля в list_display будут ссылками на страницу редактирования объекта.

По умолчанию, на страницу редактирования объекта будет вести ссылка в первой колонке – первое поле в list_display. Но list_display_links позволяет изменить это поведение:

Можно указать None, чтобы убрать ссылки.

Укажите список или кортеж полей (так же как и в list_display) чьи колонки должны быть ссылками на страницу редактирования.

Вы можете указывать одно или несколько полей. Пока указанные поля входят в list_display, Django безразлично сколько их. Единственное требование: для использования list_display_links вы должны указать list_display.

```
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('views_count',)
    list_display = ('name', 'slug')
    list_display_links = ('name',)
```
В этом примере список объектов будет без ссылок:
```
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('views_count',)
    list_display = ('name', 'slug')

    list_display_links = None

```
## ModelAdmin.readonly_fields
По умолчанию интерфейс администратора отображает все поля как редактируемые. Поля указанные в этой настройке (которая является list или tuple) будут отображаться значение без возможности редактировать, они также будут исключены из ModelForm используемой для создания и редактирования объектов. Однако, если вы определяете аргумент ModelAdmin.fields или ModelAdmin.fieldsets поля для чтения должны быть в них указаны (иначе они будут проигнорированы).

Если readonly_fields используется без определения порядка полей через атрибуты ModelAdmin.fields или ModelAdmin.fieldsets, поля из этой настройки будут отображаться после редактируемых полей.

```
readonly_fields = ('views_count', 'comment_count')
```
Добавление связанных объектов
=============================
```
from .models import Category, Tag, Article

admin.site.register(Category)
admin.site.register(Tag)
```

Django знает, что поле ForeignKey должно быть представлено как select. 

Обратите внимание на ссылку “Add Another category” возле поля Category. При нажатии на “Add Another category” будет показано всплывающее окно с формой добавления category. 

Настройка страницы списка объектов
----------------------------------
По умолчанию Django отображает результат выполнения str() для каждого объекта. Но чаще всего хочется показывать список полей. Для этого используйте параметр list_display, который является кортежем состоящим из названий полей модели:

blog/admin.py
```
class ArticleAdmin(admin.ModelAdmin):

    # ...
    list_display = ('title', 'publish_date', 'status')
```

добавим метод was_published_recently:
-------------------------------------
blog/admin.py
```
class ArticleAdmin(admin.ModelAdmin):
    # ...
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
```

Вы можете нажать на заголовок колонки чтобы отсортировать записи по полю – но не для was_published_recently, так как сортировка по методу не поддерживается. Название колонки для was_published_recently по умолчанию равно названию метода (нижние подчеркивание заменяется на пробелы), а значение равно строковому представлению результата выполнения метода.

blog/models.py
```
from django.db import models
import datetime
from django.utils import timezone

class Article(models.Model):
    # ...
    def was_published_recently(self):
        return self.publish_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'publish_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
```

ModelAdmin.list_filter
======================
Укажите list_filter, чтобы определить фильтры данных в правой панели страницы списка объектов

list_filter - это список элементов, которые могу быть одного из следующих типов:
--------------------------------------------------------------------------------
- название поля следующего типа: BooleanField, CharField, DateField, DateTimeField, IntegerField, ForeignKey или ManyToManyField.:

```
list_filter = ['publish_date']
```
Это добавляет “Фильтр” по полю publish_date в боковой панели

Тип фильтра зависит от типа поля. Так как publish_date является DateTimeField, Django отображает соответствующие варианты для фильтрации: “Any date,” “Today,” “Past 7 days,” “This month,” “This year.”

Поле в list_filter может указывать и на связанный объект используя __, например:
```
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'status', 'was_published_recently')
   
    list_filter = ['publish_date']
  
```
добавим поиск:
--------------
```
search_fields = ['title']
```
Это добавляет поле для поиска в верхней части страницы. При вводе запроса, Django будет искать по полю title. Вы можете использовать любое количество полей – учтите что используется запрос LIKE, так что постарайтесь не перегрузить вашу базу данных.

Страница списка объектов также содержит постраничное отображение. По умолчанию отображается 100 объектов на страницу. Поменять количество объектов на одной странице, поля для поиска, фильтры, добавить иерархию по дате и отображаемые поля - все это возможно.

## ModelAdmin.filter_horizontal
По умолчанию, поле ManyToManyField отображается как select multiple. Однако, это поле тяжело использовать при большом количестве объектов. Добавив ManyToManyField в этот атрибут, будет использоваться “виджет” с JavaScript фильтром для поиска. 
```
filter_horizontal = ('tags',)

```
### ModelAdmin.filter_vertical
Аналогичен filter_horizontal, но использует вертикальный “виджет”.

Обработчики ошибок
===================
Если Django не может найти подходящий шаблон URL, или было вызвано исключение в процессе обработки запроса, Django вызовет соответствующее представление обрабатывающее ошибку.

Эти представления определены в четырёх переменных. Их значения по-умолчанию должны подойти для большинства проектов, но вы можете их поменять при необходимости.

Эти значения должны быть определены в главном URLconf.

Значение это функции, или полный путь для импорта, которая будет вызвана, если не был найден подходящий URL-шаблон.

Функция get_object_or_404()
----------------------------

Одна из распространенных идиом – вызвать метод get() и возбудить исключение Http404, если объект не существует. Она инкапсулирована в функции get_object_or_404(), которая принимает в первом аргументе модель Django, а также произвольное количество именованных аргументов, которые передает функции get() менеджера, подразумеваемого по умолчанию. Если объект не существует, функция возбуждает исключение Http404. 
Например:

Получить объект Article с первичным ключом 3 
```
е = get_object_or_404(Article, pk=3)
```
Когда этой функции передается модель, для выполнения запроса get() она использует менеджер, подразумеваемый по умолчанию. Если вас это не устраивает или вы хотите произвести поиск в списке связанных объектов, то можно передать функции get_object_or_404() нужный объект Manager:

Получить categories записи е в блоге по имени ’Python’ 
```
а = get_object_or_404(e.caterories, name=’Python’)
```
Воспользоваться нестандартным менеджером ‘recent_entries’ для поиска записи с первичным ключом 3 е = get_object_or_404(Article.recent_entries, pk=3)

Функция getjist_or_404()
------------------------
Эта функция ведет себя так же, как get_object_or_404(), но вместо get() вызывает filter(). Если возвращается пустой список, она возбуждает исключение Http404.

blog/views.py:
--------------
```
def detail(request, blog_id):
    try:
        item = Article.objects.get(pk=blog_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'blog/detail.html', {'item': item})
```
blog/views.py:
--------------
```
from django.shortcuts import get_object_or_404, render

def detail(request, blog_id):
    item = get_object_or_404(Article, pk=blog_id)
    return render(request, 'blog/detail.html', {'item': item})

```
Именованные группы
===================
Для регулярных выражений в Python синтаксис для именованных совпадений выглядит таким образом
```
 (?P<name>pattern)
```
где name это название группы, а pattern – шаблон.

Комбинирование URLconfs
=======================
В любой момент, ваш urlpatterns может “включать” другие модули URLconf.

urls.py
--------
```
from django.conf.urls import include, url
from django.contrib import admin
from home import views as view_home

urlpatterns = [
    url(r'^$', view_home.home, name='home'),
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^admin/', admin.site.urls),
]

```
регулярные выражения не содержат $ (определитель конца строки), но содержит косую черту в конце. Каждый раз, когда Django встречает include() (django.conf.urls.include()), из URL обрезается уже совпавшая часть, остальное передается во включенный URLconf для дальнейшей обработки.

blog/urls.py
------------
```
from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /blog/
    url(r'^$', views.index, name='index'),
    # ex: /blog/5/
    url(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),

    url(r'^2016/$', views.special_case_2016),
    url(r'^([0-9]{4})/$', views.year_archive),
    url(r'^([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),

    url(r'^(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
]

```
Что использует URLconf при поиске нужного шаблона URL
------------------------------------------------------
- URLconf использует запрашиваемый URL как обычную строку Python. Он не учитывает параметры GET, POST и имя домена.

Например, при запросе к http://www.example.com/myapp/, URLconf возьмет myapp/.

- При запросе к http://www.example.com/myapp/?page=3 – myapp/.

URLconf не учитывает тип запроса. POST, GET, HEAD, и др. – будут обработаны одним представлением при одинаковом URL.

Найденные аргументы – всегда строки
------------------------------------
Каждый найденный аргумент передается в представление как строка, независимо от того, какое совпадение определено в регулярном выражении. Например, URLconf содержит такую строку:
```
url(r'^blog/(?P<year>[0-9]{4})/$', views.year_archive),
```
аргумент year для views.year_archive() будет строкой, несмотря на то, что [0-9]{4} отлавливает только числа.

Выполнение запросов
====================
После создания модели, Django автоматически создает API для работы с базой данных, который позволяет вам создавать, получать, изменять и удалять объекты. 

Получение объектов
------------------
Для получения объектов из базы данных, создается QuerySet через Manager модели.

QuerySet представляет выборку объектов из базы данных. Он может не содержать, или содержать один или несколько фильтров – критерии для ограничения выборки по определенным параметрам. В терминах SQL, QuerySet - это оператор SELECT, а фильтры - условия такие, как WHERE или LIMIT.

Каждая модель содержит как минимум один Manager, и он называется objects по умолчанию. Обратиться к нему можно непосредственно через класс модели:
```
Article.objects
<django.db.models.manager.Manager object at ...>
```
Обратиться к менеджерам можно только через модель и нельзя через ее экземпляр. Это сделано для разделения “table-level” операций и “record-level” операций.

Manager - главный источник QuerySet для модели. Например, Article.objects.all() вернет QuerySet, который содержит все объекты Article из базы данных.

Получение всех объектов
------------------------
Самый простой способ получить объекты из таблицы - это получить их всех. Для этого используйте метод all() менеджера:
```
all_entries = Article.objects.all()
```
Метод all() возвращает QuerySet всех объектов в базе данных.

Получение объектов через фильтры
--------------------------------
QuerySet, возвращенный Manager, описывает все объекты в таблице базы данных. Обычно вам нужно выбрать только подмножество всех объектов.

Для создания такого подмножества, вы можете изменить QuerySet, добавив условия фильтрации. Два самых простых метода изменить QuerySet - это:
```
filter(**kwargs)
```
    Возвращает новый QuerySet, который содержит объекты удовлетворяющие параметрам фильтрации.
```
exclude(**kwargs)
```
    Возвращает новый QuerySet содержащий объекты, которые не удовлетворяют параметрам фильтрации.

Параметры фильтрации (**kwargs) должны быть в формате Field lookups.

Например, для создания QuerySet чтобы получить записи с 2016, используйте filter() таким образом:
```
Article.objects.filter(publish_date__year=2016)
```
Это аналогично:
```
Article.objects.all().filter(publish_date__year=2016)
```
blog/urls.py
------------
```
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^2016/$', views.special_case_2016),

```
blog/views.py
-------------
```
def special_case_2016(request):
    items = Article.objects.filter(publish_date__year=2016)  
    return render(request, "blog/special_case_2016.html", {'items':items})
```

templates/blog/special_case_2016.html
--------------------------------------
```
{% extends "base.html" %}
{% block head_title %}special_case_2016{% endblock %}

{% block content %} 
      <div class="row">
        <div class="col-md-8">
          <h2>Special Case 2016</h2>
              {% if items %}
                {% for item in items %}
                  <h3><a href ="{% url 'blog:detail' item.id %}">{{ item.title }}</a></h3>
                    <p><a class="btn btn-default" href="{% url 'blog:detail' item.id %}" role="button">View details &raquo;</a></p>
                {% endfor %}
              {% else %}
                <li>Sorry, no items in this list.</li>
              {% endif %}
        </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
       </div>
      </div>
{% endblock content %}

```
Цепочка фильтров
================
Результат изменения QuerySet - это новый QuerySet и можно использовать цепочки фильтров. 

views.py:
---------
```
def latest(request):
    items = Article.objects.filter(
        title__startswith='QuerySet'
        ).filter(
        publish_date__gte=datetime.date(2015, 1, 1)
        )  
    return render(request, "blog/special_case_2016.html", {'items':items})

```
views.py
--------
```
def latest(request):
    items = Article.objects.filter(
        title__startswith='QuerySet'
        ).exclude(
        publish_date__gte=datetime.date.today()
        ).filter(
        publish_date__gte=datetime.date(2015, 1, 1)
        )  
    return render(request, "blog/special_case_2016.html", {'items':items})
```

В этом примере к начальному QuerySet, который возвращает все объекты, добавляется фильтр, затем исключающий фильтр, и еще один фильтр. Полученный QuerySet содержит все объекты, у которых заголовок начинается с QuerySet, и которые были опубликованы между 1-го января 2016 и текущей датой.

Отфильтрованный QuerySet – уникален

После каждого изменения QuerySet, вы получаете новый QuerySet, который никак не связан с предыдущим QuerySet. Каждый раз создается отдельный QuerySet, который может быть сохранен и использован.

Например:
```
q1 = Article.objects.filter(title__startswith="QuerySet")
q2 = q1.exclude(publish_date__gte=datetime.date.today())
q3 = q1.filter(publish_date__gte=datetime.date.today())
```
Эти три QuerySets независимы. Первый – это базовый QuerySet, который содержит все объекты с заголовками, которые начинаются с QuerySet. Второй – это множество первых с дополнительным критерием фильтрации, который исключает объекты с publish_date больше, чем текущая дата. Третий – это множество первого, с отфильтрованными объектами, у которых publish_date больше, чем текущая дата. Первоначальный QuerySet(q1) не изменяется последующим добавлением фильтров.

QuerySets – ленивы
-------------------
QuerySets – ленивы, создание QuerySet не выполняет запросов к базе данных. Вы можете добавлять фильтры хоть весь день и Django не выполнит ни один запрос, пока QuerySet не вычислен.
```
q1 = Article.objects.filter(title__startswith="QuerySet")
q2 = q1.filter(publish_date__lte=datetime.date.today())
q3 = q2.exclude(content__icontains="Donec")
print(q3)
```
Глядя на это можно подумать что было выполнено три запроса в базу данных. На самом деле был выполнен один запрос, в последней строке (print(q3)). Результат QuerySet не будет получен из базы данных, пока вы не попросите об этом. Когда вы делаете это, QuerySet вычисляется запросом к базе данных. 

Получение одного объекта с помощью get
=======================================
filter() всегда возвращает QuerySet, даже если только один объект возвращен запросом - в этом случае, это будет QuerySet содержащий один объект.

Если вы знаете, что только один объект возвращается запросом, вы можете использовать метод get() менеджера, который возвращает непосредственно объект:
```
one_entry = Article.objects.get(pk=1)
```
Вы можете использовать для get() аргументы, такие же, как и для filter().

есть разница между использованием get() и filter(). Если результат пустой, get() вызовет исключение DoesNotExist. Это исключение является атрибутом модели, для которой выполняется запрос. Если не существует объекта Article с первичным ключом равным 1, Django вызовет исключение Entry.DoesNotExist.

Также Django отреагирует, если запрос get() вернет не один объект. В этом случае будет вызвано исключение MultipleObjectsReturned, которое также является атрибутом класса модели.

Ограничение выборки
===================
Используйте синтаксис срезов для списков Python для ограничения результата выборки QuerySet. Это эквивалент таких операторов SQL как LIMIT и OFFSET.

Например, этот код возвращает 5 первых объектов (LIMIT 5):
```
Article.objects.all()[:5]
```
Этот возвращает с шестого по десятый (OFFSET 5 LIMIT 5):
```
Article.objects.all()[5:10]
```
Отрицательные индексы (например, Article.objects.all()[-1]) не поддерживаются.

На самом деле, срез QuerySet возвращает новый QuerySet – запрос не выполняется. Исключением является использовании “шага” в срезе. Например, этот пример выполнил бы запрос, возвращающий каждый второй объект из первых 10:
```
Article.objects.all()[:10:2]
```
Для получения одного объекта, а не списка (например, SELECT foo FROM bar LIMIT 1), используйте индекс вместо среза. Например, этот код возвращает первый объект Article в базе данных, после сортировки записей по заголовку:
```
Article.objects.order_by('title')[0]
```
Это эквивалент:
```
Article.objects.order_by('title')[0:1].get()
```
Заметим, что первый пример вызовет IndexError, в то время как второй - DoesNotExist, если запрос не вернёт ни одного объекта. 

Фильтры полей
--------------
Фильтры полей – это “операторы” для составления условий SQL WHERE. Они задаются как именованные аргументы для метода filter(), exclude() и get() в QuerySet.

Фильтры полей выглядят как field__lookuptype=value. (Используется двойное подчеркивание). 
```
Article.objects.filter(publish_date__lte='2016-01-01')
```
будет транслировано в SQL:
```
SELECT * FROM blog_article WHERE publish_date <= '2016-01-01';
```

Python позволяет определить функции, которые принимают именованные аргументы с динамически вычисляемыми названиями и значениями. 

Поля указанные при фильтрации должны быть полями модели. Есть одно исключение, для поля ForeignKey можно указать поле с суффиксом _id. В этом случае необходимо передать значение первичного ключа связанной модели:
```
Article.objects.filter(blog_id=4)
```
При передаче неверного именованного аргумента, будет вызвано исключение TypeError.

API базы данных поддерживает около 24 фильтров:
-----------------------------------------------
- exact
    “Точное” совпадение. Например:
```
   Article.objects.get(title__exact="Man bites dog")
```
    Создаст такой SQL запрос:
```
    SELECT * fronm blog_article WHERE title = 'Man bites dog';
```
    Если вы не указали фильтр – именованный аргумент не содержит двойное подчеркивание – будет использован фильтр exact.

    Например, эти два выражения идентичны:
```
    Article.objects.get(id__exact=1)  # Explicit form
    Article.objects.get(id=1)         # __exact is implied
```    

- iexact
    Регистронезависимое совпадение. Такой запрос:
```
   Article.objects.get(title__iexact="beatles blog")
```
    Найдет Article с названием "Beatles Blog", "beatles blog", и даже "BeAtlES blOG".

- contains
    Регистрозависимая проверка на вхождение. Например:
```
    Article.objects.get(title__contains='Lennon')
```
    Будет конвертировано в такой SQL запрос:
```
    SELECT ... WHERE title LIKE '%Lennon%';
```
    найдет заголовок 'Today Lennon honored', но не найдет 'today lennon honored'.
    Существуют также регистронезависимые версии, icontains.

- startswith, endswith
    Поиск по началу и окончанию соответственно. Существуют также регистронезависимые версии istartswith и iendswith.

Фильтры по связанным объектам
==============================
Django предлагает удобный и понятный интерфейс для фильтрации по связанным объектам, самостоятельно заботясь о JOIN в SQL. Для фильтра по полю из связанных моделей, используйте имена связывающих полей разделенных двойным нижним подчеркиванием, пока вы не достигните нужного поля.

Этот пример получает все объекты Article с Category, name которого равен 'news':
```
Article.objects.filter(category__name='news')
```
Этот поиск может быть столь глубоким, как вам будет угодно.

blog/urls.py
------------
```
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^news/$', views.news, name='news'),
    url(r'^2016/$', views.special_case_2016),
    url(r'^latest/$', views.latest),
```
blog/views.py:
---------------
```
def news(request):
    blog_list = Article.objects.filter(category__name='news')
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)
```
Все работает и в другую сторону. Чтобы обратиться к “обратной” связи, просто используйте имя модели в нижнем регистре.

Этот пример получает все объекты Category, которые имеют хотя бы один связанный объект Article с title содержащим 'QuerySet':
```
Category.objects.filter(article__title__contains='QuerySet')
```
