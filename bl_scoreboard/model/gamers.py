# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from sqlalchemy import Column, ForeignKey, Integer, UnicodeText, Boolean
from sqlalchemy.orm import relationship, backref

from bl_scoreboard.lib.database import Base, IdMixin


class Gamers_x_Games_Assoc(Base):
    __tablename__ = 'gamers_x_games_assocs'

    # allow cascaded removal of gamer along with its assco'd rows
    gamer_ref = Column(Integer, ForeignKey('gamers.id', ondelete='cascade'),
                       nullable=False, index=True, primary_key=True)
    # prohibit cascaded removal of game along with its assco'd rows
    game_ref = Column(Integer, ForeignKey('games.id', ondelete='restrict'),
                      index=True, primary_key=True)
    gamer = relationship("Gamer", backref=backref('scores_assoc', cascade='all,delete-orphan'))
    game = relationship("Game", backref='scores_assoc')
    score = Column(Integer)


class Game(IdMixin, Base):
    __tablename__ = 'games'

    name = Column(UnicodeText)
    # 'scores_assoc' column backref'ed from Gamers_x_Games_Assoc


class Gamer(IdMixin, Base):
    __tablename__ = 'gamers'

    phone = Column(UnicodeText, unique=True, index=True)
    name = Column(UnicodeText, index=True)
    is_prize_given = Column(Boolean, index=True, default=False)
    # 'scores_assoc' column backref'ed from Gamers_x_Games_Assoc

