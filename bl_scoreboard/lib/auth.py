# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from identity import IdentityMixin
from ..model.auth import Person
from sqlalchemy.orm import exc


class Identity(IdentityMixin):
    def __init__(self):
        self._is_authenticated = False
        self._person = None

    def is_authenticated(self):
        return self._is_authenticated

    def is_permanent_session(self):
    # TODO make as option stored in user profile
        return True

    def request_permissions(self, meth, requested_perms):
        return False

    def get_identity_idx(self):
        if isinstance(self._person, Person):
            ident = self._person.login
        else:
            ident = None
        return ident

    @property
    def person(self):
        return self._person

    @classmethod
    def authenticate(cls, user, pin):
        identity = cls()
        try:
            identity._person = Person.query.filter_by(login=user, is_blocked=False).one()
        except exc.NoResultFound:
            identity._is_authenticated = False
            return identity
        identity._is_authenticated = identity._person.check_pin(pin)
        return identity

    @classmethod
    def get_identity(cls, identity_idx):
        identity = cls()
        try:
            identity._person = Person.query.filter_by(login=identity_idx, is_blocked=False).one()
            identity._is_authenticated = True
        except exc.NoResultFound:
            pass
        return identity
