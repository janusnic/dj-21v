# dj-21v
Blog
====
```
./manage.py startapp blog
```
Настройка базы данных
======================
mysite/settings.py. 
-------------------
```
# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

```
По умолчанию используется SQLite. SQLite включен в Python, так что вам не нужно устанавливать что либо еще. 

Модели
=======
Модели отображают информацию о данных, с которыми вы работаете. Они содержат поля и поведение ваших данных. Обычно одна модель представляет одну таблицу в базе данных.

Каждая модель это класс унаследованный от django.db.models.Model.
```
from django.db import models
```
Атрибут модели представляет поле в базе данных.

```
class Category(models.Model):
    name = models.CharField('categories name', max_length=100)
    
    description = models.TextField(max_length=4096)
        
    views_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name
```

name,description,views_count - поля модели. Каждое поле определено как атрибут класса (представлено экземпляром класса Field), и каждый атрибут соответствует полю таблицы в базе данных.

CharField для текстовых полей и DateTimeField для полей даты и времени. Это указывает Django какие типы данных хранят эти поля.

Названия каждого экземпляра Field - это название поля, в “машинном”(machine-friendly) формате. Вы будете использовать эти названия в коде, а база данных будет использовать их как названия колонок.

Вы можете использовать первый необязательный аргумент конструктора класса Field, чтобы определить отображаемое, удобное для восприятия, название поля. Оно используется в некоторых компонентах Django, и полезно для документирования. Если это название не указано, Django будет использовать “машинное” название. В этом примере, мы указали отображаемое название только для поля name - 'categories name'. Для всех других полей будет использоваться “машинное” название.

Некоторые классы, унаследованные от Field, имеют обязательные аргументы. Например, CharField требует, чтобы вы передали ему max_length. Это используется не только в схеме базы данных, но и при валидации.

Field может принимать различные необязательные аргументы; в нашем примере мы указали default значение для views_count равное 0.

Активация моделей
=================
- Создать структуру базы данных (CREATE TABLE) для приложения.

- Создать Python API для доступа к данным объектов Category.

Но первым делом мы должны указать нашему проекту, что приложение blog установлено.

Приложения Django “подключаемые”: вы можете использовать приложение в нескольких проектах и вы можете распространять приложение, так как они не связаны с конкретным проектом Django.

Отредактируйте файл mysite/settings.py и измените настройку INSTALLED_APPS добавив строку 'blog':

mysite/settings.py
-------------------
```
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',
)
```
Теперь Django знает, что необходимо использовать приложение blog. 

INSTALLED_APPS
--------------
По умолчанию: () (Пустой кортеж)

Кортеж строк, который указывают все приложения Django, используемые в проекте. Каждая строка должна быть полным Python путем к:

- классу настройки приложения, или
- пакету с приложением.

INSTALLED_APPS теперь поддерживает конфигурации приложений.

- Названия приложения и метки(labels) должны быть уникальны в INSTALLED_APPS
- Названия приложений — Python путь к пакету приложения — должны быть уникальны. Нельзя подключить одно приложение дважды, разве что продублировав код с другим названием.

Короткие названия приложения — по умолчанию последняя часть названия приложения — должны быть так же уникальны. Например, можно использовать вместе django.contrib.auth и myproject.auth. Однако, необходимо указать label.

Эти правила распространяются на все приложения в INSTALLED_APPS, как на классы настройки приложений, так и на пакеты приложений.
Если несколько приложений содержат разные версии одних и тех же ресурсов (шаблоны, статические файлы, команды, файлы перевода), будут использоваться ресурсы из приложения, которое указано выше в INSTALLED_APPS.

Поля
====
Самая важная часть модели – и единственная обязательная – это список полей таблицы базы данных которые она представляет. Поля определены атрибутами класса. Нельзя использовать имена конфликтующие с API моделей, такие как clean, save или delete.

```
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
```

Типы полей
===========
Каждое поле в модели должно быть экземпляром соответствующего Field класса. Django использует классы полей для определения такой информации:

- Типа колонки в базе данных (например: INTEGER, VARCHAR).

- Виджет используемый при создании поля формы (например: input type="text", select).

- Минимальные правила проверки данных, используемые в интерфейсе администратора и для автоматического создания формы.

Настройка полей
===============
Для каждого поля есть набор предопределенных аргументов. Например, CharField (и унаследованные от него) имеют обязательный аргумент max_length, который определяет размер поля VARCHAR для хранения данных этого поля.

Также есть список стандартных аргументов для всех полей. Все они не обязательны.

null
-----
Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.

blank
------
Если True, поле не обязательно и может быть пустым. По умолчанию - False.

Это не то же что и null. null относится к базе данных, blank - к проверке данных. Если поле содержит blank=True, форма позволит передать пустое значение. При blank=False - поле обязательно.

# help_text
Поля моделей в Django принимают атрибут help_text, который используется в Django формах/админке для вывода назначения полей  — это служит отличной возможностью для документации ваших моделей. Если в дальнейшем вы пригласите нового разработчика в проект, то help_text позволит сохранить бесчисленное количество часов на объяснения структуры моделей.

Подсказка, отображаемая в поле формы. 
при отображении в форме, HTML-символы не экранируются. Это позволяет использовать HTML в help_text если вам необходимо. Например:
```
help_text="Please use the following format: <em>YYYY-MM-DD</em>."
```
Также вы можете использовать обычный текст и django.utils.html.escape(), чтобы экранировать HTML. Убедитесь, что вы экранируете все подсказки, которые могут определять непроверенные пользователи, чтобы избежать XSS атак.

# primary_key

При True поле будет первичным ключом.

Если primary_key=True не указан ни для одного поля, Django самостоятельно добавит поле типа IntegerField для хранения первичного ключа, поэтому вам не обязательно указывать primary_key=True для каждой модели. 

Поле первичного ключа доступно только для чтения. Если вы поменяете значение первичного ключа для существующего объекта, а затем сохраните его, будет создан новый объект рядом с существующим. 
Например:
```
from django.db import models

class Fruit(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
>>> fruit = Fruit.objects.create(name='Apple')
>>> fruit.name = 'Pear'
>>> fruit.save()
>>> Fruit.objects.values_list('name', flat=True)
['Apple', 'Pear']
unique
```
При True поле будет уникальным.

# краткое описание самых используемых аргументов.

## Первичный ключ по умолчанию
По умолчанию Django для каждой модели добавляет такое поле:
```
id = models.AutoField(primary_key=True)
```
Это автоинкрементный первичный ключ.

Для его переопределения просто укажите primary_key=True для одного из полей. При этом Django не добавит поле id.

Каждая модель должна иметь хотя бы одно поле с primary_key=True (явно указанное или созданное автоматически).

primary_key=True подразумевает null=False и unique=True. Модель может содержать только один первичный ключ.

# verbose_name
Field.verbose_name

## Читабельное имя поля
Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField, первым аргументом принимает необязательное читабельное название. Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
```
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    description = models.TextField(max_length=4096)
```
# default
Field.default
Значение по умолчанию для поля. Это может быть значение или вызываемый(callable) объект. Если это вызываемый объект, он будет вызван при создании нового объекта.

Значение по умолчанию не может быть изменяемым значением (экземпляр модели, список, множество и т.д.), т.к. все объекты модели будут ссылаться на этот объект и использовать его как значение по умолчанию. Вместо этого укажите функцию, которая возвращает нужное значение. Например, если у вас есть собственное поле JSONField и вы хотите указать словарь как значение по умолчанию, используйте следующую функцию:
```
def contact_default():
    return {"email": "to1@example.com"}

contact_info = JSONField("ContactInfo", default=contact_default)
```
Обратите внимание, lambda нельзя использовать в качестве значения для default т.к. она не может быть сериализована для миграций.

Значение по умолчанию используется, если был создан экземпляр модели, а значение для поля не было указано. Если поле является первичным ключом, значение по умолчанию также использует и при указании None.


# unique
Field.unique
При True значение поля должно быть уникальным.

Этот параметр учитывается при сохранении в базу данных и при проверке данных в модели. Если вы попытаетесь сохранить повторное значение в поле с unique, будет вызвана ошибка django.db.IntegrityError методом save().

Этот параметр можно использовать для любого типа поля кроме ManyToManyField, OneToOneField и FileField.

Заметим что, при unique равном True, не нужно указывать db_index, т.к. unique создает индекс.

# Типы полей

## AutoField
class AutoField(**options)
Автоинкрементное поле IntegerField. Используется для хранения ID. Скорее всего вам не придется использовать это поле, первичный ключ будет автоматически добавлен к модели.

## BigIntegerField
class BigIntegerField([**options])
64-битное целочисленное, аналогично IntegerField но позволяет хранить числа от -9223372036854775808 до 9223372036854775807. Форма будет использовать TextInput для отображения.

## BooleanField
class BooleanField(**options)
Поле хранящее значение true/false.

Виджет по умолчанию для этого поля CheckboxInput.

Если вам нужен параметр null, используйте поле NullBooleanField.

по умолчанию для BooleanField None, если Field.default не указан.

## CharField
class CharField(max_length=None[, **options])
Строковое поле для хранения коротких или длинных строк.

Для большого количества текстовой информации используйте TextField.

Виджет по умолчанию для этого поля TextInput.

CharField принимает один дополнительный аргумент:

### CharField.max_length
Максимальная длинна(в символах) этого поля. max_length используется для проверки данных на уровне базы данных и форм Django.

Если вы создаете независимое приложение, которое должно работать на различных базах данных, помните что существуют некоторые ограничения использования max_length для некоторых типов баз данных. 
#### Пользователям MySQL
Если вы используете это поле с MySQLdb 1.2.2 и utf8_bin “collation” (которое не является значением по умолчанию), могут быть некоторые проблемы.

## DateField
class DateField([auto_now=False, auto_now_add=False, **options])
Дата, представленная в виде объекта datetime.date Python. Принимает несколько дополнительных параметров:

### DateField.auto_now
Значение поля будет автоматически установлено в текущую дату при каждом сохранении объекта. Полезно для хранения времени последнего изменения. текущее время будет использовано всегда; 

### DateField.auto_now_add
Значение поля будет автоматически установлено в текущую дату при создании(первом сохранении) объекта. Полезно для хранения времени создания. 

В форме поле будет представлено как :class:`~django.forms.TextInput с JavaScript календарем, и кнопкой “Сегодня”. Содержит дополнительную ошибку invalid_date.

Опции auto_now_add, auto_now и default взаимоисключающие. Использование их вместе вызовет ошибку.

При использовании auto_now или auto_now_add со значением True будут установлены параметры editable=False и blank=True.

Опции``auto_now`` и auto_now_add всегда используют дату в часовом поясе по умолчанию в момент создания или изменения объекта. Если такое поведение вам не подходит, вы можете указать свою функцию как значение по умолчанию, или переопределить метод save(), вместо использования auto_now или auto_now_add. Или использовать DateTimeField вместо DateField и выполнять преобразование в дату при выводе значения.

## DateTimeField
class DateTimeField([auto_now=False, auto_now_add=False, **options])
Дата и время, представленные объектом datetime.datetime Python. Принимает аналогичные параметры что и DateField.

Виджет по умолчанию в форме для этого поля - TextInput. Интерфейс администратора использует два виджета TextInput и JavaScript.

## IntegerField
class IntegerField([**options])
Число. Значение от -2147483648 до 2147483647 для всех поддерживаемых баз данных Django. Форма использует виджет TextInput.


## SmallIntegerField
class SmallIntegerField([**options])
Как и поле IntegerField, но принимает значения в определенном диапазоне(зависит от типа базы данных). Для баз данных поддерживаемых Django можно использовать значения от -32768 до 32767.

## TextField
class TextField([**options])
Большое текстовое поле. Форма использует виджет Textarea.

Если указать атрибут max_length, это повлияет на поле, создаваемое виджетом Textarea. Но не учитывается на уровне модели или базы данных. Для этого используйте CharField.

#### Пользователям MySQL
Если вы используете это поле с MySQLdb 1.2.1p2 и utf8_bin “collation” (которое не является значением по умолчанию), могут быть некоторые проблемы. 

## TimeField¶
class TimeField([auto_now=False, auto_now_add=False, **options])
Время, представленное объектом datetime.time Python. Принимает те же аргументы, что и DateField.

Форма использует виджет TextInput. Интерфейс администратора также использует немного JavaScript.

Миграции
=========

Выполняя makemigrations, вы говорите Django, что внесли некоторые изменения в ваши модели и хотели бы сохранить их в миграции.
```
./manage.py makemigrations blog
App 'blog' could not be found. Is it in INSTALLED_APPS?

```
INSTALLED_APPS
--------------
'blog'
```
./manage.py makemigrations blog
Migrations for 'blog':
  0001_initial.py:
    - Create model Article
    - Create model Category
    - Create model Tag

```
Миграции используются Django для сохранения изменений ваших моделей (и структуры базы данных) - это просто файлы на диске. Вы можете изучить миграцию для создания ваших моделей, она находится в файле blog/migrations/0001_initial.py. 

Команда sqlmigrate получает название миграции и возвращает SQL:

```
./manage.py sqlmigrate blog 0001
```
Вы увидите приблизительно такое:

```
BEGIN;
--
-- Create model Article
--
CREATE TABLE "blog_article" 
    (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "title" varchar(100) NOT NULL UNIQUE, 
    "status" integer NOT NULL, 
    "content" text NOT NULL, 
    "publish_date" datetime NOT NULL, 
    "created_date" datetime NOT NULL
    );
--
-- Create model Category
--
CREATE TABLE "blog_category" 
    (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "name" varchar(100) NOT NULL, 
    "description" text NOT NULL
    );
--
-- Create model Tag
--
CREATE TABLE "blog_tag" 
    (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
    "name" varchar(100) NOT NULL UNIQUE)
    ;

COMMIT;

```
Полученные запросы зависят от базы данных, которую вы используете. 

Названия таблиц созданы автоматически из названия приложения(blog) и названия модели в нижнем регистре – category, tag и article. (Вы можете переопределить это.)

Первичные ключи (ID) добавлены автоматически. (Вы можете переопределить и это.)

Django добавляет "_id" к названию внешнего ключа. (вы можете переопределить это.)

Учитываются особенности базы данных, которую вы используете. Специфические типы данных такие как auto_increment (MySQL), serial (PostgreSQL), или integer primary key (SQLite) будут использоваться автоматически. Тоже касается и экранирование названий, что позволяет использовать в названии кавычки – например, использование одинарных или двойных кавычек.

Команда sqlmigrate не применяет миграцию к базе данных - она просто выводит запросы на экран, чтобы вы могли увидеть какой SQL создает Django. Это полезно, если вы хотите проверить что выполнит Django, или чтобы предоставить вашему администратору базы данных SQL скрипт.

Если необходимо, можете выполнить python manage.py check. Эта команда ищет проблемы в вашем проекте не применяя миграции и не изменяя базу данных.

В Django есть команда, которая выполняет миграции и автоматически обновляет базу данных - она называется migrate. 

выполните команду migrate, чтобы создать таблицы для этих моделей в базе данных:
```
$ python manage.py migrate
```
Команда migrate выполняет все миграции, которые ещё не выполнялись, (Django следит за всеми миграциями, используя таблицу в базе данных django_migrations) и применяет изменения к базе данных, синхронизируя структуру базы данных со структурой ваших моделей.

Миграции - очень мощная штука. Они позволяют изменять ваши модели в процессе развития проекта без необходимости пересоздавать таблицы в базе данных. Их задача изменять базу данных без потери данных. 

1. Внесите изменения в модели (в models.py).
2. Выполните python manage.py makemigrations чтобы создать миграцию для ваших изменений
3. Выполните python manage.py migrate чтобы применить изменения к базе данных.
```
./manage.py migrate
Operations to perform:
  Apply all migrations: sessions, auth, contenttypes, blog, admin
Running migrations:
  Rendering model states... DONE
  Applying blog.0001_initial... OK

```
Две команды необходимы для того, чтобы хранить миграции в системе контроля версий. Они не только помогают вам, но и могут использоваться другими программистами вашего проекта.

Мыкет проекта
==============
```
.
├── db.sqlite3
├── f_tests
│   ├── __init__.py
│   └── tests.py
├── static
│   ├── favicon.ico
│   ├── css
│   │   ├── main.css
│   │   ├── bootstrap.css
│   │   ├── bootstrap-theme.css
│   │   └── bootstrap.css.map
│   ├── js
│   │   ├── main.js
│   │   ├── plugins.js
│   │   └── vendor
│   ├── img
│   │   └── star.png
│   └── fonts
│       ├── glyphicons-halflings-regular.eot
│       ├── glyphicons-halflings-regular.svg
│       ├── glyphicons-halflings-regular.ttf
│       └── glyphicons-halflings-regular.woff
├── templates
│   ├── base.html
│   ├── 404.html
│   ├── home
│   │   └── index.html
│   └── blog
│       └── index.html
├── blog
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   └── views.py
├── home
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   └── views.py
├── manage.py
└── mysite
    ├── __init__.py
    ├── __pycache__
    ├── settings.py
    ├── urls.py
    └── wsgi.py

```
admin.py
--------
```
from django.contrib import admin

from .models import Category, Tag, Article

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article)

```

base.html
---------
```
    </nav>
        {% block jumbotron %} 

        {% endblock jumbotron %}
        
        <div class="container">
        {% block content %} 

        {% endblock content %}
          <hr>

          <footer>
            <p>&copy; Company 2016</p>
          </footer>
        </div> <!-- /container -->     
```
home/index.html
----------------
```
{% extends "base.html" %}
{% block head_title %}My Cool Django Site{% endblock %}
<!-- Main jumbotron for a primary marketing message or call to action -->
    {% block jumbotron %} 

    
    <div class="jumbotron">
      <div class="container">
        <h1>Hello, world!</h1>
        <p>This is a template for a simple marketing or informational website. It includes a large callout called a jumbotron and three supporting pieces of content. Use it as a starting point to create something more unique.</p>
        <p><a class="btn btn-primary btn-lg" href="#" role="button">Learn more &raquo;</a></p>
      </div>
    </div>
{% endblock jumbotron %}

{% block content %} 
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-4">
          <h2>Heading</h2>
          <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
       </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          <p>Donec sed odio dui. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
      </div>

{% endblock content %}
```

blog/index.html
----------------
```
{% extends "base.html" %}
{% block head_title %}My Cool Django Blog{% endblock %}

{% block content %} 
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-8">
          <h2>Heading</h2>
          <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
       </div>
        
      </div>

{% endblock content %}
```
includes/header.html
--------------------
```
{% load staticfiles %}
<!doctype html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang=""> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8" lang=""> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9" lang=""> <![endif]-->
<!--[if gt IE 8]><!--> 
<html class="no-js" lang=""> 
<!--<![endif]-->
    <head>
        <title>{% block head_title %}{% endblock %}</title>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="apple-touch-icon" href="apple-touch-icon.png">
        <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
        <style>
            body {
                padding-top: 50px;
                padding-bottom: 20px;
            }
        </style>
        <link rel="stylesheet" href="{% static 'css/bootstrap-theme.min.css' %}">
        <link rel="stylesheet" href="{% static 'css/main.css' %}">
        
        <script src="{% static 'js/vendor/modernizr-2.8.3-respond-1.4.2.min.js' %}"></script>
    </head>
    <body>        

```

includes/footer.html
--------------------
```
{% load staticfiles %}
      <hr>

      <footer>
        <p>&copy; Company 2016</p>
      </footer>
    </div> <!-- /container -->        

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="static/js/vendor/jquery-1.11.0.min.js"><\/script>')</script>

        <script src="{% static 'js/vendor/bootstrap.min.js' %}">
        
        <script src="{% static 'js/plugins.js' %}">
        <script src="{% static 'js/main.js' %}">
        

        <!-- Google Analytics: change UA-XXXXX-X to be your site's ID. -->
        <script>
            (function(b,o,i,l,e,r){b.GoogleAnalyticsObject=l;b[l]||(b[l]=
            function(){(b[l].q=b[l].q||[]).push(arguments)});b[l].l=+new Date;
            e=o.createElement(i);r=o.getElementsByTagName(i)[0];
            e.src='//www.google-analytics.com/analytics.js';
            r.parentNode.insertBefore(e,r)}(window,document,'script','ga'));
            ga('create','UA-XXXXX-X','auto');ga('send','pageview');
        </script>
    </body>
</html>
```
includes/mainmenu.html
----------------------
```
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">Project name</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">

          <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home <span class="sr-only">(current)</span></a></li>
            <li><a href="/blog">Blog</a></li>
          </ul>

          <form class="navbar-form navbar-right" role="form">
            <div class="form-group">
              <input type="text" placeholder="Email" class="form-control">
            </div>
            <div class="form-group">
              <input type="password" placeholder="Password" class="form-control">
            </div>
            <button type="submit" class="btn btn-success">Sign in</button>
          </form>
        </div><!--/.navbar-collapse -->
      </div>
    </nav>
```
base.html
----------
```
{% include 'includes/header.html'%}
{% include 'includes/mainmenu.html'%}

    {% block jumbotron %} 

    {% endblock jumbotron %}
    
    <div class="container">
    {% block content %} 

    {% endblock content %}

{% include 'includes/footer.html'%}

```

Как Django обрабатывает запрос
===============================
При запросе к странице Django-сайта, используется такой алгоритм для определения какой код выполнить:

- Django определяет какой корневой модуль URLconf использовать. Обычно, это значение настройки ROOT_URLCONF, но, если объект запроса HttpRequest содержит атрибут urlconf (установленный request middleware), его значение будет использоваться вместо ROOT_URLCONF.
settings.py:
------------
```
ROOT_URLCONF = 'mysite.urls'
```
- Django загружает модуль конфигурации URL и ищет переменную urlpatterns. Это должен быть список экземпляров django.conf.urls.url().
```
def url(regex, view, kwargs=None, name=None, prefix=''):
    if isinstance(view, (list, tuple)):
        # For include(...) processing.
        urlconf_module, app_name, namespace = view
        return RegexURLResolver(regex, urlconf_module, kwargs, app_name=app_name, namespace=namespace)
    else:
        if isinstance(view, six.string_types):
            warnings.warn(
                'Support for string view arguments to url() is deprecated and '
                'will be removed in Django 1.10 (got %s). Pass the callable '
                'instead.' % view,
                RemovedInDjango110Warning, stacklevel=2
            )
            if not view:
                raise ImproperlyConfigured('Empty URL pattern view name not permitted (for pattern %r)' % regex)
            if prefix:
                view = prefix + '.' + view
        return RegexURLPattern(regex, view, kwargs, name)

```
- Django перебирает каждый URL-шаблон по порядку, и останавливается при первом совпадении с запрошенным URL-ом.

- Если одно из регулярных выражений соответствует URL-у, Django импортирует и вызывает соответствующее представление, которое является просто функцией Python(или представление-класс). 

При вызове передаются следующие аргументы:
------------------------------------------
Объект HttpRequest.
-------------------
Если в результате применения регулярного выражения получили именованные совпадения, они будут переданы как позиционные аргументы.

Именованные аргументы создаются из именованных совпадений. Они могут быть перезаписаны значениями из аргумента kwargs, переданного в django.conf.urls.url().

Если ни одно регулярное выражение не соответствует, или возникла ошибка на любом из этапов, Django вызывает соответствующий обработчик ошибок. 

пример простого URLconf:
------------------------
```
from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^blog/2016/$', views.special_case_2016),
    url(r'^blog/([0-9]{4})/$', views.year_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]
```
views.py
--------
```
def special_case_2016(request):
    item = {'title':'Special Case 2016','topics':10}    
    return render(request, "home/special_case_2016.html", {'item':item})

def year_archive(request,yy):
    item = {'title':'Year Archive','content':yy}    
    return render(request, "home/year_archive.html", {'item':item})

def month_archive(request,yy,mm):
    item = {'title':'Month Archive','content':yy}    
    return render(request, "home/month_archive.html", {'item':item})

def article_detail(request,yy,mm,id):
    item = {'title':'Article Detail','content':id}    
    return render(request, "home/article_detail.html", {'item':item})
```
Не нужно добавлять косую черту в начале, потому что каждый URL содержит его. Например, используйте ^blog, вместо ^/blog.

Символ 'r' перед каждым регулярным выражением не обязателен, но рекомендуется. Он указывает Python что строка “сырая(raw)” и ничего в строке не должно быть экранировано. 

- Запрос к``/blog/2016/03/`` будет обработан третьим элементом списка. Django вызовет функцию views.month_archive(request, '2016', '03').

- /blog/2016/3/ не соответствует ни одному URL-шаблону, потому что третья запись требует две цифры в номере месяца.

- /blog/2016/ соответствует первому выражению, не второму, потому что шаблоны проверяются по порядку. 

- /blog/2016 не соответствует ни одному регулярному выражению, потому что каждое ожидает, что URL оканчивается на косую черту.

- /blog/2016/03/03/ соответствует последнему выражению. Django вызовет функцию views.article_detail(request, '2016', '03', '03').

blog/views.py
-------------
```
from django.shortcuts import render
from .models import Article

def special_case_2016(request):
    item = {'title':'Special Case 2016','topics':10}    
    return render(request, "blog/special_case_2016.html", {'item':item})

def year_archive(request,yy):
    item = {'title':'Year Archive','content':yy}    
    return render(request, "blog/year_archive.html", {'item':item})

def month_archive(request,yy,mm):
    item = {'title':'Month Archive','content':yy}    
    return render(request, "blog/month_archive.html", {'item':item})

def article_detail(request,yy,mm,id):
    item = {'title':'Article Detail','content':id}    
    return render(request, "blog/article_detail.html", {'item':item})
```

QuerySet API
============

Когда вычисляется QuerySets
----------------------------
QuerySet может быть создан, отфильтрован, ограничен и использован фактически без выполнения запросов к базе данных. База данных не будет затронута, пока вы не спровоцируете выполнение QuerySet.

QuerySet будет вычислен при таких действиях:
--------------------------------------------
Итерация. QuerySet – это итератор, и при первом выполнении итерации будет произведен запрос к базе данных. Например, этот код выводит заголовки статей из базы данных:
```
for e in Article.objects.all():
    print(e.title)
```
не используйте такой подход, если необходимо всего лишь узнать содержит ли результат запроса хотя бы один объект, и вам не нужен сам результат. Эффективнее использовать метод exists().

Ограничение выборки. 
--------------------
выборка QuerySet может быть ограничена, используя синтаксис срезов в Python. Срез не вычисленного QuerySet обычно возвращает новый не вычисленный QuerySet, но Django выполнит запрос, если будет указан шаг среза и вернет список. Срез QuerySet, который был вычислен (частично или полностью), также вернет список.

если нужно узнать только количество записей в выборке, эффективнее использовать подсчет на уровне базы данных, используя оператор SQL SELECT COUNT(*), и Django предоставляет метод count() для этого.

order_by order_by(*fields)
---------------------------
По-умолчанию, результат возвращаемый QuerySet, отсортирован по полям указанным в аргументе ordering класса Meta модели. Вы можете переопределить сортировку используя метод order_by.

Например:
```
blog_list = Article.objects.order_by('-publish_date', 'title')
```
Результат выше будет отсортирован в обратном порядке по полю publish_date, далее по полю title. Знак “минус” в "-publish_date" указывает на “нисходящую” сортировку. Сортировка по возрастанию подразумевается по-умолчанию. Чтобы отсортировать случайно используйте "?", например:
```
Article.objects.order_by('?')
```
запрос с order_by('?') может быть медленным и сильно нагружать базу данных, зависит от типа базы данных, которую вы используете.

Вы можете также сортировать по выражению, вызвав asc() или desc() для выражения:
--------------------------------------------------------------------------------
```
Article.objects.order_by('-publish_date', 'title').desc())
```

отсортировать по полю преобразовав значение в нижний регистр, используя Lower:
------------------------------------------------------------------------------
```
Article.objects.order_by(Lower('title').desc())
```

Если вы не хотите использовать сортировку, даже указанную по-умолчанию, выполните метод order_by() без аргументов.

Вы можете определить используется сортировка или нет проверив атрибут QuerySet.ordered, который будет равен True, если сортировка была применена для QuerySet каким-либо образом.

Каждый последующий вызов order_by() сбросит предыдущую сортировку. 
------------------------------------------------------------------
Например, следующий запрос будет отсортирован по publish_date, а не title:
```
Article.objects.order_by('title').order_by('publish_date')
```
Сортировка не бесплатная операция. Каждое поле влияет на скорость выполнения запроса. Каждый внешний ключ добавит сортировку по умолчанию связанной модели.

views.py
---------
```
def index(request):
    blog_list = Article.objects.order_by('-publish_date')
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)

```
blog/index.html
---------------
```
<div class="col-md-8">
          <h2>Publications</h2>
          
          <ul>
              {% if blog_list %}
                {% for item in blog_list %}
                  <li>{{ item.title }}</li>
                {% endfor %}
              {% else %}
                <li>Sorry, no items in this list.</li>
              {% endif %}
          </ul>
```

Метод get не возвращает QuerySets
---------------------------------
get метод выполняет QuerySet и возвращает не QuerySet.
метод не использует кэш и выполняет запрос к базе данных при каждом вызове.

get get(**kwargs)
-----------------
Возвращает объект соответствующий параметрам поиска

get() вызывает исключение MultipleObjectsReturned, если найдено более одно объекта. MultipleObjectsReturned – атрибут класса модели.

get() вызывает исключение DoesNotExist, ни один объект не был найден. Это исключение также атрибут класса модели. Например:
```
item = Article.objects.get(pk=blog_id) # raises Entry.DoesNotExist
```
Исключение DoesNotExist унаследовано от django.core.exceptions.ObjectDoesNotExist,таким образом можно обработать несколько исключений DoesNotExist. Например:
```
from django.core.exceptions import ObjectDoesNotExist
def detail(request, blog_id):
    try:
        item = Article.objects.get(pk=blog_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'blog/detail.html', {'item': item})
```
url
---
Возвращает абсолютную ссылку (URL без имени домена) соответствующую указанному представлению с необязательными аргументами. Любые спецсимволы будут экранированы с помощью функции iri_to_uri().

urls.py
-------
```
urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^req/', views.req_test, name='req_test'),

    url(r'^exampl1/', views.exampl1, name='some-url-name'),

    url(r'^admin/', admin.site.urls),
]

```
views.py
---------
```
def exampl1(request):
    return render(request, "home/exampl1.html", {})

```
home.html
----------
```
        <h2>url</h2>

        <a href="{% url 'some-url-name' %}">Example 1 </a>

```
Позиционные аргументы.
----------------------
Этот способ выводить ссылки без “хардкодинга” в шаблоне, чтобы не нарушать принцип DRY:
```
{% url 'some-url-name' v1 v2 %}
```
Первый аргумент – это путь к функции представления в формате package.package.module.function. Он может быть строкой в кавычках или любой другой контекстной переменной. Дополнительные аргументы необязательны. Это значения, разделенные пробелами, которые будут использоваться как аргументы при формировании URL.  

Также можно использовать именованные аргументы:
-----------------------------------------------
```
{% url 'some-url-name' arg1=v1 arg2=v2 %}
```
Нельзя использовать и позиционные и именованные аргументы в одном теге. Все обязательные аргументы URLconf должны быть указаны.

Например, мы имеем представление, views.article, чей URLconf принимает ID клиента (article() это метод в файле views.py). 
views.py
--------
```
def article(request,id):
    item = {'title':1,'content':id}    
    return render(request, "home/article.html", {'item':item})
```

urls.py:
--------
```
url(r'^article/([0-9]+)/$', views.article, name='app-views-article'),
```
example1.html
-------------
```
        <h3>Article</h3>
      
        <a href="{% url 'app-views-article' 1 %}">Article 1 </a>
```



blog/index.html
----------------
```
            {% if blog_list %}
                {% for item in blog_list %}
                  <h3><a href ="{% url 'blog:detail' item.id %}">{{ item.title }}</a></h3>
                    <p><a class="btn btn-default" href="{% url 'blog:detail' item.id %}" role="button">View details &raquo;</a></p>
                {% endfor %}
              {% else %}
                <li>Sorry, no items in this list.</li>
              {% endif %}
```

blog/detail.html
```
{% extends "base.html" %}
{% block head_title %}My Cool Django Blog{% endblock %}

{% block content %} 
      <!-- Example row of columns -->
      <div class="row">
        <div class="col-md-8">
          <h2>{{ item.title }}</h2>
         
          <p> {{ item.content }} </p>
          <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
        </div>
        <div class="col-md-4">
          <h2>Heading</h2>
          
       </div>
        
      </div>

{% endblock content %}
```

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
    
]

```
mysite/url.py
--------------
```
from django.conf.urls import include, url
from django.contrib import admin

from home import views as view_home
from blog import views

urlpatterns = [
    url(r'^$', view_home.home, name='home'),
    
    
    url(r'^blog/2016/$', views.special_case_2016),
    url(r'^blog/([0-9]{4})/$', views.year_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^blog/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),

    url(r'^blog/', include('blog.urls', namespace="blog")),

    url(r'^blog/(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
    
    url(r'^admin/', admin.site.urls),
]

```