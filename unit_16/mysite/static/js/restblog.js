(function () {
  'use strict';

  angular
    .module('restblog', [
      'restblog.config',
      'restblog.routes',
      'restblog.accounts',
      'restblog.authentication',
      'restblog.layout',
      'restblog.posts',
      'restblog.utils'
    ]);

  angular
    .module('restblog.config', []);

  angular
    .module('restblog.routes', ['ngRoute']);

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
})();
