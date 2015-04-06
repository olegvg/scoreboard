/**
 * Created by ogaidukov on 07.04.14.
 */

define([
    'angular',

    /* call loaders here */
    'components/lib/index',
    'components/auth/index',
    'components/pages/index'

  ],
  function(angular) {
    'use strict';

    var app = angular.module('blScoreboard', [
        'ngRoute',
        'ui.select2',

        /* set submodules as dependencies here */
        'lib',
        'auth',
        'pages'

      ]
    );

    app.init = function () {
      angular.bootstrap(document, ['blScoreboard']);
    };

    return app;
  }
);
