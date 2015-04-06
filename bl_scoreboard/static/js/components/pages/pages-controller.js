/**
 * Created by ogaidukov on 25.06.14.
 */

define(['./pages'], function(pages) {
  'use strict';

  /* Auth operations controller: checks auth status and offers logout func */
  pages.controller('AuthOpsCtrl', ['$scope', '$http', '$route', 'Authenticator', function($scope, $http, $route, Authenticator) {
    // Update login name when already logged in via getting auth status
    $http.get('../auth/status').success(function(data) {
      $scope.isLoggedIn = true;
      $scope.login = data.login
    });

    // Update login name immediately after finishing login process. 'data' is the result of '../auth/login' API call
    Authenticator.listenForLoginDone(function(data) {
      $scope.isLoggedIn = true;
      $scope.login = data.login
    });

    $scope.loginClick = function() {
      $scope.isLoggedIn = false;
      $scope.login = '';
      $route.reload()
    };
    $scope.logoutClick = function() {
      $http.post('../auth/logout', {}).success(function(data) {
        $scope.isLoggedIn = false;
        $scope.login = '';
        $route.reload() });
    }
  }]);

  pages.controller('NavSearchPhoneCtrl', [
    '$scope',
    '$location',
    '$http',
    function($scope, $location, $http) {
      $scope.s2SearchOptions = {
        minimumInputLength: 3,
        width: '200px',
        allowClear: true,
        ajax: {
          data: function (term, page) {
            return { query: term };
          },
          quietMillis: 500,
          transport: function(query) {
            $http.post('../gamers/search_by_phone', query.data).then(query.success)
          },
          results: function (data, page) {
            return { results: $.map(data.data, function(item) { return {id: item, text: item} }) };
          }
        }
      };

      $scope.phoneSearchClick = function() {
        $location.url('gamer/' + $scope.searchPhone.text);
//        $scope.searchPhone = '';
      }
    }
  ]);

  pages.controller('GamerDetailsCtrl', [
    '$scope',
    '$routeParams',
    '$location',
    '$http',
    function($scope, $routeParams, $location, $http) {
      $scope.s2GameTagsOptions = {
        multiple: true,
        ajax: {
          data: function (term, page) {
            return { query: term };
          },
          quietMillis: 500,
          transport: function(query) {
            $http.post('../gamers/available_games', query.data).then(query.success)
          },
          results: function (data, page) {
            return { results: $.map(data.data, function(item) { return {id: item, text: item} }) };
          }
        }
      };

      $scope.gamer = {
        score: {}
      };

      // Update scores in '$scope.gamer.score' according to changes of 'selectGame' model (select2 widget)
      $scope.$watchCollection('selectGame', function(newData) {
        if(newData) {
          var selectedKeys = $.map(newData, function (item) {
            return item.id
          });
          var scores = {};
          for (var key in $scope.gamer.score) {
            if ($.inArray(key, selectedKeys) > -1) {
              scores[key] = $scope.gamer.score[key]
            }
          }
          $scope.gamer.score = scores;
      }});

      if($routeParams.phoneNum) {
        $scope.detailsMode = 'edit';

        $http.get('../gamers/mangle_gamer', {
          params: { phone: $routeParams.phoneNum }
        }).then(function(res) {
          $scope.selectGame = $.map(res.data.score, function(item, key) { return {id: key, text: key} });
          $scope.gamer = res.data;
          if(res.data.prize_given) {
            $scope.alertPrizeGivenModal.show()
          }
        })
      } else {
        $scope.detailsMode = 'new';
      }

      $scope.adjClick = function(gameId, val) {
        if(typeof $scope.gamer.score[gameId] === 'number')
          $scope.gamer.score[gameId] += val;
        else
          $scope.gamer.score[gameId] = val
      };

      $scope.submitClick = function() {
        if($scope.detailsMode === 'edit') {
          $http.put('../gamers/mangle_gamer', $scope.gamer).then(function(){
            $location.url('/')
          })
        } else if($scope.detailsMode === 'new') {
          $http.post('../gamers/mangle_gamer', $scope.gamer)
            .success(function() { $location.url('/')})
            .error(function(d, status) { if(status == 409 ) { $scope.gamerAlreadyRegistered.show() }})
        }
      };

      $scope.prizeGivenClick = function() {
        $scope.prizeGivenModal.show();
      };

      $scope.prizeGivenAcceptClick = function() {
        $scope.gamer.prize_given = true;

        $scope.prizeGivenModal.hide().then(function() {
          if($scope.detailsMode === 'edit') {
            $http.put('../gamers/mangle_gamer', $scope.gamer).then(function(){
              $location.url('/')
            })
          } else if($scope.detailsMode === 'new') {
            $http.post('../gamers/mangle_gamer', $scope.gamer)
              .success(function() { $location.url('/')})
              .error(function(d, status) { if(status == 409 ) { $scope.gamerAlreadyRegistered.show() }})
          }
        })
      };

      $scope.leaveGamerDetailsClick = function() {
        $scope.alertPrizeGivenModal.hide().then(function() { $location.url('/') })
      }
    }
  ]);

  pages.controller('ScoreboardCtrl', [
    '$scope',
    '$route',
    '$http',
    function($scope, $route, $http) {
      $http.get('../gamers/get_scoreboard').then(function(res){
        $scope.scoreBoard = res.data
      });
    }])
});