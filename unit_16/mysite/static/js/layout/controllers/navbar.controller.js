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
