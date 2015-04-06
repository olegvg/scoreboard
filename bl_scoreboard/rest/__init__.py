# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from auth import auth_bp
from gamers import gamers_bp


def init_blueprint(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(gamers_bp, url_prefix='/gamers')