# Forntend. Preparation of development environment.

## 1. _node.js_ installatin using _brew_ on Mac OS X

    brew install node

## 2. Installation of dependencies.

    cd bl-scoreboard
    
    npm cache clear
    npm cache clean
    
    npm install
    
    export PATH=`pwd`/node_modules/.bin:$PATH

## 3. Installation of runtime-development dependencies (_angular_, _bootstrap_).

    grunt build-dev

## 4. Preparation of deployment environment (uglify, less compilation, css minify) in the _dist_ directory.

    grunt build-dist

## 5. Cleaning up.

Cleaning up of `deployment`
    
    grunt clean-dist

Cleaning of `devel`
    
    grunt clean-dev

Beware of the fact that `grunt clean-dev` doesn't clean up _requirejs_ dependencies in `bl_scoreboard/static/js/main.js`. It's up to you to keep these dependencies up to date.

