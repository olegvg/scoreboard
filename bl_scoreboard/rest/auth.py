# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from flask import Blueprint, current_app
from flask.ext.restful import Resource, reqparse

from ..lib.rest import Api
from ..lib.identity import ProtectedResource, login, logout, current_identity
from ..lib.auth import Identity


auth_bp = Blueprint('auth', __name__)
endpoint = Api(auth_bp, catch_all_404s=True)


class Login(Resource):
    def post(self):
        rp = reqparse.RequestParser()
        rp.add_argument('login', type=unicode, required=True)
        rp.add_argument('password', type=unicode, required=True)
        args = rp.parse_args()
        if login(Identity.authenticate(args['login'], args['password'])):
            current_app.logger.info('Login successful: ' + args['login'])
            return {'status': 'ok', 'login': current_identity.person.login}
        else:
            return {'status': 'fail'}, 419


class Logout(Resource):
    def post(self):
        if logout() is not None:
            return {'status': 'ok'}
        else:
            return {'status': 'not logged in'}, 403


class Status(ProtectedResource):
    def get(self):
        if current_identity.is_authenticated() is True:
            return {
                'status': 'logged in',
                'login': current_identity.person.login
            }
        else:
            return {'status': 'not logged in'}, 403

endpoint.add_resource(Login, '/login')
endpoint.add_resource(Logout, '/logout')
endpoint.add_resource(Status, '/status')