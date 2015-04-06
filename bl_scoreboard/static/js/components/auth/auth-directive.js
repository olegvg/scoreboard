/**
 * Created by ogaidukov on 25.06.14.
 */

define(['./auth', 'require'], function(auth, require) {
  'use strict';

  auth.directive('authForm', function() {
    return {
      restrict: 'E',
      templateUrl: require.toUrl('./auth-form.html'),
      controller: 'AuthFormCtrl'
    }
  });
});