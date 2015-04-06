# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from abc import ABCMeta, abstractmethod
import hashlib
from werkzeug.local import LocalProxy
from flask import _app_ctx_stack, session, current_app
from flask.ext.restful import Resource, abort

SESSION_IDENTITY_ATTRIBUTE = 'identity_idx'

current_identity = LocalProxy(lambda: getattr(_app_ctx_stack.top, 'identity', Anonymous()))


class IdentityMixin(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_authenticated(self):
        raise NotImplementedError("Can't authenticate in abstract class!")

    @abstractmethod
    def is_permanent_session(self):
        """
        Returns True, if session (browser cookie) must be stored in permanent manner. Affects flask.session behavior.
        """
        return False

    @abstractmethod
    def request_permissions(self, meth, requested_perms):
        raise NotImplementedError("Can't check permissions in abstract class!")

    @abstractmethod
    def get_identity_idx(self):
        return None


class Anonymous(IdentityMixin):
    def is_authenticated(self):
        return False

    def is_permanent_session(self):
        return False

    def request_permissions(self, meth, requested_perms):
        return False

    def get_identity_idx(self):
        return None


class RestAuthManager(object):
    def __init__(self, app=None, digest_method=hashlib.sha256):
        self.not_logged_in_cb = lambda: abort(403, result="Authentication needed!")
        self._load_identity = None
        self.digest_method = digest_method
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.rest_auth = self
        app.before_request(self._load_from_session)

    def _load_from_session(self):
        ctx = _app_ctx_stack.top
        identity_idx = session.get(SESSION_IDENTITY_ATTRIBUTE)
        identity = self._load_identity(identity_idx) if identity_idx else Anonymous()
        if identity:
            session.permanent = identity.is_permanent_session()
        ctx.identity = identity

    def not_logged_in_handler(self, cb):
        self.not_logged_in_cb = cb
        return cb

    def identity_loader(self, cb):
        self._load_identity = cb
        return cb


def login(identity):
    if identity.is_authenticated():  # implies has_app_context() == True
        session[SESSION_IDENTITY_ATTRIBUTE] = identity.get_identity_idx()
        _app_ctx_stack.top.identity = identity
        return True
    else:
        return False


def logout():
    return session.pop(SESSION_IDENTITY_ATTRIBUTE, None)


class ProtectedResource(Resource):
    permissions_needed = []

    def dispatch_request(self, *args, **kwargs):
        if current_identity.is_authenticated() is not True:
            return current_app.rest_auth.not_logged_in_cb()
        return super(ProtectedResource, self).dispatch_request(*args, **kwargs)
