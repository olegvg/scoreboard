# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

import hashlib
from os import urandom

from sqlalchemy import Column, String, UnicodeText, Boolean

from bl_scoreboard.lib.database import Base, IdMixin


class Person(IdMixin, Base):
    __tablename__ = 'persons'

    login = Column(UnicodeText, unique=True, index=True)
    pin = Column(String(128))                      # Salted hash of password, fitted to SHA512
    salt = Column(String(128))                          # Crypto salt for password, fitted to SHA512
    is_blocked = Column(Boolean, index=True)            # disables login completely
    description = Column(UnicodeText)
    # 'orgs_assoc' column backref'ed from Person_x_Organizanion_Assoc

    def update_pin(self, plain_pin):
        self.salt = hashlib.sha256(urandom(32)).hexdigest()     # potentially DDoSable point because of urandom
        self.pin = hashlib.sha256(self.salt + plain_pin).hexdigest()

    def check_pin(self, plain_pin):
        return hashlib.sha256(self.salt + plain_pin).hexdigest() == self.pin