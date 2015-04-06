# -*- coding: utf-8 -*-

__author__ = 'ogaidukov'

from flask import Blueprint
from flask.ext.restful import reqparse
from ..lib.rest import Api
from ..lib.identity import ProtectedResource
from ..model.gamers import Game, Gamer, Gamers_x_Games_Assoc
from ..lib.database import sqla_session
from sqlalchemy import not_, func, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from ..lib.database import compile_query


gamers_bp = Blueprint('gamers', __name__)
endpoint = Api(gamers_bp, catch_all_404s=True)


class SearchByPhone(ProtectedResource):
    def post(self):
        rp = reqparse.RequestParser()
        rp.add_argument('query', type=unicode, required=True)
        args = rp.parse_args()

        like_arg = u"%{}%".format(args.query)
        gamers = Gamer.query.filter(Gamer.phone.ilike(like_arg)).all()

        return [x.phone for x in gamers]


class AvailableGames(ProtectedResource):
    def post(self):
        rp = reqparse.RequestParser()
        rp.add_argument('query', type=unicode, required=True)
        args = rp.parse_args()

        like_arg = u"%{}%".format(args.query)
        games = Game.query.filter(Game.name.ilike(like_arg)).all()

        return [x.name for x in games]


class MangleGamer(ProtectedResource):
    def post(self):
        """
        Creates a new gamer
        """
        rp = reqparse.RequestParser()
        rp.add_argument('name', type=unicode, required=True)
        rp.add_argument('phone', type=unicode, required=True)
        rp.add_argument('score', type=dict)
        rp.add_argument('prize_given', type=bool)
        args = rp.parse_args()

        # sqla_session.begin()
        rows = []
        gamer = Gamer(phone=args.phone, name=args.name, is_prize_given=True if args.prize_given else False)
        rows.append(gamer)
        if args.score:
            selected_games = Game.query.filter(Game.name.in_(args.score.keys())).all()
            for game in selected_games:
                score = Gamers_x_Games_Assoc(gamer=gamer, game=game, score=args.score[game.name])
                rows.append(score)
        sqla_session.add_all(rows)
        try:
            sqla_session.commit()
        except IntegrityError:
            return {'status': 'already registered'}, 409

    def put(self):
        """
        Updates existing gamer's score, and data except phone number
        """
        rp = reqparse.RequestParser()
        rp.add_argument('name', type=unicode, required=True)
        rp.add_argument('phone', type=unicode, required=True)
        rp.add_argument('score', type=dict)
        rp.add_argument('prize_given', type=bool)
        args = rp.parse_args()

        gamer = Gamer.query.filter_by(phone=args.phone).first()
        gamer.name = args.name
        gamer.is_prize_given = True if args.prize_given else False

        # Scores to be delete
        scores_to_delete = Gamers_x_Games_Assoc.query \
            .join(Game.scores_assoc) \
            .join(Gamers_x_Games_Assoc.gamer) \
            .filter(not_(Game.name.in_(args.score.keys())),
                    Gamer.id == gamer.id)\
            .all()
        for score_to_delete in scores_to_delete:
            sqla_session.delete(score_to_delete)

        # Scores to be update
        scores_to_update = Gamers_x_Games_Assoc.query \
            .join(Game.scores_assoc) \
            .join(Gamers_x_Games_Assoc.gamer) \
            .options(joinedload(Gamers_x_Games_Assoc.game)) \
            .filter(Game.name.in_(args.score.keys()),
                    Gamer.id == gamer.id)\
            .all()
        for score_obj in scores_to_update:
            score_obj.score = args.score[score_obj.game.name]

        # Scores to be create
        games_of_gamer_q = Game.query \
            .join(Gamer.scores_assoc) \
            .join(Gamers_x_Games_Assoc.game) \
            .filter(Gamer.id == gamer.id)
        games_to_create = Game.query \
            .filter(Game.name.in_(args.score.keys()))\
            .except_(games_of_gamer_q) \
            .all()
        new_scores = []
        for new_game_score in games_to_create:
            new_score = Gamers_x_Games_Assoc(gamer=gamer, game=new_game_score, score=args.score[new_game_score.name])
            new_scores.append(new_score)
        sqla_session.add_all(new_scores)
        sqla_session.commit()

    def get(self):
        """
        Returns the gamer's data
        """
        rp = reqparse.RequestParser()
        rp.add_argument('phone', type=unicode, required=True)
        args = rp.parse_args()

        res = {'score': {}}
        gamer = Gamer.query.filter_by(phone=args.phone).first()
        res.update({
            'name': gamer.name,
            'phone': gamer.phone,
            'prize_given': gamer.is_prize_given
        })
        for score in gamer.scores_assoc:
            game_name = score.game.name.encode('utf-8')
            res['score'][game_name] = score.score
        return res


class GetScoreboard(ProtectedResource):
    def get(self):
        scores = sqla_session.query(Gamer, func.sum(Gamers_x_Games_Assoc.score).label('sum_score')) \
            .join(Gamer.scores_assoc) \
            .filter(Gamer.is_prize_given.is_(False)) \
            .group_by(Gamer) \
            .order_by(desc('sum_score')) \
            .limit(30) \
            .all()
        return [{'phone': x[0].phone, 'name': x[0].name, 'score': x[1]} for x in scores]

endpoint.add_resource(SearchByPhone, '/search_by_phone')
endpoint.add_resource(AvailableGames, '/available_games')
endpoint.add_resource(MangleGamer, '/mangle_gamer')
endpoint.add_resource(GetScoreboard, '/get_scoreboard')
