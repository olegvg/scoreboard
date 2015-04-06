/**
 * Created by ogaidukov on 25.06.14.
 */

define(['./app'], function (app) {
     'use strict';

     return app.config(['$routeProvider', function ($routeProvider) {

         $routeProvider.when('/gamer', {
           templateUrl: 'js/components/pages/gamer-details.html',
           controller: 'GamerDetailsCtrl'
         });

         $routeProvider.when('/gamer/:phoneNum', {
           templateUrl: 'js/components/pages/gamer-details.html',
           controller: 'GamerDetailsCtrl'
         });

         $routeProvider.when('/', {
           templateUrl: 'js/components/pages/scoreboard.html',
           controller: 'ScoreboardCtrl'
         });

     }]);
});