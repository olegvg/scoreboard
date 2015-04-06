# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from bl_scoreboard import model
from bl_scoreboard.model import Base

# SQLA_URL_TEST = 'postgresql://me_advert:1qazxsw2@int.ovg.me:5432/bl-scoreboard-test'
SQLA_URL_TEST = 'sqlite:///../tmp/scoreboard.db'


def init_sqla(sqla_url):

    engine = create_engine(sqla_url, echo=True)
    sqla_session = scoped_session(sessionmaker(autocommit=True,
                                               autoflush=False,
                                               bind=engine))
    Base.query = sqla_session.query_property()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return sqla_session


def fillup_db(session):
    objects = []

    p = model.Person()
    p.login = u'promo'
    p.update_pin(u'1234')
    p.is_blocked = False

    g1 = model.Game()
    g1.name = u'Шашки'
    objects.append(g1)

    g2 = model.Game()
    g2.name = u'Шахматы'
    objects.append(g2)

    g3 = model.Game()
    g3.name = u'Бокс'
    objects.append(g3)

    objects.append(p)
    session.begin()
    session.add_all(objects)
    session.commit()


if __name__ == '__main__':
    print "init"
    session = init_sqla(SQLA_URL_TEST)
    fillup_db(session)