/**
 * Created by ogaidukov on 25.06.14.
 */

define(['./auth'], function(auth) {
  'use strict';

  auth.config(['$httpProvider', function($httpProvider){
      $httpProvider.interceptors.push('AuthInterceptor');
    }]);

});