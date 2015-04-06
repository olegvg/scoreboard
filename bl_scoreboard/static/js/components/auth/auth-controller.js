/**
 * Created by ogaidukov on 28.04.14.
 */

define(['./auth'], function(auth) {
  'use strict';

  /*
    Controller of modal authentication window. It handles 'login' and 'cancel' buttons and tries to authenticate
    against credentials which specified in $scope.user (user.login & user.password)
  */
  auth.controller('AuthFormCtrl', ['$scope', '$http', 'Authenticator', function($scope, $http, Authenticator) {
    $scope.user = {};
    Authenticator.listenForAuthStatusChange(function(status) {
      if(status === 'login-needed') {
        $scope.showAuthError = false
      }
      if(status === 'login-unsuccessfull') {
        $scope.showAuthError = true
      }
    });

    $scope.authenticate = function() {
      if($scope.userAuthForm.$valid) {
        $http.post('../auth/login', $scope.user)
          .success(Authenticator._getLoginDeferred().resolve)
          .error(Authenticator._getLoginDeferred().reject);
      }
    };

    $scope.cancel = function() { Authenticator._getLoginDeferred().reject() }
  }])
});
