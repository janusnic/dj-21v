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
