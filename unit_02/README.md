# p21v-django unit 02

# Selenium

http://docs.seleniumhq.org/

Selenium – это проект, в рамках которого разрабатывается серия программных продуктов с открытым исходным кодом (open source):

- Selenium WebDriver,
- Selenium RC,
- Selenium Server,
- Selenium Grid,
- Selenium IDE.

Называть просто словом Selenium любой из этих пяти продуктов, вообще говоря, неправильно, хотя так часто делают, если из контекста понятно, о каком именно из продуктов идёт речь, или если речь идёт о нескольких продуктах одновременно, или обо всех сразу.

## Selenium RC

Selenium RC – это предыдущая версия библиотеки для управления браузерами. Аббревиатура RC в названии этого продукта расшифровывается как Remote Control, то есть это средство для «удалённого» управления браузером.

## Selenium Server

Selenium Server – это сервер, который позволяет управлять браузером с удалённой машины, по сети. 

## Selenium Grid

Selenium Grid – это кластер, состоящий из нескольких Selenium-серверов. 

## Selenium IDE

Selenium IDE – плагин к браузеру Firefox, который может записывать действия пользователя, воспроизводить их, а также генерировать код для WebDriver или Selenium RC, в котором выполняются те же самые действия.

# Selenium WebDriver

http://selenium-python.readthedocs.org/en/latest/api.html

Selenium WebDriver – это программная библиотека для управления браузерами. WebDriver представляет собой драйверы для различных браузеров и клиентские библиотеки на разных языках программирования, предназначенные для управления этими драйверами.

Часто употребляется также более короткое название WebDriver.

использование такого веб-драйвера сводится к созданию бота, выполняющего всю ручную работу с браузером автоматизированно.

Библиотеки WebDriver доступны на языках Java, .Net (C#), Python, Ruby, JavaScript, драйверы реализованы для браузеров Firefox, InternetExplorer, Safari, Andriod, iOS (а также Chrome и Opera).

Чаще всего Selenium WebDriver используется для тестирования функционала веб-сайтов/веб-ориентированных приложений. Автоматизированное тестирование удобно, потому что позволяет многократно запускать повторяющиеся тесты. Регрессионное тестирование, то есть, проверка, что старый код не перестал работать правильно после внесения новых изменений, является типичным примером, когда необходима автоматизация. WebDriver предоставляет все необходимые методы, обеспечивает высокую скорость теста и гарантирует корректность проверки (поскольку человеский фактор исключен). В официальной документации Selenium приводятся следующие плюсы автоматизированного тестирования веб-приложений:

- возможность проводить чаще регрессионное тестирование;
- быстрое предоставление разработчикам отчета о состоянии продукта;
- получение потенциально бесконечного числа прогонов тестов;
- обеспечение поддержки Agile и экстремальным методам разработки;
- сохранение строгой документации тестов;
- обнаружение ошибок, которые были пропущены на стадии ручного тестирования.

Привязка Python-Selenium предоставляет удобный API для доступа к таким веб-драйверам Selenium как Firefox, Ie, Chrome, Remote и других. На данный момент поддерживаются версии Python 2.7, 3.2, 3.3 и 3.4.

# Загрузка Selenium для Python
```
pip install -U selenium
```

## В виртуальное окружение ставим Selenium
```
$ workon dj21

(dj21)$ pip install django==1.9.1 
(dj21)$ pip install -U selenium
(dj21)$ pip install -U mock
# (dj21)$ pip install unittest2 # (only if using Python 2.6)
```

# Подробная инструкция для пользователей Windows

1. Установите Python 3.4 через файл MSI, доступный на странице загрузок сайта python.org.
2. Запустите командную строку через программу cmd.exe и запустите команду pip установки selenium.
```
C:\Python34\Scripts\pip.exe install selenium
```
Теперь вы можете запускать свои тестовые скрипты, используя Python:
```
C:\Python34\python.exe C:\my_selenium_script.py
```

pip list

```
alabaster (0.7.7)
Babel (2.2.0)
Django (1.9.1)
docutils (0.12)
Jinja2 (2.8)
MarkupSafe (0.23)
pip (7.1.2)
Pygments (2.1)
pytz (2015.7)
selenium (2.49.2)
setuptools (18.2)
six (1.10.0)
snowballstemmer (1.2.1)
Sphinx (1.3.4)
sphinx-rtd-theme (0.1.9)
wheel (0.24.0)

```
## Проверка работы selenium
test.py
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # начиная с версии 2.4.0
from selenium.webdriver.support import expected_conditions as EC # начиная с версии 2.26.0

# Создаем новый instance от Firefox driver
driver = webdriver.Firefox()

# идем на страницу google
# Метод driver.get перенаправляет к странице URL. 
# WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. Стоит отметить, что если страница использует много AJAX-кода при загрузке, то WebDriver может не распознать, загрузилась ли она полностью:
driver.get("http://www.google.com")

# страница динамическая, поэтому title найдем здесь:
print (driver.title)

# Google

assert "Google" in driver.title

# это утверждение (assertion), что заголовок содержит слово “Google” [assert позволяет проверять предположения о значениях произвольных данных в произвольном месте программы. По своей сути assert напоминает констатацию факта, расположенную посреди кода программы. В случаях, когда произнесенное утверждение не верно, assert возбуждает исключение. Такое поведение позволяет контролировать выполнение программы в строго определенном русле. Отличие assert от условий заключается в том, что программа с assert не приемлет иного хода событий, считая дальнейшее выполнение программы или функции бессмысленным.]

# WebDriver предоставляет ряд способов получения элементов с помощью методов find_element_by_*. Для примера, элемент ввода текста input может быть найден по его атрибуту name методом find_element_by_name. 

# найдем элемент с атрибутом name = q (google search box)
inputElement = driver.find_element_by_name("q")

# После этого мы посылаем нажатия клавиш (аналогично введению клавиш с клавиатуры). Специальные команды могут быть переданы с помощью класса Keys импортированного из selenium.webdriver.common.keys
# inputElement.send_keys(Keys.RETURN)

# набираем строку поиска
inputElement.send_keys("cheese!")

# сабмитим форму (обычно google автоматически выполняет поиск без submitting)
inputElement.submit()

# После ответа страницы, вы получите результат, если таковой ожидается. Чтобы удостовериться, что мы получили какой-либо результат, добавим утверждение:

# assert "No results found." not in driver.page_source

try:
    # ждем обновления страницы, ждем обновления title
    WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

    # Должны увидеть "cheese! - Поиск в Google"
    print (driver.title)

# В завершение, окно браузера закрывается. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью:
finally:
    driver.quit()
```

python test.py 
--------------
```
Google
cheese! - Пошук Google

```
## Selenium для написания тестов
Selenium чаще всего используется для написания тестовых ситуаций. Сам пакет selenium не предоставляет никаких тестовых утилит или инструментов разработки. Вы можете писать тесты с помощью модуля Python unittest. Другим вашим выбором в качестве тестовых утилит/инструментов разработки могут стать py.test и nose.

### тесты с помощью модуля Python unittest
Данный скрипт тестирует функциональность поиска на сайте www.google.com:

test_search.py
```
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Сначала были импортированы все основные необходимые модули. Модуль unittest встроен в Python и реализован на Java’s JUnit. Этот модуль предоставляет собой утилиту для организации тестов.

# Класс теста унаследован от unittest.TestCase. Наследование класса TestCase является способом сообщения модулю unittest, что это тест:

class PythonOrgSearch(unittest.TestCase):

# setUp — это часть инициализации, этот метод будет вызываться перед каждым методом теста, который вы собираетесь написать внутри класса теста. Здесь мы создаем элемент класса Firefox WebDriver.

    def setUp(self):
        self.driver = webdriver.Firefox()

# Метод теста всегда должен начинаться с фразы test. Первая строка метода создает локальную ссылку на объект драйвера, созданный методом setUp.

    def test_search_in_python_org(self):
        driver = self.driver

        # Метод driver.get перенаправляет к странице URL в параметре. WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. 

        driver.get("http://www.google.com")

        # утверждение, что заголовок содержит слово “Google”:

        self.assertIn("Google", driver.title)
        
        # WebDriver предоставляет ряд способов получения элементов с помощью методов find_element_by_*. Для примера, элемент ввода текста input может быть найден по его атрибуту name методом find_element_by_name. 

        elem = driver.find_element_by_name("q")

        # После этого мы посылаем нажатия клавиш (аналогично введению клавиш с клавиатуры). Специальные команды могут быть переданы с помощью класса Keys импортированного из selenium.webdriver.common.keys:

        elem.send_keys("django")

        # После ответа страницы, вы получите результат, если таковой ожидается. Чтобы удостовериться, что мы получили какой-либо результат, добавим утверждение:

        assert "No results found." not in driver.page_source
        elem.send_keys(Keys.RETURN)

    # Метод tearDown будет вызван после каждого метода теста. Это метод для действий чистки. В текущем методе реализовано закрытие окна браузера. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью.:

    def tearDown(self):
        self.driver.close()

# Завершающий код — это стандартная вставка кода для запуска набора тестов [Сравнение __name__ с "__main__" означает, что модуль (файл программы) запущен как отдельная программа («main» — «основная», «главная») (а не импортирован из другого модуля). Если вы импортируете модуль, атрибут модуля __name__ будет равен имени файла без каталога и расширения.]:

if __name__ == "__main__":
    unittest.main()
```

запустить тест python test_search.py 
------------------------------------
```
python test_search.py 
.
----------------------------------------------------------------------
Ran 1 test in 9.733s

OK
```
тест завершился успешно

django-admin startproject mysite

```
-- mysite
    |-- manage.py
    `-- mysite
        |-- __init__.py
        |-- settings.py
        |-- urls.py
        `-- wsgi.py
```
## Наш первый functional test:
```
cd mysite
mkdir f_test
cd f_test/
touch test0.py
```
test0.py
--------
```
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title

```
python test0.py 
---------------
```
Traceback (most recent call last):
  File "test0.py", line 7, in <module>
    assert 'Django' in browser.title
AssertionError
```
python manage.py runserver
--------------------------
```
./manage.py runserver

Performing system checks...

System check identified no issues (0 silenced).
January 20, 2016 - 11:05:08
Django version 1.9.1, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.


```
python test0.py 
---------------
## Наш первый functional test для нашего сайта: 

test1.py
--------
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title

print (browser.title)

try:
    
    WebDriverWait(browser, 10).until(EC.title_contains("Welcome"))

    # You should see "Welcome to Django This is my cool Site!"
    print (browser.title,' This is my cool Site!')

finally:
    browser.quit()
```
python test1.py 
---------------
```
Welcome to Django
Welcome to Django  This is my cool Site!

```
Selenium WebDriver – это спецификация интерфейса для управления браузером
--------------------------------------------------------------------------
WebDriver – это драйвер браузера, то есть не имеющая пользовательского интерфейса программная библиотека, которая позволяет различным другим программам взаимодействовать с браузером, управлять его поведением, получать от браузера какие-то данные и заставлять браузер выполнять какие-то команды.

Исходя из этого определения, ясно, что WebDriver не имеет прямого отношения к тестированию. Он всего лишь предоставляет автотестам доступ к браузеру. 

Самое главное отличие WebDriver от всех остальных драйверов заключается в том, что это «стандартный» драйвер, а все остальные – «нестандартные».

Организация W3C действительно приняла WebDriver за основу при разработке стандарта интерфейса для управления браузером.

реализация интерфейса WebDriver возложена на производителей браузеров.

В рамках проекта Selenium было разработано несколько референсных реализаций для различных браузеров, но постепенно эта деятельность переходит в ведение производителей браузеров. Драйвер для браузера Chrome разрабатывается в рамках проекта Chromium, его делает та же команда, которая занимается разработкой самого браузера. Драйвер для браузера Opera разрабатывается в компании Opera Software. Драйвер для браузера Firefox разрабатывается участниками проекта Selenium, но в недрах компании Mozilla уже готовится ему замена, которая носит кодовое название Marionette. Этот новый драйвер для Firefox уже доступен в девелоперских сборках браузера. На очереди Internet Explorer и Safari, к их разработке сотрудники соответствующих компаний пока не подключились.

В общем, можно сказать, что Selenium это единственный проект по созданию средств автоматизации управления браузерами, в котором участвуют непосредственно компании, разрабатывающие браузеры. 

ChromeDriver - WebDriver for Chrome
-----------------------------------
https://sites.google.com/a/chromium.org/chromedriver/getting-started
```
import time
from selenium import webdriver

driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/xhtml');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
```
Controlling ChromeDriver's lifetime
-----------------------------------
```
import time

from selenium import webdriver
import selenium.webdriver.chrome.service as service

service = service.Service('/path/to/chromedriver')
service.start()
capabilities = {'chrome.binary': '/path/to/custom/chrome'}
driver = webdriver.Remote(service.service_url, capabilities)
driver.get('http://www.google.com/xhtml');
time.sleep(5) # Let the user actually see something!
driver.quit()
```

# Functional Test == Acceptance Test == End-to-End Test

test_hello.py
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'This is my cool Site!' in browser.title

print (browser.title)

try:
    
    WebDriverWait(browser, 10).until(EC.title_contains("Site"))
 
    print (browser.title)

finally:
    browser.quit()

```
python test_hello.py 
```
Traceback (most recent call last):
  File "test_hello.py", line 9, in <module>
    assert 'This is my cool Site!' in browser.title
AssertionError
```
test_welcome.py 
```
# Сначала были импортированы все основные необходимые модули. Модуль unittest встроен в Python и реализован на Java’s JUnit. Этот модуль предоставляет собой утилиту для организации тестов.

from selenium import webdriver
import unittest

# Класс теста унаследован от unittest.TestCase. Наследование класса TestCase является способом сообщения модулю unittest, что это тест:

class NewVisitorTest(unittest.TestCase):  

    # setUp — это часть инициализации, этот метод будет вызываться перед каждым методом теста, который вы собираетесь написать внутри класса теста. Здесь мы создаем элемент класса Firefox WebDriver.

    def setUp(self):  
        self.browser = webdriver.Firefox()

    # Метод tearDown будет вызван после каждого метода теста. Это метод для действий чистки. В текущем методе реализовано закрытие окна браузера. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью.:

    def tearDown(self):  
        self.browser.quit()

    # Метод теста всегда должен начинаться с фразы test. Первая строка метода создает локальную ссылку на объект драйвера, созданный методом setUp.
    
    def test_can_start_a_list_and_retrieve_it_later(self):  
        
        # Метод driver.get перенаправляет к странице URL в параметре. WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. 

        self.browser.get('http://localhost:8000')
        
        # утверждение, что заголовок содержит слово “This is my cool Site!”:
        self.assertIn('This is my cool Site!', self.browser.title)  
        
        # self.fail ничего не получилось, генерирует сообщение об ошибке. Используется в качестве напоминания, чтобы закончить тест.

        self.fail('Finish the test!')  
            
# Завершающий код — это стандартная вставка кода для запуска набора тестов [Сравнение __name__ с "__main__" означает, что модуль (файл программы) запущен как отдельная программа («main» — «основная», «главная») (а не импортирован из другого модуля). Если вы импортируете модуль, атрибут модуля __name__ будет равен имени файла без каталога и расширения.]:

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  
```
warnings='ignore' подавляет избыточные предупреждения ResourceWarning,  которые генерируются в момент выполнения. 


python test_welcome.py 
```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_welcome.py", line 30, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('This is my cool Site!', self.browser.title)
AssertionError: 'This is my cool Site!' not found in 'Welcome to Django'

----------------------------------------------------------------------
Ran 1 test in 6.324s

FAILED (failures=1)

```
# Implicit waits - Неявные ожидания
добавить implicitly_wait в настройки setUp:

```
    def setUp(self):  
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

```
all_users.py
-------------
```
# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest
 
class NewVisitorTest(unittest.TestCase):
 
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
 
    def tearDown(self):
        self.browser.quit()
 
    def test_it_worked(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Welcome to Django', self.browser.title)
 
if __name__ == '__main__':
    unittest.main(warnings='ignore')
```
python all_users.py 
-------------------
```
.
----------------------------------------------------------------------
Ran 1 test in 6.368s
OK
```

./manage.py startapp home
--------------------------
```
mysite/
├── db.sqlite3
├── f_tests.py
├── home
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
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

## Unit Tests

Основное различие между юнит-тестами и функциональными тестами является то, что функциональные тесты используются для тестирования приложения с точки зрения пользователя. Модульные тесты используются для тестирования приложения с точки зрения программиста.

TDD подход будет выглядеть так:
-------------------------------
- Начнем с написания функциональных тестов, описывая новые возможности с точки зрения пользователя.
- После того, как у нас есть функциональный тест, который не удается, мы начинаем думать о том, как написать код, который может заставить его пройти (или по крайней мере пройти его нынешнем недостаточности). Сейчас мы используем один или несколько юнит-тестов, чтобы определить, как должен вести себя наш код.
- После того, как у нас есть модульный тест и он не проходит, мы пишем некоторое количество кода приложения, достаточное чтобы пройти модульный тест. Мы можем повторять шаги 2 и 3 несколько раз, пока не получим желаемое.
Теперь мы можем повторно вызвать наши функциональные тесты и посмотреть, проходят ли они. 

# Unit Testing in Django

home/test.py

```
from django.test import TestCase

# Create your tests here.
```
home/test.py
------------
```
from django.test import TestCase

# Create your tests here.
class EqualTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
```
./manage.py test      
```
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_bad_maths (home.tests.EqualTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/home/tests.py", line 7, in test_bad_maths
    self.assertEqual(1 + 1, 3)
AssertionError: 2 != 3

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
Destroying test database for alias 'default'..

```
Static Files Settings
=====================
Settings file (settings.py)
---------------------------
```
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    
    'django.contrib.staticfiles',
]
```

Static files (CSS, JavaScript, Images)
---------------------------------------
```
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
```

STATICFILES DIR
---------------
```
mkdir static
```

settings.py:
------------
```
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

STATICFILES_DIRS:
-----------------
```
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
```
Templates Settings
------------------
```
mkdir templates
```
Templates files
---------------
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                 django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Initializr: HTML5 Boilerplate and Twitter Bootstrap
---------------------------------------------------
http://www.initializr.com/

После загрузки и распаковки:
----------------------------
- Переместить index.html, 404.html, humans.txt и robots.txt в templates folder.
- Переименовать index.html в base.html. 
- Остальные файлы переместить в static
- Создайте свой favicon.ico.
- Можно удалить файлы apple-touch-icon.png, browserconfig.xml, tile-wide.png и tile.png.


# Django MVC, URLs, and View Functions

### Рабочий процесс в Django:

- HTTP-запрос приходит на определенной URL.
- Django использует некоторые правила и решает, какой метод контроллера должен откликнуться на запрос (это называется разрешением URL).
- Метод контроллера обрабатывает запрос и возвращает ответ HTTP.

Проверим две идеи:
------------------
- Можем ли мы разрешить URL для корня сайта ("/") и в каком методе это сделать?
- Может ли метод вернуть некоторый HTML, который получит функциональный тест?

home/tests.py. 
--------------
```
from django.core.urlresolvers import resolve
from django.test import TestCase
from home.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, home_page)  

```

При вызове "/"(корень сайта), Django находит метод с именем home_page.

Этот метод мы напишем позже. Мы планируем сохранить его в home/views.py.

home/views.py. 
```
from django.shortcuts import render

# Create your views here.
home_page = None

```
./manage.py test
```
Creating test database for alias 'default'...
FE
======================================================================
ERROR: test_root_url_resolves_to_home_page_view (home.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/home/tests.py", line 9, in test_root_url_resolves_to_home_page_view
    found = resolve('/')
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 534, in resolve
    return get_resolver(urlconf).resolve(path)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 404, in resolve
    raise Resolver404({'tried': tried, 'path': new_path})
django.core.urlresolvers.Resolver404: {'tried': [[<RegexURLResolver <RegexURLPattern list> (admin:admin) ^admin/>]], 'path': ''}

```
## urls.py

mysite/urls.py. 
```
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]


```
mysite/urls.py. 
```
from django.conf.urls import include, url
from django.contrib import admin

from home import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^admin/', include(admin.site.urls)),
]
```
./manage.py test
```
Creating test database for alias 'default'...
FE
======================================================================
ERROR: test_root_url_resolves_to_home_page_view (home.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/home/tests.py", line 9, in test_root_url_resolves_to_home_page_view
    found = resolve('/')
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 534, in resolve
    return get_resolver(urlconf).resolve(path)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 376, in resolve
    sub_match = pattern.resolve(new_path)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 248, in resolve
    return ResolverMatch(self.callback, args, kwargs, self.name)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 255, in callback
    self._callback = get_callable(self._callback_str)
  File "/home/janus/Envs/dj21/lib/python3.4/functools.py", line 448, in wrapper
    result = user_function(*args, **kwds)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 102, in get_callable
    "'%s' is not a callable or a dot-notation path" % lookup_view
django.core.exceptions.ViewDoesNotExist: 'None' is not a callable or a dot-notation path

```

home/views.py. 
--------------
```
from django.shortcuts import render

# Create your views here.
def home_page():
    pass
```

./manage.py test
```
Creating test database for alias 'default'...
..
----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK
Destroying test database for alias 'default'...
```

## Unit Test метод

home/test_1.py. 
```
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from home.views import home_page 

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') 
        self.assertEqual(found.func, home_page) 

    def test_home_page_returns_correct_html(self):

        # создали HttpRequest object, который использует Django когда пользователь запрашивает страницу.

        request = HttpRequest()  
        
        # перенаправляем запрос на метод home_page view, который формирует response - экземпляр класса HttpResponse. Далее проверяем является ли .content в response HTML-текстом который мы отдаем пользователю.

        response = home_page(request)  
        
        # HTML-текст должен начинаться с html тега, который должен закрываться вконце. response.content является сырым литералом (raw bytes), а не Python-строкой, поэтому мы используем b'' синтаксис.

        self.assertTrue(response.content.startswith(b'<html>'))  
        
        # Мы хотим поместить тег title, содержащий наш заголовок.

        self.assertIn(b'<title>Welcome to Django. This is my cool Site!</title>', response.content)  
        self.assertTrue(response.content.endswith(b'</html>'))  


class EqualTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 2)
```

./manage.py test

```
Creating test database for alias 'default'...
ERROR: test_home_page_returns_correct_html (home.test_1.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/home/test_1.py", line 22, in test_home_page_returns_correct_html
    response = home_page(request)
TypeError: home_page() takes 0 positional arguments but 1 was given
```

home/views.py. 
--------------
```
def home_page(request):
    pass
```
./manage.py test
```
ERROR: test_home_page_returns_correct_html (home.test_1.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/home/test_1.py", line 26, in test_home_page_returns_correct_html
    self.assertTrue(response.content.startswith(b'<html>'))
AttributeError: 'NoneType' object has no attribute 'content'
```
home/views.py. 
```
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    return HttpResponse()
```

./manage.py test
```
FAIL: test_home_page_returns_correct_html (home.test_1.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/home/test_1.py", line 26, in test_home_page_returns_correct_html
    self.assertTrue(response.content.startswith(b'<html>'))
AssertionError: False is not true

```

home/views.py. 

```
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):

    return HttpResponse("<html><title>Welcome to Django. This is my cool Site!</title>")

```

./manage.py test
```
FAIL: test_home_page_returns_correct_html (home.test_1.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/home/test_1.py", line 31, in test_home_page_returns_correct_html
    self.assertTrue(response.content.endswith(b'</html>'))
AssertionError: False is not true

```

home/views.py. 
--------------
```
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):

    return HttpResponse("<html><title>Welcome to Django. This is my cool Site!</title></html>")

```
./manage.py test
```
Creating test database for alias 'default'...
.....
----------------------------------------------------------------------
Ran 5 tests in 0.003s

OK
Destroying test database for alias 'default'...
```
functional tests
-----------------
```
touch f_tests/__init__.py
```
- Все файлы тестов должны начинаться с test, например test_all_users.py.

- Тестируем заголовок на совпадение с “My Cool Django Site”
- Тестируем цвет h1 header в home page на совпадение с rgba(200, 50, 255, 1) ~ pink color.

test_all_users.py:
-------------------
```
# -*- coding: utf-8 -*-
from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase  
 
 
class HomeNewVisitorTest(LiveServerTestCase): 
 
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
 
    def tearDown(self):
        self.browser.quit()
 
    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)
 
    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("My Cool Django Site", self.browser.title)
 
    def test_h1_css(self):
        self.browser.get(self.get_full_url("home"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"), 
                         "rgba(200, 50, 255, 1)")
```

Шаг за шагом:
--------------
1. Определили function named get_full_url, принимающую 1 аргумент - namespace
namespace определен в url. 
2. self.live_server_url определяет local host url. Нужно из-за того, что server использует другой url (обычно http://127.0.0.1:8021).
3. reverse дает похлдящий url для указанного namespace, именно - /
4. test_home_title  method проверяет что home page title содержит "My Cool Django Site".
5. test_h1_css method тестирут color. 

```
./manage.py test f_test
------------------------
```
E.F
======================================================================
ERROR: test_h1_css (f_test.test_all_users.HomeNewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/f_test/test_all_users.py", line 25, in test_h1_css
    h1 = self.browser.find_element_by_tag_name("h1")
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/selenium/webdriver/remote/webdriver.py", line 354, in find_element_by_tag_name
    return self.find_element(by=By.TAG_NAME, value=name)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/selenium/webdriver/remote/webdriver.py", line 712, in find_element
    {'using': by, 'value': value})['value']
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/selenium/webdriver/remote/webdriver.py", line 201, in execute
    self.error_handler.check_response(response)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/selenium/webdriver/remote/errorhandler.py", line 188, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: {"method":"tag name","selector":"h1"}

```
Цикл TDD:
---------

home/test.py:
-------------
```
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
 
 
class TestHomePage(TestCase):
 
    def test_uses_index_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/index.html")
 
    def test_uses_base_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base.html")

``` 
 
./manage.py test home.test
----------------------------
```
FAIL: test_uses_base_template (home.test.TestHomePage)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/home/test.py", line 14, in test_uses_base_template
    self.assertTemplateUsed(response, "base.html")
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/test/testcases.py", line 579, in assertTemplateUsed
    self.fail(msg_prefix + "No templates used to render the response")
AssertionError: No templates used to render the response

======================================================================
FAIL: test_uses_index_template (home.test.TestHomePage)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/dj-21v/unit_02/mysite/home/test.py", line 10, in test_uses_index_template
    self.assertTemplateUsed(response, "home/index.html")
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/test/testcases.py", line 579, in assertTemplateUsed
    self.fail(msg_prefix + "No templates used to render the response")
AssertionError: No templates used to render the response

----------------------------------------------------------------------
```

urls.py
--------
```
rlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
]
```
home/views.py
-------------
```
 
def home(request):
    return render(request, "home/index.html", {})
```
templates/home
---------------
```
mkdir templates/home
touch templates/home/index.html
```
base.html
----------
```
<title>{% block head_title %}{% endblock %}</title>

```
home/index.html
---------------
```
{% extends "base.html" %}
{% block head_title %}My Cook Django Site{% endblock %}
```
./manage.py test home.test
---------------------------
```
Creating test database for alias 'default'...
..
----------------------------------------------------------------------
Ran 2 tests in 0.033s

OK
Destroying test database for alias 'default'...
```
static/css/main.css
-------------------
```
.jumbotron h1 {
    color: rgba(200, 50, 255, 1);
}
```
base.html:
----------
```
{% load staticfiles %}
<!DOCTIPE html> 
```
static files
------------
Заменить
```
    <link rel="stylesheet" href="css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="css/main.css">
```
на
```
    <link rel="stylesheet" href="{% static 'css/bootstrap-theme.min.css' %}">
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
```
Заменить
```
    <script src="js/vendor/modernizr-2.8.3-respond-1.4.2.min.js"></script>
```
на
```
    <script src="{% static 'js/vendor/modernizr-2.8.3-respond-1.4.2.min.js' %}">
```
Заменить
```
    <script src="js/main.js"></script>
    <script src="js/plugins.js"></script>
```
на
```
    <script src="{% static 'js/main.js' %}">
    <script src="{% static 'js/plugins.js' %}">
```
Заменить
```
    <script src="js/vendor/bootstrap.min.js"></script>
```
на
```
    <script src="{% static 'js/vendor/bootstrap.min.js' %}">
```
Но
--
```
document.write('<script src="js/vendor/jquery-1.11.0.min.js"><\/script>')</script>
```
заменить на
```
document.write('<script src="static/js/vendor/jquery-1.11.0.min.js"><\/script>')</script>
```

