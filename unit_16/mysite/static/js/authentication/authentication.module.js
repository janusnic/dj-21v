/**
* Authentication
* @namespace restblog.authentication.services
*/

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
