# dj-21v

Уровень модели User
===================

    $ python manage.py startapp authentication

## Account model

authentication/models.py:
--------------------------
    from django.contrib.auth.models import AbstractBaseUser
    from django.db import models

    @python_2_unicode_compatible
    class Account(AbstractBaseUser):
        email = models.EmailField(unique=True)
        username = models.CharField(max_length=40, unique=True)

        first_name = models.CharField(_('first name'),max_length=40, blank=True)
        last_name = models.CharField(_('last name'),max_length=40, blank=True)
        tagline = models.CharField(max_length=140, blank=True)

        is_admin = models.BooleanField(default=False)

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        objects = AccountManager()

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username']

        def __str__(self):
            return self.email

        def get_full_name(self):
            return ' '.join([self.first_name, self.last_name])

        def get_short_name(self):
            return self.first_name


встроенный User требуется имя пользователя. Это имя пользователя используется для входа пользователя в систему. В отличие от этого, наше приложение будет использовать адрес электронной почты пользователя для этой цели.

мы хотим обработать поле электронной почты в качестве имени пользователя для этой модели, поэтому устанавливаем атрибут USERNAME_FIELD в email. Поле SERNAME_FIELD должно быть уникальным, поэтому мы передаем unique=True аргумент в поле электронной почты.

    email = models.EmailField(unique=True)

    # ...

    USERNAME_FIELD = 'email'

tagline атрибут будет отображаться в профиле пользователя. Это hint на личность пользователя.

    tagline = models.CharField(max_length=140, blank=True)

created_at поле - записывает время, когда был создан объект Account. Установив в models.DateTimeField auto_now_add = true, мы говорим, что это поле должно быть автоматически установлено когда объект создается и не редактируется после этого.

updated_at автоматически устанавливается Джанго. Разница между auto_now_add = true и auto_now = true является то, что auto_now = true вызывает поле для обновления каждый раз, когда объект будет сохранен.


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

Если вы хотите получить экземпляр модели в Django, вы используете выражение вида Model.objects.get (** kwargs). Objects атрибут здесь является  Manager класс, где имя, согласно соглашению, задают так - имямоделиManager. В нашем случае, мы создадим класс `AccountManager`. 

    objects = AccountManager()

Мы будем отображать имя пользователя в нескольких местах. Т.к. имея имя пользователя не является обязательным - включили его в список REQUIRED_FIELDS. 


    REQUIRED_FIELDS = ['username']

Перезагрузка __str__ - строка по умолчанию представления объекта Account. 

    def __str__(self):
        return self.email

Get_full_name() и get_short_name () - включаем их в соответствие с соглашением Django.

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name


## Создание класса диспетчера для учетной записи

В кастомной моделе требуется переопределить create_user() и create_superuser() методы класса.
authentication/models.py:
-------------------------

    from django.contrib.auth.models import BaseUserManager


    class AccountManager(BaseUserManager):
        def create_user(self, email, password=None, **kwargs):
            if not email:
                raise ValueError(_('Users must have a valid email address.'))

            if not kwargs.get('username'):
                raise ValueError(_('Users must have a valid username.'))

            account = self.model(
                email=self.normalize_email(email), username=kwargs.get('username')
            )

            account.set_password(password)
            account.save()

            return account

        def create_superuser(self, email, password, **kwargs):
            account = self.create_user(email, password, **kwargs)

            account.is_admin = True
            account.save()

            return account

Поскольку пользователи должны иметь как адрес электронной почты так и имя пользователя, мы должны выбросить ошибку, если любого из этих атрибутов не хватает.

    if not email:
        raise ValueError(_('Users must have a valid email address.'))

    if not kwargs.get('username'):
        raise ValueError(_('Users must have a valid username.'))

self.model наследуется от BaseUserManager. Значение по умолчанию задем в settings.AUTH_USER_MODEL.

    account = self.model(
        email=self.normalize_email(email), username=kwargs.get('username')
    )

Вместо того чтобы копировать весь код из create_account и вставлять его в create_superuser, мы просто наследум create_user. create_superuser отвечает только за превращение Account в привилегированный режим.


    account = self.create_account(email, password, **kwargs)

    account.is_admin = True
    account.save()


## Изменение настройки Django AUTH_USER_MODEL

Django по-прежнему считает, что User - это модель, которую мы хотим использовать для проверки подлинности.

Для того, чтобы начать использовать Account в нашей модели аутентификации, мы должны изменить settings.AUTH_USER_MODEL.

settings.py:
------------
    AUTH_USER_MODEL = 'authentication.Account'


## Installing authentication

settings.py:

    INSTALLED_APPS = (
        ...,
        'authentication',
    )


## Migrating

    $ python manage.py makemigrations authentication
    $ python manage.py migrate


## superuser

    $ python manage.py createsuperuser


## Checkpoint

    $ python manage.py shell

    >>> from authentication.models import Account
    >>> a = Account.objects.latest('created_at')

    >>> a
    >>> a.email
    >>> a.username



API на Django Rest Framework
=============================

Django Rest Framework предоставляет готовую архитектуру для разработки как простых RESTful API, так и более сложных конструкций. Его ключевая особенность, это четкое разделение на сериализаторы, которые описывают соответствие между моделью и ее форматом представления (будь то JSON, XML или любой другой формат), и на отдельный набор универсальных представлениях на основе классов (Class-Based-Views), которые могут быть по необходимости расширены. Вы так же можете определить свою ссылочную структуру, вместо использования дефолтной. Это то, что отличает Django Rest Framework от других фреймворков, таких как Tastypie и Piston, которые автоматизируют формировнаие API на основе моделей, но это происходит за счет снижения гибкости и применимости к различным нестандартным требованиям (особенно, если речь идет о доступах и вложенных ресурсах).

http://www.django-rest-framework.org/

Requirements
-------------
REST framework requires the following:

    Python (2.7, 3.2, 3.3, 3.4, 3.5)
    Django (1.7+, 1.8, 1.9)
The following packages are optional:

    Markdown (2.1.0+) - Markdown support for the browsable API.
    django-filter (0.9.2+) - Filtering support.
    django-crispy-forms - Improved HTML display for filtering.
    django-guardian (1.1.1+) - Object level permissions support.

Installation
-------------

    pip install djangorestframework
    pip install markdown       # Markdown support for the browsable API.
    pip install django-filter  # Filtering support

...or clone the project from github.

    git clone git@github.com:tomchristie/django-rest-framework.git

INSTALLED_APPS setting.
-----------------------

    INSTALLED_APPS = (
        ...
        'rest_framework',
    )


Сериализаторы моделей
======================
Сериализаторы в Django Rest Framework предназначены для преобразования экземпляров django-модели в API представление. Это дает нам возможность конвертировать любые типы данных, или предоставлять дополнительную информацию о данной модели. 

Сильной стороной сериализаторов является то, что их можно расширить для создания дополнительных версий.

С помощью AngularJS мы будем строить AJAX запросы к серверу, чтобы получить данные, которые он бутет отображать. Прежде чем мы сможем отправить эти данные обратно клиенту, нам нужно отформатировать их таким образом, чтобы клиент мог их понять; мы выбираем JSON. Процесс трансформации модели Django в формате JSON называется сериализацией.

В качестве модели мы хотим сериализовать Account, наш сериализатор будет называться  AccountSerializer.


## AccountSerializer

    $ touch authentication/serializers.py


authentication/serializers.py:
------------------------------
    from django.contrib.auth import update_session_auth_hash

    from rest_framework import serializers

    from authentication.models import Account


    class AccountSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True, required=False)
        confirm_password = serializers.CharField(write_only=True, required=False)

        class Meta:
            model = Account
            fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                      'first_name', 'last_name', 'tagline', 'password',
                      'confirm_password',)
            read_only_fields = ('created_at', 'updated_at',)

            def create(self, validated_data):
                return Account.objects.create(**validated_data)

            def update(self, instance, validated_data):
                instance.username = validated_data.get('username', instance.username)
                instance.tagline = validated_data.get('tagline', instance.tagline)

                instance.save()

                password = validated_data.get('password', None)
                confirm_password = validated_data.get('confirm_password', None)

                if password and confirm_password and password == confirm_password:
                    instance.set_password(password)
                    instance.save()

                update_session_auth_hash(self.context.get('request'), instance)

                return instance


явно определим поле password в верхней части AccountSerializer класса. Причина, почему мы делаем это, чтобы мы могли передать required=False аргумент. Каждое поле в fields обязятельно, но мы не хотим обновить пароль пользователя, если он не задал новый.

confirm_password похож на password и используется только чтобы убедиться, что пользователь не сделал опечатку.

write_only = true аргумент
--------------------------
Пароль пользователя не должен быть виден клиенту в ответе AJAX.

    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

Meta суб-класс определяет метаданные сериализатора.

    class Meta:

Поскольку этот сериализатор наследуется от serializers.ModelSerializer, мы должны сказать ему  какая модель используется для сериализации. Указание модели создает гарантию того, что только атрибуты этой модели или явно созданные поля могут быть упорядочены. 

    model = Account

Fields атрибут класса Meta где мы указываем, какие атрибуты модели Account должны быть упорядочены. Мы должны быть осторожны при определении полей для сериализации, потому что некоторые поля, такие как is_superuser, не должны быть доступны клиенту по соображениям безопасности.

    fields = ('id', 'email', 'username', 'created_at', 'updated_at',
              'first_name', 'last_name', 'tagline', 'password',
              'confirm_password',)


Благодаря этой функции, мы добавим created_at и updated_at поля в список полей, которые должны быть только для чтения.

    read_only_fields = ('created_at', 'updated_at',)

мы хотим превратить JSON в объект Python. Это называется десериализация и обрабатывается с помощью .create() и .update() методов. При создании нового объекта Account, используется .create(). При обновлении Account, используется .update().

    def create(self, validated_data):
        # ...

    def update(self, instance, validated_data):
        # ...

Предложим пользователю обновлять свои имя пользователя и атрибуты. Если эти ключи присутствуют в словаре, мы будем использовать новое значение. В противном случае, используется текущее значение объекта instance. Здесь instance имеет тип Account.

    instance.username = validated_data.get('username', instance.username)
    instance.tagline = validated_data.get('tagline', instance.tagline)

Перед обновлением пароля пользователя, мы должны подтвердить, что он предоставил значения и для ` password и для password_confirmation полей. Затем мы проверяем, что эти два поля имеют equivelant значения.

После того, как мы убедились, что пароль должен быть обновлен, мы используем Account.set_password() для выполнения обновления. Account.set_password() заботится о хранении паролей в защищенном режиме. Важно отметить, что мы должны явно сохранить модель после обновления пароля.


    password = validated_data.get('password', None)
    confirm_password = validated_data.get('confirm_password', None)

    if password and confirm_password and password == confirm_password:
        instance.set_password(password)
        instance.save()

Когда пароль пользователя обновляется, его хэш сеанса аутентификации должен быть явно обновлен. Если мы не будем этого делать, то пользователь не будет проходить проверку подлинности при следующем запросе, и ему придется снова войти в систему.

    update_session_auth_hash(self.context.get('request'), instance)


## Checkpoint

    >>> from authentication.models import Account
    >>> from authentication.serializers import AccountSerializer
    >>> account = Account.objects.latest('created_at')
    >>> serialized_account = AccountSerializer(account)
    >>> serialized_account.data.get('email')
    >>> serialized_account.data.get('username')


# Регистрация новых пользователей

## Создание учетной записи API Viewset

authentication/views.py:
------------------------

    from rest_framework import permissions, viewsets

    from authentication.models import Account
    from authentication.permissions import IsAccountOwner
    from authentication.serializers import AccountSerializer


    class AccountViewSet(viewsets.ModelViewSet):
        lookup_field = 'username'
        queryset = Account.objects.all()
        serializer_class = AccountSerializer

        def get_permissions(self):
            if self.request.method in permissions.SAFE_METHODS:
                return (permissions.AllowAny(),)

            if self.request.method == 'POST':
                return (permissions.AllowAny(),)

            return (permissions.IsAuthenticated(), IsAccountOwner(),)

        def create(self, request):
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                Account.objects.create_user(**serializer.validated_data)

                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

            return Response({
                'status': 'Bad request',
                'message': 'Account could not be created with received data.'
            }, status=status.HTTP_400_BAD_REQUEST)



Django REST Framework предлагает функцию под названием viewsets. Viewset, как следует из названия, представляет собой набор представлений. В частности, ModelViewSet предлагает интерфейс для просмотра, создания, извлечения, обновления и уничтожения объектов данной модели.

    class AccountViewSet(viewsets.ModelViewSet):

Здесь мы определяем query set и serialzier, с которыми Viewset будет работать дальше. Django REST Framework использует указанный QuerySet и serialzier для выполнения действия, перечисленные выше. Также отметим, что мы указываем lookup_field  атрибут. мы будем использовать username атрибут модели Account для поиска вместо id атрибута. 

    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

Единственный пользователь, который может вызывать опасные методы (такие как update() и delete()) является владельцем account. Сначала мы проверяем прошел ли проверку подлинности пользователь, а затем применять пользовательские разрешения. Этот случай не имеет места, когда метод HTTP является Post. Мы хотим разрешить любому пользователю создать учетную запись.

Если метод HTTP запроса ('GET', 'POST', и т.д.) является "безопасным", то любой человек может использовать этот сервис.

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

При создании объекта с помощью сериализатора в .save() методе, атрибуты объекта устанавливаются литерально. Это означает, что пользователь при регистрации с паролем password будет хранить свой пароль в виде password. Это плохо по нескольким причинам: 1) Сохранение паролей в виде обычного текста - это огромная проблема безопасности. 2) Django хэшит и солит пароли, прежде чем сравнивать их, так что пользователь не сможет войти в систему с помощью password в качестве пароля.

Перекроим .create() метод, используя Account.objects.create_user() для создания объекта Account.

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


## Создание IsAccountOwner permission

authentication/permissions.py:
------------------------------

    from rest_framework import permissions


    class IsAccountOwner(permissions.BasePermission):
        def has_object_permission(self, request, view, account):
            if request.user:
                return account == request.user
            return False

Если есть пользователь, связанный с текущим запросом, проверяем что request.user - тот же объект, что и account. Если нет, просто возвращаем `false`.

Nested Routers for Django Rest Framework
========================================
https://github.com/alanjds/drf-nested-routers

You can install this library using pip:
```
pip install drf-nested-routers
```
## Добавляем API

urls.py:
--------
    # .. Imports
    from rest_framework_nested import routers

    from authentication.views import AccountViewSet

    router = routers.SimpleRouter()
    router.register(r'accounts', AccountViewSet)

    urlpatterns = patterns(
         '',
        # ... URLs
        url(r'^api/v1/', include(router.urls)),

        url('^.*$', IndexView.as_view(), name='index'),
    )


## Angular service для регистрации нового пользователя
Создаем AngularJS service который создаст связь между слиентом и сервером.
angularjs_authentication_service
--------------------------------
Создаем в static/js/authentication/services/ файл authentication.service.js:

    /**
    * Authentication
    * @namespace restblog.authentication.services
    */
    (function () {
      'use strict';

      angular
        .module('restblog.authentication.services')
        .factory('Authentication', Authentication);

      Authentication.$inject = ['$cookies', '$http'];

      /**
      * @namespace Authentication
      * @returns {Factory}
      */
      function Authentication($cookies, $http) {
        /**
        * @name Authentication
        * @desc The Factory to be returned
        */
        var Authentication = {
          register: register
        };

        return Authentication;

        ////////////////////

        /**
        * @name register
        * @desc Try to register a new user
        * @param {string} username The username entered by the user
        * @param {string} password The password entered by the user
        * @param {string} email The email entered by the user
        * @returns {Promise}
        * @memberOf restblog.authentication.services.Authentication
        */
        function register(email, password, username) {
          return $http.post('/api/v1/accounts/', {
            username: username,
            password: password,
            email: email
          });
        }
      }
    })();


AngularJS поддерживает использование модулей. Определяем restblog.authentication.services модуль.

    angular
      .module('restblog.authentication.services')

Регистрируем factory с именем Authentication в млдуле. 

    .factory('Authentication', Authentication);

Определяем factory, которую зарегистрировали. Инжектим $cookies и $http серисы как дополнительные.

    function Authentication($cookies, $http) {

Персональные установки. 

    var Authentication = {
      register: register
    };

method: register получает `username`, `password` и `email`.

    function register (username, password, email) {

Создаем AJAX request к API. Передаваемые данные data включают `username`, `password` и `email` параметры, которые получит метод. 

    return $http.post('/api/v1/accounts/', {
      username: username,
      password: password,
      email: email
    });


## Создание интерфейса для регистрации

static/templates/authentication/register.html: 
-----------------------------------------------

    <div class="row">
      <div class="col-md-4 col-md-offset-4">
        <h1>Register</h1>

        <div class="well">
          <form role="form" ng-submit="vm.register()">
            <div class="form-group">
              <label for="register__email">Email</label>
              <input type="email" class="form-control" id="register__email" ng-model="vm.email" placeholder="ex. john@notgoogle.com" />
            </div>

            <div class="form-group">
              <label for="register__username">Username</label>
              <input type="text" class="form-control" id="register__username" ng-model="vm.username" placeholder="ex. john" />
            </div>

            <div class="form-group">
              <label for="register__password">Password</label>
              <input type="password" class="form-control" id="register__password" ng-model="vm.password" placeholder="ex. thisisnotgoogleplus" />
            </div>

            <div class="form-group">
              <button type="submit" class="btn btn-primary">Submit</button>
            </div>
          </form>
        </div>
      </div>
    </div>


 Большинство классов из Bootstrap, который включен в проект. Строка:

    <form role="form" ng-submit="vm.register()">

отвечает за вызов $scope.register, который мы создали в нашем контроллере. ng-submit будет вызывать vm.register, когда форма будет отправлена. 

    <input type="email" class="form-control" id="register__email" ng-model="vm.email" placeholder="ex. john@notgoogle.com" />

в каждом input есть директива ng-model. ng-model отвечает за хранение значения входа в ViewModel. Так мы получаем имя пользователя, пароль и адрес электронной почты, когда `vm.register` вызывается.

## Управление интерфейсом с помощью RegisterController 

Для использования сервиса и интерфейса вместе, нам нужен контроллер для их подключения. 
Контроллер RegisterController позволит нам вызвать register метод службы Authentication когда пользователь отправляет форму.

static/js/authentication/controllers/register.controller.js:

    /**
    * Register controller
    * @namespace restblog.authentication.controllers
    */
    (function () {
      'use strict';

      angular
        .module('restblog.authentication.controllers')
        .controller('RegisterController', RegisterController);

      RegisterController.$inject = ['$location', '$scope', 'Authentication'];

      /**
      * @namespace RegisterController
      */
      function RegisterController($location, $scope, Authentication) {
        var vm = this;

        vm.register = register;

        /**
        * @name register
        * @desc Register a new user
        * @memberOf restblog.authentication.controllers.RegisterController
        */
        function register() {
          Authentication.register(vm.email, vm.password, vm.username);
        }
      }
    })();



Здесь мы зарегистрировали наш контроллер.

    .controller('RegisterController', RegisterController);

Vm подключает шаблон, который мы создали, чтобы получить доступ к register методу, который определим позже в контроллере.

    vm.register = register;

Здесь мы вызываем сервис. Мы передаем имя пользователя, пароль и электронную почту из `vm`.

    Authentication.register(vm.email, vm.password, vm.username);


## Регистрация маршрутов и модулей

static/js.restblog.routes.js:
-----------------------------
    (function () {
      'use strict';

      angular
        .module('restblog.routes')
        .config(config);

      config.$inject = ['$routeProvider'];

      /**
      * @name config
      * @desc Define valid application routes
      */
      function config($routeProvider) {
        $routeProvider.when('/register', {
          controller: 'RegisterController', 
          controllerAs: 'vm',
          templateUrl: '/static/templates/authentication/register.html'
        }).otherwise('/');
      }
    })();



Angular позволяет редактировать его конфигурацию. Вы делаете это с помощью .config блока.

    .config(config);

Здесь мы делаем инъекцию $routeProvider как зависимость, которая позволит нам добавить маршрутизацию к клиенту.

    function config($routeProvider) {

$routeProvider.when принимает два аргумента: путь и объект опций. Здесь мы используем путь /register, где мы хотим показать регистрационную форму.

    $routeProvider.when('/register', {

Один ключ, который вы можете включить в объект опций является controller. Он будет связывать RegisterController контроллер к этому маршруту. controllerAs - другой вариант. Это необходимо, чтобы использовать vm переменную. 

    controller: 'RegisterController',
    controllerAs: 'vm',

Другой ключ, который мы будем использовать - templateUrl. TemplateUrl принимает строку в URL, где можно найти шаблон, который мы хотим использовать для этого маршрута.

    templateUrl: '/static/templates/authentication/register.html'

Если пользователь захочет ввести URL, который мы не поддерживаем, тогда $routeProvider.otherwise будет перенаправить пользователя на путь, указанноый в этом случае, как '/'.

    }).otherwise('/');


## Настройка модулей AngularJS

В Angular необходимо определить модули до их использования. Т.е. нам нужно определить restblog.authentication.services, restblog.authentication.controllers и restblog.routes. Поскольку restblog.authentication.services и restblog.authentication.controllers подмодулями restblog.authentication, нам нужно создать также restblog.authentication модуль.

static/js/authentication/authentication.module.js:
--------------------------------------------------
    (function () {
      'use strict';

      angular
        .module('restblog.authentication', [
          'restblog.authentication.controllers',
          'restblog.authentication.services'
        ]);

      angular
        .module('restblog.authentication.controllers', []);

      angular
        .module('restblog.authentication.services', ['ngCookies']);
    })();


Now we need define to include `restblog.authentication` and `restblog.routes` as dependencies of `restblog`.

static/js/restblog.js
---------------------
определяет необходимые модули, и включает их в качестве зависимостей restblog модуля. Обратите внимание, что restblog.routes ссылается на ngRoute.

    (function () {
      'use strict';

      angular
        .module('restblog', [
          'restblog.routes',
          'restblog.authentication'
        ]);

      angular
        .module('restblog.routes', ['ngRoute']);
    })();


## Hash routing
По умолчанию, Angular использует функцию, которая называется хэш-маршрутизация. Если вы когда-либо видели URL, который выглядит как `www.google.com / # / search` то вы узнаете ее. Чтобы избавиться от хэш-маршрутизации, мы можем быть включен $locationProvider.html5Mode. В старых браузерах, которые не поддерживают маршрутизацию HTML5, Angular следут вернуться к хэш-маршрутизации.


static/js/restblog.config.js:

    (function () {
      'use strict';

      angular
        .module('restblog.config')
        .config(config);

      config.$inject = ['$locationProvider'];

      /**
      * @name config
      * @desc Enable HTML5 routing
      */
      function config($locationProvider) {
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix('!');
      }
    })();


Разрешить HTML5 routing для AngularJS
-------------------------------------
static/js/restblog.js
---------------------

    angular
      .module('restblog', [
        'restblog.config',
        // ...
      ]);

    angular
      .module('restblog.config', []);


## Подключаем файлы .js

templates/javascripts.html
--------------------------

    <script type="text/javascript" src="{% static 'js/restblog.config.js' %}"></script>
    <script type="text/javascript" src="{% static 'js/restblog.routes.js' %}"></script>
    <script type="text/javascript" src="{% static 'js/authentication/authentication.module.js' %}"></script>
    <script type="text/javascript" src="{% static 'js/authentication/services/authentication.service.js' %}"></script>
    <script type="text/javascript" src="{% static 'js/authentication/controllers/register.controller.js' %}"></script>


## CSRF защита

Поскольку мы используем аутентификацию на основе сеансов, мы должны беспокоиться о защите CSRF. 

Джанго, по умолчанию хранит маркер CSRF в куки с именем csrftoken и обслуживает заголовок с именем X-CSRFToken для любого опасного запроса HTTP (Post, PUT, PATCH, delete).

static/js/restblog.js:

    angular
      .module('restblog')
      .run(run);

    run.$inject = ['$http'];

    /**
    * @name run
    * @desc Update xsrf $http headers to align with Django's defaults
    */
    function run($http) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    }


## Checkpoint
http://localhost:8000/register

    python manage.py shell

    >>> from authentication.models import Account
    >>> Account.objects.latest('created_at')

# Logging users

## Создание login API view
authentication/views.py:
------------------------
    import json

    from django.contrib.auth import authenticate, login

    from rest_framework improt status, views
    from rest_framework.response import Response

    class LoginView(views.APIView):
        def post(self, request, format=None):
            data = json.loads(request.body)

            email = data.get('email', None)
            password = data.get('password', None)

            account = authenticate(email=email, password=password)

            if account is not None:
                if account.is_active:
                    login(request, account)

                    serialized = AccountSerializer(account)

                    return Response(serialized.data)
                else:
                    return Response({
                        'status': 'Unauthorized',
                        'message': 'This account has been disabled.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'Username/password combination invalid.'
                }, status=status.HTTP_401_UNAUTHORIZED)


views.APIView сделаны специально для обработки AJAX-запросов.

     class LoginView(views.APIView):

В отличие от generic views, мы должны обрабатывать каждый HTTP. Вход в систему, как правило, должен быть запрос Post, поэтому переопределим self.post()) метод.

    def post(self, request, format=None):

Django обеспечивает хороший набор утилит для аутентификации пользователей. Authenticate() метод  принимает адрес электронной почты и пароль. Джанго затем проверяет базу данных для Account с электронной почтой email. Если он найден, Django попытается проверить данный пароль. Если имя пользователя и пароль правильны, Authenticate() возвращает - Account найден. Если какй-либо из этих шагов не проходит, Authenticate() вернет None.

    account = authenticate(email=email, password=password)

В случае, если Authenticate() возвращает None, мы отвечаем 401 кодом состояния и сообщаем пользователю, что сочетание электронной почты/пароль недействительно.

    if account is not None:
        # ...
    else:
        return Response({
            'status': 'Unauthorized',
            'message': 'Username/password combination invalid.'
        }, status=status.HTTP_401_UNAUTHORIZED)

Если учетная запись пользователя по какой-то причине отключена, мы отвечаем 401 кодом состояния. Здесь мы просто говорим, что учетная запись была отключена.

    if account.is_active:
        # ...
    else:
        return Response({
            'status': 'Unauthorized',
            'message': 'This account has been disabled.'
        }, status=status.HTTP_401_UNAUTHORIZED)

Если Authenticate() вернул успех и пользователь активен, то мы используем login() утилиту Джанго, чтобы создать новую сессию для этого пользователя.

    login(request, account)

Мы хотим сохранить некоторую информацию о пользователе в браузере, если запрос login прошел успешно, мы выполняем сериализацию объекта Account и возвращаем полученный JSON в качестве ответа.

    serialized = AccountSerializer(account)

    return Response(serialized.data)


## Добавляем login API маршрут

urls.py:
--------
    from authentication.views import LoginView

    urlpatterns = patterns(
        # ...
        url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
        # ...
    )


## Authentication Service

static/js/authentication/services/authentication.service.js:
-------------------------------------------------------------
    /**
     * @name login
     * @desc Try to log in with email `email` and password `password`
     * @param {string} email The email entered by the user
     * @param {string} password The password entered by the user
     * @returns {Promise}
     * @memberOf restblog.authentication.services.Authentication
     */
    function login(email, password) {
      return $http.post('/api/v1/auth/login/', {
        email: email, password: password
      });
    }

выставим его как часть службы:

    var Authentication = {
      login: login,
      register: register
    };


Мы хотим отобразить информацию о текущем пользователе в навигационной панели в верхней части страницы. Это означает, что нам нужен способ, чтобы сохранить ответ, возвращаемый login(). Нам также потребуется способ извлечения с проверкой подлинности пользователя. Нам нужен способ, чтобы идентифицировать пользователя в браузере. И хотелось бы иметь простой способ проверить, если текущий пользователь проходит проверку подлинности.


Добавим каэдую из функций в Authentication service:
---------------------------------------------------
    /**
     * @name getAuthenticatedAccount
     * @desc Return the currently authenticated account
     * @returns {object|undefined} Account if authenticated, else `undefined`
     * @memberOf restblog.authentication.services.Authentication
     */
    function getAuthenticatedAccount() {
      if (!$cookies.authenticatedAccount) {
        return;
      }

      return JSON.parse($cookies.authenticatedAccount);
    }

Есди нет authenticatedAccount cookie (установлено в setAuthenticatedAccount()), тогда return; иначе return обработаный user object из cookie.

    /**
     * @name isAuthenticated
     * @desc Check if the current user is authenticated
     * @returns {boolean} True is user is authenticated, else false.
     * @memberOf restblog.authentication.services.Authentication
     */
    function isAuthenticated() {
      return !!$cookies.authenticatedAccount;
    }

Возврат boolean значения из authenticatedAccount cookie. 

    /**
     * @name setAuthenticatedAccount
     * @desc Stringify the account object and store it in a cookie
     * @param {Object} user The account object to be stored
     * @returns {undefined}
     * @memberOf restblog.authentication.services.Authentication
     */
    function setAuthenticatedAccount(account) {
      $cookies.authenticatedAccount = JSON.stringify(account);
    }

Установка authenticatedAccount cookie в stringified версии account объекта.

    /**
     * @name unauthenticate
     * @desc Delete the cookie where the user object is stored
     * @returns {undefined}
     * @memberOf restblog.authentication.services.Authentication
     */
    function unauthenticate() {
      delete $cookies.authenticatedAccount;
    }

Удалить authenticatedAccount cookie.

Зарегистрировать service:

    var Authentication = {
      getAuthenticatedAccount: getAuthenticatedAccount,
      isAuthenticated: isAuthenticated,
      login: login,
      register: register,
      setAuthenticatedAccount: setAuthenticatedAccount,
      unauthenticate: unauthenticate
    };

обновить метод login службы Authentication
-------------------------------------------
Заменить Authentication.login следующим текстом:


    /**
     * @name login
     * @desc Try to log in with email `email` and password `password`
     * @param {string} email The email entered by the user
     * @param {string} password The password entered by the user
     * @returns {Promise}
     * @memberOf restblog.authentication.services.Authentication
     */
    function login(email, password) {
      return $http.post('/api/v1/auth/login/', {
        email: email, password: password
      }).then(loginSuccessFn, loginErrorFn);

      /**
       * @name loginSuccessFn
       * @desc Set the authenticated account and redirect to index
       */
      function loginSuccessFn(data, status, headers, config) {
        Authentication.setAuthenticatedAccount(data.data);

        window.location = '/';
      }

      /**
       * @name loginErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function loginErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }


## Создание login interface

static/templates/authentication/login.html:
-------------------------------------------

    <div class="row">
      <div class="col-md-4 col-md-offset-4">
        <h1>Login</h1>

        <div class="well">
          <form role="form" ng-submit="vm.login()">
            <div class="alert alert-danger" ng-show="error" ng-bind="error"></div>

            <div class="form-group">
              <label for="login__email">Email</label>
              <input type="text" class="form-control" id="login__email" ng-model="vm.email" placeholder="ex. john@example.com" />
            </div>

            <div class="form-group">
              <label for="login__password">Password</label>
              <input type="password" class="form-control" id="login__password" ng-model="vm.password" placeholder="ex. thisisnotgoogleplus" />
            </div>

            <div class="form-group">
              <button type="submit" class="btn btn-primary">Submit</button>
            </div>
          </form>
        </div>
      </div>
    </div>


## Обработка login interface с помощью LoginController

static/js/authentication/controllers/login.controller.js:
---------------------------------------------------------
    /**
    * LoginController
    * @namespace restblog.authentication.controllers
    */
    (function () {
      'use strict';

      angular
        .module('restblog.authentication.controllers')
        .controller('LoginController', LoginController);

      LoginController.$inject = ['$location', '$scope', 'Authentication'];

      /**
      * @namespace LoginController
      */
      function LoginController($location, $scope, Authentication) {
        var vm = this;

        vm.login = login;

        activate();

        /**
        * @name activate
        * @desc Actions to be performed when this controller is instantiated
        * @memberOf restblog.authentication.controllers.LoginController
        */
        function activate() {
          // If the user is authenticated, they should not be here.
          if (Authentication.isAuthenticated()) {
            $location.url('/');
          }
        }

        /**
        * @name login
        * @desc Log the user in
        * @memberOf restblog.authentication.controllers.LoginController
        */
        function login() {
          Authentication.login(vm.email, vm.password);
        }
      }
    })();


если пользователь уже идентифицирован, ему нечего делать на странице входа - перенаправим пользователя на страницу индекса.

Мы должны сделать это на странице регистрации тоже. 

    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }


## RegisterController

static/js/authentication/controllers/register.controller.js:
------------------------------------------------------------
    activate();
    
    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     * @memberOf restblog.authentication.controllers.RegisterController
     */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }



Заменим Authentication.register на:

    /**
    * @name register
    * @desc Try to register a new user
    * @param {string} email The email entered by the user
    * @param {string} password The password entered by the user
    * @param {string} username The username entered by the user
    * @returns {Promise}
    * @memberOf restblog.authentication.services.Authentication
    */
    function register(email, password, username) {
      return $http.post('/api/v1/accounts/', {
        username: username,
        password: password,
        email: email
      }).then(registerSuccessFn, registerErrorFn);

      /**
      * @name registerSuccessFn
      * @desc Log the new user in
      */
      function registerSuccessFn(data, status, headers, config) {
        Authentication.login(email, password);
      }

      /**
      * @name registerErrorFn
      * @desc Log "Epic failure!" to the console
      */
      function registerErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }


## Маршрут для login interface

static/js/restblog.routes.js:

    $routeProvider.when('/register', {
      controller: 'RegisterController', 
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/register.html'
    }).when('/login', {
      controller: 'LoginController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/authentication/login.html'
    }).otherwise('/');



## javascripts.html:

    <script type="text/javascript" src="{% static 'js/authentication/controllers/login.controller.js' %}"></script>


## Checkpoint

    http://localhost:8000/login



# Logout


## Создание logout API view

authentication/views.py:
------------------------
    from django.contrib.auth import logout

    from rest_framework import permissions

    class LogoutView(views.APIView):
        permission_classes = (permissions.IsAuthenticated,)

        def post(self, request, format=None):
            logout(request)

            return Response({}, status=status.HTTP_204_NO_CONTENT)


Только прошедшие проверку пользователи вызывать этот метод. Django REST Framework в permissions.IsAuthenticated обрабатывает это за нас. Если пользователь не прошел проверку подлинности, он получат 403 ошибку.

    permission_classes = (permissions.IsAuthenticated,)

Если пользователь прошел проверку подлинности, все, что нам нужно сделать, это вызвать logout метод Джанго.

    logout(request)

вернуться при выходе из системы - мы просто возвращаем пустой ответ с `200` кодом состояния.

    return Response({}, status=status.HTTP_204_NO_CONTENT)


URLs.
-----
urls.py:

    from authentication.views import LogoutView

    urlpatterns = patterns(
        # ...
        url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
        #...
    )


## Logout: AngularJS Service

Добавим Authentication service в authentication.service.js:

    /**
     * @name logout
     * @desc Try to log the user out
     * @returns {Promise}
     * @memberOf restblog.authentication.services.Authentication
     */
    function logout() {
      return $http.post('/api/v1/auth/logout/')
        .then(logoutSuccessFn, logoutErrorFn);

      /**
       * @name logoutSuccessFn
       * @desc Unauthenticate and redirect to index with page reload
       */
      function logoutSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();

        window.location = '/';
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function logoutErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }

Зарегистрируем Authentication service:

    var Authentication = {
      getAuthenticatedUser: getAuthenticatedUser,
      isAuthenticated: isAuthenticated,
      login: login,
      logout: logout,
      register: register,
      setAuthenticatedUser: setAuthenticatedUser,
      unauthenticate: unauthenticate
    };


## Навигация NavbarController

static/js/layout/controllers/navbar.controller.js:
--------------------------------------------------

    /**
    * NavbarController
    * @namespace restblog.layout.controllers
    */
    (function () {
      'use strict';

      angular
        .module('restblog.layout.controllers')
        .controller('NavbarController', NavbarController);

      NavbarController.$inject = ['$scope', 'Authentication'];

      /**
      * @namespace NavbarController
      */
      function NavbarController($scope, Authentication) {
        var vm = this;

        vm.logout = logout;

        /**
        * @name logout
        * @desc Log the user out
        * @memberOf restblog.layout.controllers.NavbarController
        */
        function logout() {
          Authentication.logout();
        }
      }
    })();


templates/navbar.html
----------------------
Добавляем `ng-controller` directive со значением `NavbarController as vm` в nav tag:

    <nav class="navbar navbar-default" role="navigation" ng-controller="NavbarController as vm">

templates/navbar.html:

    <li><a href="javascript:void(0)" ng-click="vm.logout()">Logout</a></li>


## Layout modules

static/js/layout/layout.module.js:

    (function () {
      'use strict';

      angular
        .module('restblog.layout', [
          'restblog.layout.controllers'
        ]);

      angular
        .module('restblog.layout.controllers', []);
    })();


Обновить static/javascripts/restblog.js:

    angular
      .module('restblog', [
        'restblog.config',
        'restblog.routes',
        'restblog.authentication',
        'restblog.layout'
      ]);


## javascripts.html

    <script type="text/javascript" src="{% static 'javascripts/layout/layout.module.js' %}"></script>
    <script type="text/javascript" src="{% static 'javascripts/layout/controllers/navbar.controller.js' %}"></script>


# Создаем Post model

## Создаем posts app

    $ python manage.py startapp posts


settings.py:

    INSTALLED_APPS = (
        # ...
        'posts',
    )

## Редактируем Post model

from django.db import models

from authentication.models import Account


    class Post(models.Model):
        author = models.ForeignKey(Account)
        content = models.TextField()

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __unicode__(self):
            return '{0}'.format(self.content)


migrate

    $ python manage.py makemigrations
    $ python manage.py migrate


## Сериализация Post model
posts/serializers.py:
---------------------
    from rest_framework import serializers

    from authentication.serializers import Account
    from posts.models import Post


    class PostSerializer(serializers.ModelSerializer):
        author = AccountSerializer(read_only=True, required=False)

        class Meta:
            model = Post

            fields = ('id', 'author', 'content', 'created_at', 'updated_at')
            read_only_fields = ('id', 'created_at', 'updated_at')

        def get_validation_exclusions(self, *args, **kwargs):
            exclusions = super(PostSerializer, self).get_validation_exclusions()

            return exclusions + ['author']


При сериализации объекта Post, мы хотим включить всю информацию об авторе. В Django REST Framework, это называется вложенные отношения. Сериализуем Account, связанный с этим Post и включаем его в наш JSON.

Мы передаем read_only = true, потому что мы не должны обновлять объект Account вместе с PostSerializer. Мы также устанавливаем required = false, потому что мы будем автоматически установливать автора этого поста.

    author = AccountSerializer(read_only=True, required=False)

По той же причине мы используем required=False

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(PostSerializer, self).get_validation_exclusions()

        return exclusions + ['author']

## Создаем API views для Post


Заменим posts/views.py:

    from rest_framework import permissions, viewsets
    from rest_framework.response import Response

    from posts.models import Post
    from posts.permissions import IsAuthorOfPost
    from posts.serializers import PostSerializer


    class PostViewSet(viewsets.ModelViewSet):
        queryset = Post.objects.order_by('-created_at')
        serializer_class = PostSerializer

        def get_permissions(self):
            if self.request.method in permissions.SAFE_METHODS:
                return (permissions.AllowAny(),)
            return (permissions.IsAuthenticated(), IsAuthorOfPost(),)

    def perform_create(self, serializer):
      instance = serializer.save(author=self.request.user)

      return super(PostViewSet, self).perform_create(serializer)



    class AccountPostsViewSet(viewsets.ViewSet):
        queryset = Post.objects.select_related('author').all()
        serializer_class = PostSerializer

        def list(self, request, account_username=None):
            queryset = self.queryset.filter(author__username=account_username)
            serializer = self.serializer_class(queryset, many=True)

            return Response(serializer.data)



perform_create вызывается перед как модель сохраняется.

Когда создается объект Post он должен быть связан с автором. Перехватим пользователя, связанного с этим запросом и сделаем его автором этого Post.

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)

        return super(PostViewSet, self).perform_create(serializer)


Если метод HTTP является безопасным, мы позволяем анонимный доступ к этому посту.


    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(), IsAuthorOfPost(),)


Этот Viewset будет использоваться для получения списка сообщений, связанных с конкретным Account.

    class AccountPostsViewSet(viewsets.ViewSet):

Здесь мы фильтруем наш QuerySet, основанный на имени автора. Account_username аргумент будет поставляться маршрутизатором.

    queryset = self.queryset.filter(author__username=account_username)


## Создание IsAuthorOfPost permission
posts/permissions.py
----------------------

    from rest_framework import permissions


    class IsAuthorOfPost(permissions.BasePermission):
        def has_object_permission(self, request, view, post):
            if request.user:
                return post.author == request.user
            return False

## urls.py

urls.py:

    from posts.views import AccountPostsViewSet, PostViewSet

    urlpatterns = [

    router.register(r'posts', PostViewSet)

    accounts_router = routers.NestedSimpleRouter(
        router, r'accounts', lookup='account'
    )
    accounts_router.register(r'posts', AccountPostsViewSet)

    urlpatterns = [
      # ...
      
      url(r'^api/v1/', include(router.urls)),
      url(r'^api/v1/', include(accounts_router.urls)),

      # ...
    ]

## Checkpoint

    >>> from authentication.models import Account
    >>> from posts.models import Post
    >>> from posts.serializers import PostSerializer
    >>> account = Account.objects.latest('created_at')
    >>> post = Post.objects.create(author=account, content='I promise this is not Google Plus!')
    >>> serialized_post = PostSerializer(post)
    >>> serialized_post.data


# Rendering Post objects

## Модуль для posts

static/js/postsposts.module.js:

    (function () {
      'use strict';

      angular
        .module('restblog.posts', [
          'restblog.posts.controllers',
          'restblog.posts.directives',
          'restblog.posts.services'
        ]);

      angular
        .module('restblog.posts.controllers', []);

      angular
        .module('restblog.posts.directives', ['ngDialog']);

      angular
        .module('restblog.posts.services', []);
    })();


Добавим restblog.posts в restblog.js:

    angular
      .module('restblog', [
        'restblog.config',
        'restblog.routes',
        'restblog.authentication',
        'restblog.layout',
        'restblog.posts'
      ]);


javascripts.html:
------------------

    <script type="text/javascript" src="{% static 'js/posts/posts.module.js' %}"></script>


## Создаем Posts service

static/js/posts/services/posts.service.js:

    /**
    * Posts
    * @namespace restblog.posts.services
    */
    (function () {
      'use strict';

      angular
        .module('restblog.posts.services')
        .factory('Posts', Posts);

      Posts.$inject = ['$http'];

      /**
      * @namespace Posts
      * @returns {Factory}
      */
      function Posts($http) {
        var Posts = {
          all: all,
          create: create,
          get: get
        };

        return Posts;

        ////////////////////
        
        /**
        * @name all
        * @desc Get all Posts
        * @returns {Promise}
        * @memberOf restblog.posts.services.Posts
        */
        function all() {
          return $http.get('/api/v1/posts/');
        }


        /**
        * @name create
        * @desc Create a new Post
        * @param {string} content The content of the new Post
        * @returns {Promise}
        * @memberOf restblog.posts.services.Posts
        */
        function create(content) {
          return $http.post('/api/v1/posts/', {
            content: content
          });
        }

        /**
         * @name get
         * @desc Get the Posts of a given user
         * @param {string} username The username to get Posts for
         * @returns {Promise}
         * @memberOf restblog.posts.services.Posts
         */
        function get(username) {
          return $http.get('/api/v1/accounts/' + username + '/posts/');
        }
      }
    })();


javascripts.html:
------------------

    <script type="text/javascript" src="{% static 'js/posts/services/posts.service.js' %}"></script>


## Создание интерфейса для index page

static/templates/layout/index.html:
-----------------------------------

    <posts posts="vm.posts" ng-show="vm.posts && vm.posts.length"></posts>


## Snackbar service

static/js/utils/services/snackbar.service.js:

    /**
    * Snackbar
    * @namespace restblog.utils.services
    */
    (function ($, _) {
      'use strict';

      angular
        .module('restblog.utils.services')
        .factory('Snackbar', Snackbar);

      /**
      * @namespace Snackbar
      */
      function Snackbar() {
        /**
        * @name Snackbar
        * @desc The factory to be returned
        */
        var Snackbar = {
          error: error,
          show: show
        };

        return Snackbar;

        ////////////////////
        
        /**
        * @name _snackbar
        * @desc Display a snackbar
        * @param {string} content The content of the snackbar
        * @param {Object} options Options for displaying the snackbar
        */
        function _snackbar(content, options) {
          options = _.extend({ timeout: 3000 }, options);
          options.content = content;

          $.snackbar(options);
        }


        /**
        * @name error
        * @desc Display an error snackbar
        * @param {string} content The content of the snackbar
        * @param {Object} options Options for displaying the snackbar
        * @memberOf restblog.utils.services.Snackbar
        */
        function error(content, options) {
          _snackbar('Error: ' + content, options);
        }


        /**
        * @name show
        * @desc Display a standard snackbar
        * @param {string} content The content of the snackbar
        * @param {Object} options Options for displaying the snackbar
        * @memberOf restblog.utils.services.Snackbar
        */
        function show(content, options) {
          _snackbar(content, options);
        }
      }
    })($, _);


static/js/utils/utils.module.js:
--------------------------------
    (function () {
      'use strict';

      angular
        .module('restblog.utils', [
          'restblog.utils.services'
        ]);

      angular
        .module('restblog.utils.services', []);
    })();

static/js/restblog.js:
----------------------
    angular
      .module('restblog', [
        // ...
        'restblog.utils',
        // ...
      ]);


javascripts.html:
------------------
    <script type="text/javascript" src="{% static 'js/utils/utils.module.js' %}"></script>
    <script type="text/javascript" src="{% static 'js/utils/services/snackbar.service.js' %}"></script>

## IndexController
static/js/layout/controllers/index.controller.js:
-------------------------------------------------
    /**
    * IndexController
    * @namespace restblog.layout.controllers
    */
    (function () {
      'use strict';

      angular
        .module('restblog.layout.controllers')
        .controller('IndexController', IndexController);

      IndexController.$inject = ['$scope', 'Authentication', 'Posts', 'Snackbar'];

      /**
      * @namespace IndexController
      */
      function IndexController($scope, Authentication, Posts, Snackbar) {
        var vm = this;

        vm.isAuthenticated = Authentication.isAuthenticated();
        vm.posts = [];

        activate();

        /**
        * @name activate
        * @desc Actions to be performed when this controller is instantiated
        * @memberOf restblog.layout.controllers.IndexController
        */
        function activate() {
          Posts.all().then(postsSuccessFn, postsErrorFn);

          $scope.$on('post.created', function (event, post) {
            vm.posts.unshift(post);
          });

          $scope.$on('post.created.error', function () {
            vm.posts.shift();
          });


          /**
          * @name postsSuccessFn
          * @desc Update posts array on view
          */
          function postsSuccessFn(data, status, headers, config) {
            vm.posts = data.data;
          }


          /**
          * @name postsErrorFn
          * @desc Show snackbar with error
          */
          function postsErrorFn(data, status, headers, config) {
            Snackbar.error(data.error);
          }
        }
      }
    })();


javascripts.html:
------------------

    <script type="text/javascript" src="{% static 'js/layout/controllers/index.controller.js' %}"></script>


## route для index page

static/js/restblog.routes.js:
-----------------------------
    .when('/', {
      controller: 'IndexController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/layout/index.html'
    })


## directive просмотра Posts
static/js/posts/directives/posts.directive.js:
-----------------------------------------------
    /**
    * Posts
    * @namespace restblog.posts.directives
    */
    (function () {
      'use strict';

      angular
        .module('restblog.posts.directives')
        .directive('posts', posts);

      /**
      * @namespace Posts
      */
      function posts() {
        /**
        * @name directive
        * @desc The directive to be returned
        * @memberOf restblog.posts.directives.Posts
        */
        var directive = {
          controller: 'PostsController',
          controllerAs: 'vm',
          restrict: 'E',
          scope: {
            posts: '='
          },
          templateUrl: '/static/templates/posts/posts.html'
        };

        return directive;
      }
    })();

javascripts.html:
-----------------
    <script type="text/javascript" src="{% static 'js/posts/directives/posts.directive.js' %}"></script>


## PostsController

static/js/posts/controllers/posts.controller.js:

    /**
    * PostsController
    * @namespace restblog.posts.controllers
    */
    (function () {
      'use strict';

      angular
        .module('restblog.posts.controllers')
        .controller('PostsController', PostsController);

      PostsController.$inject = ['$scope'];

      /**
      * @namespace PostsController
      */
      function PostsController($scope) {
        var vm = this;

        vm.columns = [];

        activate();


        /**
        * @name activate
        * @desc Actions to be performed when this controller is instantiated
        * @memberOf restblog.posts.controllers.PostsController
        */
        function activate() {
          $scope.$watchCollection(function () { return $scope.posts; }, render);
          $scope.$watch(function () { return $(window).width(); }, render);
        }
        

        /**
        * @name calculateNumberOfColumns
        * @desc Calculate number of columns based on screen width
        * @returns {Number} The number of columns containing Posts
        * @memberOf restblog.posts.controllers.PostsControllers
        */
        function calculateNumberOfColumns() {
          var width = $(window).width();

          if (width >= 1200) {
            return 4;
          } else if (width >= 992) {
            return 3;
          } else if (width >= 768) {
            return 2;
          } else {
            return 1;
          }
        }


        /**
        * @name approximateShortestColumn
        * @desc An algorithm for approximating which column is shortest
        * @returns The index of the shortest column
        * @memberOf restblog.posts.controllers.PostsController
        */
        function approximateShortestColumn() {
          var scores = vm.columns.map(columnMapFn);

          return scores.indexOf(Math.min.apply(this, scores));

          
          /**
          * @name columnMapFn
          * @desc A map function for scoring column heights
          * @returns The approximately normalized height of a given column
          */
          function columnMapFn(column) {
            var lengths = column.map(function (element) {
              return element.content.length;
            });

            return lengths.reduce(sum, 0) * column.length;
          }


          /**
          * @name sum
          * @desc Sums two numbers
          * @params {Number} m The first number to be summed
          * @params {Number} n The second number to be summed
          * @returns The sum of two numbers
          */
          function sum(m, n) {
            return m + n;
          }
        }


        /**
        * @name render
        * @desc Renders Posts into columns of approximately equal height
        * @param {Array} current The current value of `vm.posts`
        * @param {Array} original The value of `vm.posts` before it was updated
        * @memberOf restblog.posts.controllers.PostsController
        */
        function render(current, original) {
          if (current !== original) {
            vm.columns = [];

            for (var i = 0; i < calculateNumberOfColumns(); ++i) {
              vm.columns.push([]);
            }

            for (var i = 0; i < current.length; ++i) {
              var column = approximateShortestColumn();

              vm.columns[column].push(current[i]);
            }
          }
        }
      }
    })();


javascripts.html:
------------------
    <script type="text/javascript" src="{% static 'js/posts/controllers/posts.controller.js' %}"></script>


## template

static/templates/posts/posts.html
---------------------------------
    <div class="row" ng-cloak>
      <div ng-repeat="column in vm.columns">
        <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
          <div ng-repeat="post in column">
            <post post="post"></post>
          </div>
        </div>
      </div>

      <div ng-hide="vm.columns && vm.columns.length">
        <div class="col-sm-12 no-posts-here">
          <em>The are no posts here.</em>
        </div>
      </div>
    </div>


## directive для одного Post

static/js/posts/directives/post.directive.js:
---------------------------------------------
    /**
    * Post
    * @namespace restblog.posts.directives
    */
    (function () {
      'use strict';

      angular
        .module('restblog.posts.directives')
        .directive('post', post);

      /**
      * @namespace Post
      */
      function post() {
        /**
        * @name directive
        * @desc The directive to be returned
        * @memberOf restblog.posts.directives.Post
        */
        var directive = {
          restrict: 'E',
          scope: {
            post: '='
          },
          templateUrl: '/static/templates/posts/post.html'
        };

        return directive;
      }
    })();


javascripts.html:
-----------------

    <script type="text/javascript" src="{% static 'js/posts/directives/post.directive.js' %}"></script>

## template

static/templates/posts/post.html:
-----------------------------------

    <div class="row">
      <div class="col-sm-12">
        <div class="well">
          <div class="post">
            <div class="post__meta">
              <a href="/+{{ post.author.username }}">
                +{{ post.author.username }}
              </a>
            </div>

            <div class="post__content">
              {{ post.content }}
            </div>
          </div>
        </div>
      </div>
    </div>


## CSS
static/сыы/styles.css:
----------------------

    .no-posts-here {
      text-align: center;
    }

    .post {}

    .post .post__meta {
      font-weight: bold;
      text-align: right;
      padding-bottom: 19px;
    }

    .post .post__meta a:hover {
      text-decoration: none;
    }


# Создание новых posts

static/templates/layout/index.html:
-----------------------------------

    <a class="btn btn-primary btn-fab btn-raised mdi-content-add btn-add-new-post"
      href="javascript:void(0)"
      ng-show="vm.isAuthenticated"
      ng-dialog="/static/templates/posts/new-post.html"
      ng-dialog-controller="NewPostController as vm"></a>


static/css/styles.css:

    .btn-add-new-post {
      position: fixed;
      bottom: 20px;
      right: 20px;
    }


## Интерфейс
static/templates/posts/new-post.html:
--------------------------------------

    <form role="form" ng-submit="vm.submit()">
      <div class="form-group">
        <label for="post__content">New Post</label>
        <textarea class="form-control" 
                  id="post__content" 
                  rows="3" 
                  placeholder="ex. This is my first time posting on Not Google Plus!" 
                  ng-model="vm.content">
        </textarea>
      </div>

      <div class="form-group">
        <button type="submit" class="btn btn-primary">
          Submit
        </button>
      </div>
    </form>


## NewPostController
static/js/posts/controller/new-post.controller.js:
---------------------------------------------------

    /**
    * NewPostController
    * @namespace restblog.posts.controllers
    */
    (function () {
      'use strict';

      angular
        .module('restblog.posts.controllers')
        .controller('NewPostController', NewPostController);

      NewPostController.$inject = ['$rootScope', '$scope', 'Authentication', 'Snackbar', 'Posts'];

      /**
      * @namespace NewPostController
      */
      function NewPostController($rootScope, $scope, Authentication, Snackbar, Posts) {
        var vm = this;

        vm.submit = submit;

        /**
        * @name submit
        * @desc Create a new Post
        * @memberOf restblog.posts.controllers.NewPostController
        */
        function submit() {
          $rootScope.$broadcast('post.created', {
            content: vm.content,
            author: {
              username: Authentication.getAuthenticatedAccount().username
            }
          });

          $scope.closeThisDialog();

          Posts.create(vm.content).then(createPostSuccessFn, createPostErrorFn);


          /**
          * @name createPostSuccessFn
          * @desc Show snackbar with success message
          */
          function createPostSuccessFn(data, status, headers, config) {
            Snackbar.show('Success! Post created.');
          }

          
          /**
          * @name createPostErrorFn
          * @desc Propogate error event and show snackbar with error message
          */
          function createPostErrorFn(data, status, headers, config) {
            $rootScope.$broadcast('post.created.error');
            Snackbar.error(data.error);
          }
        }
      }
    })();




javascripts.html:
-----------------
    <script type="text/javascript" src="{% static 'js/posts/controllers/new-post.controller.js' %}"></script>

# user profiles

## Создание profile modules

static/js/profiles/profiles.module.js:
--------------------------------------
    (function () {
      'use strict';

      angular
        .module('restblog.profiles', [
          'restblog.profiles.controllers',
          'restblog.profiles.services'
        ]);

      angular
        .module('restblog.profiles.controllers', []);

      angular
        .module('restblog.profiles.services', []);
    })();


restblog.js:
--------------
    angular
      .module('restblog', [
        'restblog.config',
        'restblog.routes',
        'restblog.authentication',
        'restblog.layout',
        'restblog.posts',
        'restblog.profiles'
      ]);


javascripts.html:
------------------
    <script type="text/javascript" src="{% static 'js/profiles/profiles.module.js' %}"></script>

## Создание Profile factory

static/js/profiles/services/profile.service.js:
------------------------------------------------
    /**
    * Profile
    * @namespace restblog.profiles.services
    */
    (function () {
      'use strict';

      angular
        .module('restblog.profiles.services')
        .factory('Profile', Profile);

      Profile.$inject = ['$http'];

      /**
      * @namespace Profile
      */
      function Profile($http) {
        /**
        * @name Profile
        * @desc The factory to be returned
        * @memberOf restblog.profiles.services.Profile
        */
        var Profile = {
          destroy: destroy,
          get: get,
          update: update
        };

        return Profile;

        /////////////////////

        /**
        * @name destroy
        * @desc Destroys the given profile
        * @param {Object} profile The profile to be destroyed
        * @returns {Promise}
        * @memberOf restblog.profiles.services.Profile
        */
        function destroy(profile) {
          return $http.delete('/api/v1/accounts/' + profile.id + '/');
        }


        /**
        * @name get
        * @desc Gets the profile for user with username `username`
        * @param {string} username The username of the user to fetch
        * @returns {Promise}
        * @memberOf restblog.profiles.services.Profile
        */
        function get(username) {
          return $http.get('/api/v1/accounts/' + username + '/');
        }


        /**
        * @name update
        * @desc Update the given profile
        * @param {Object} profile The profile to be updated
        * @returns {Promise}
        * @memberOf restblog.profiles.services.Profile
        */
        function update(profile) {
          return $http.put('/api/v1/accounts/' + profile.username + '/', profile);
        }
      }
    })();


javascripts.html:
-------------------
    <script type="text/javascript" src="{% static 'js/profiles/services/profile.service.js' %}"></script>


## Интерфейс для user profiles
static/templates/profiles/profile.html:
---------------------------------------

    <div class="profile" ng-show="vm.profile">
      <div class="jumbotron profile__header">
        <h1 class="profile__username">+{{ vm.profile.username }}</h1>
        <p class="profile__tagline">{{ vm.profile.tagline }}</p>
      </div>

      <posts posts="vm.posts"></posts>
    </div>

## ProfileController

static/js/profiles/controllers/profile.controller.js:
-----------------------------------------------------
    /**
    * ProfileController
    * @namespace restblog.profiles.controllers
    */
    (function () {
      'use strict';

      angular
        .module('restblog.profiles.controllers')
        .controller('ProfileController', ProfileController);

      ProfileController.$inject = ['$location', '$routeParams', 'Posts', 'Profile', 'Snackbar'];

      /**
      * @namespace ProfileController
      */
      function ProfileController($location, $routeParams, Posts, Profile, Snackbar) {
        var vm = this;

        vm.profile = undefined;
        vm.posts = [];

        activate();

        /**
        * @name activate
        * @desc Actions to be performed when this controller is instantiated
        * @memberOf restblog.profiles.controllers.ProfileController
        */
        function activate() {
          var username = $routeParams.username.substr(1);

          Profile.get(username).then(profileSuccessFn, profileErrorFn);
          Posts.get(username).then(postsSuccessFn, postsErrorFn);

          /**
          * @name profileSuccessProfile
          * @desc Update `profile` on viewmodel
          */
          function profileSuccessFn(data, status, headers, config) {
            vm.profile = data.data;
          }


          /**
          * @name profileErrorFn
          * @desc Redirect to index and show error Snackbar
          */
          function profileErrorFn(data, status, headers, config) {
            $location.url('/');
            Snackbar.error('That user does not exist.');
          }


          /**
            * @name postsSucessFn
            * @desc Update `posts` on viewmodel
            */
          function postsSuccessFn(data, status, headers, config) {
            vm.posts = data.data;
          }


          /**
            * @name postsErrorFn
            * @desc Show error snackbar
            */
          function postsErrorFn(data, status, headers, config) {
            Snackbar.error(data.data.error);
          }
        }
      }
    })();


javascripts.html:
------------------
    <script type="text/javascript" src="{% static 'js/profiles/controllers/profile.controller.js' %}"></script>


## route
static/js/restblog.routes.js:
-----------------------------
    .when('/+:username', {
      controller: 'ProfileController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/profiles/profile.html'
    })


# Updating user profiles

## ProfileSettingsController
static/js/profiles/controllers/profile-settings.controller.js:
--------------------------------------------------------------
    /**
    * ProfileSettingsController
    * @namespace restblog.profiles.controllers
    */
    (function () {
      'use strict';

      angular
        .module('restblog.profiles.controllers')
        .controller('ProfileSettingsController', ProfileSettingsController);

      ProfileSettingsController.$inject = [
        '$location', '$routeParams', 'Authentication', 'Profile', 'Snackbar'
      ];

      /**
      * @namespace ProfileSettingsController
      */
      function ProfileSettingsController($location, $routeParams, Authentication, Profile, Snackbar) {
        var vm = this;

        vm.destroy = destroy;
        vm.update = update;

        activate();


        /**
        * @name activate
        * @desc Actions to be performed when this controller is instantiated.
        * @memberOf restblog.profiles.controllers.ProfileSettingsController
        */
        function activate() {
          var authenticatedAccount = Authentication.getAuthenticatedAccount();
          var username = $routeParams.username.substr(1);

          // Redirect if not logged in
          if (!authenticatedAccount) {
            $location.url('/');
            Snackbar.error('You are not authorized to view this page.');
          } else {
            // Redirect if logged in, but not the owner of this profile.
            if (authenticatedAccount.username !== username) {
              $location.url('/');
              Snackbar.error('You are not authorized to view this page.');
            }
          }

          Profile.get(username).then(profileSuccessFn, profileErrorFn);

          /**
          * @name profileSuccessFn
          * @desc Update `profile` for view
          */
          function profileSuccessFn(data, status, headers, config) {
            vm.profile = data.data;
          }

          /**
          * @name profileErrorFn
          * @desc Redirect to index
          */
          function profileErrorFn(data, status, headers, config) {
            $location.url('/');
            Snackbar.error('That user does not exist.');
          }
        }


        /**
        * @name destroy
        * @desc Destroy this user's profile
        * @memberOf restblog.profiles.controllers.ProfileSettingsController
        */
        function destroy() {
          Profile.destroy(vm.profile.username).then(profileSuccessFn, profileErrorFn);

          /**
          * @name profileSuccessFn
          * @desc Redirect to index and display success snackbar
          */
          function profileSuccessFn(data, status, headers, config) {
            Authentication.unauthenticate();
            window.location = '/';

            Snackbar.show('Your account has been deleted.');
          }


          /**
          * @name profileErrorFn
          * @desc Display error snackbar
          */
          function profileErrorFn(data, status, headers, config) {
            Snackbar.error(data.error);
          }
        }


        /**
        * @name update
        * @desc Update this user's profile
        * @memberOf restblog.profiles.controllers.ProfileSettingsController
        */
        function update() {
          Profile.update(vm.profile).then(profileSuccessFn, profileErrorFn);

          /**
          * @name profileSuccessFn
          * @desc Show success snackbar
          */
          function profileSuccessFn(data, status, headers, config) {
            Snackbar.show('Your profile has been updated.');
          }


          /**
          * @name profileErrorFn
          * @desc Show error snackbar
          */
          function profileErrorFn(data, status, headers, config) {
            Snackbar.error(data.error);
          }
        }
      }
    })();


javascripts.html:
------------------
    <script type="text/javascript" src="{% static 'js/profiles/controllers/profile-settings.controller.js' %}"></script>



## template

static/templates/profiles/settings.html:
-----------------------------------------

    <div class="col-md-4 col-md-offset-4">
      <div class="well" ng-show="vm.profile">
        <form role="form" class="settings" ng-submit="vm.update()">
          <div class="form-group">
            <label for="settings__email">Email</label>
            <input type="text" class="form-control" id="settings__email" ng-model="vm.profile.email" placeholder="ex. john@example.com" />
          </div>

          <div class="form-group">
            <label for="settings__password">New Password</label>
            <input type="password" class="form-control" id="settings__password" ng-model="vm.profile.password" placeholder="ex. notgoogleplus" />
          </div>

          <div class="form-group">
            <label for="settings__confirm-password">Confirm Password</label>
            <input type="password" class="form-control" id="settings__confirm-password" ng-model="vm.profile.confirm_password" placeholder="ex. notgoogleplus" />
          </div>

          <div class="form-group">
            <label for="settings__username">Username</label>
            <input type="text" class="form-control" id="settings__username" ng-model="vm.profile.username" placeholder="ex. notgoogleplus" />
          </div>

          <div class="form-group">
            <label for="settings__tagline">Tagline</label>
            <textarea class="form-control" id="settings__tagline" ng-model="vm.profile.tagline" placeholder="ex. This is Not Google Plus." />
          </div>

          <div class="form-group">
            <button type="submit" class="btn btn-primary">Submit</button>
            <button type="button" class="btn btn-danger pull-right" ng-click="vm.destroy()">Delete Account</button>
          </div>
        </form>
      </div>
    </div>


## Profile settings route
static/js/restblog.routes.js:
-----------------------------
    // ...
    .when('/+:username/settings', {
      controller: 'ProfileSettingsController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/profiles/settings.html'
    })
    // ...

