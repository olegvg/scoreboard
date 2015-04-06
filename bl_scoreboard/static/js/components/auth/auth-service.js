/**
 * Created by ogaidukov on 07.04.14.
 */

define(['./auth'], function(auth) {
  'use strict';

    /*
      'Authenticator' service holds 'login' method which shows login modal window
      (it must be included as <auth-form></auth-form> into e.g. index.html)
    */
    auth.factory('Authenticator', ['$q', '$rootScope', function($q, $rootScope) {
      var _authDeferred;
      return {
        login: function() {
          _authDeferred = $q.defer();
          _authDeferred.promise.then(function(res) { $rootScope.$broadcast('authLoginDone', res) });
          _authDeferred.promise.finally(function() { angular.element('#authModal').modal('hide') });
          angular.element('#authModal').modal('show');
          return _authDeferred.promise
        },
        _getLoginDeferred: function() { return _authDeferred },
        _broadcastAuthStatus: function(val) { $rootScope.$broadcast('authStatus', val) },
        listenForAuthStatusChange: function(fn) { $rootScope.$on('authStatus', function(e, val) { fn(val) }) },
        listenForLoginDone: function(fn) { $rootScope.$on('authLoginDone', function(e, val) { fn(val) }) }
      }
    }]);

    /*
      Interceptor service which is being registered to $http, catches auth errors of http rest api call and
      tries to authenticate through 'Authenticator.login()' then restarts http api call
     */
    auth.factory('AuthInterceptor', ['$injector', '$q', function($injector, $q) {
      return {
        responseError: function(response) {
          var $http = $injector.get('$http');
          var Authenticator = $injector.get('Authenticator');
          switch(response.status) {
            case 403: /* Authentication needed */
//            case 401: /* Unsufficient permissions. Needs different handler (?) */
              Authenticator._broadcastAuthStatus('login-needed');
              return Authenticator.login().then(function() { return $http(response.config) });
            case 419: /* Login or password are wrong. Retry needed */
              Authenticator._broadcastAuthStatus('login-unsuccessfull');
              return Authenticator.login().then(function() { return $http(response.config) })
          }
          return $q.reject(response)
        }
      }
    }])
});