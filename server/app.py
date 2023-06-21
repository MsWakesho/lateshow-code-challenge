#!/usr/bin/env python3

from models import db, Episode, Guest, Appearance
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'


class Episodes(Resource):
    def get(self):
        episodes = [episode.to_dict(rules=('-appearances',))
                    for episode in Episode.query.all()]

        return make_response(episodes, 200)


api.add_resource(Episodes, "/episodes")


class EpisodesById(Resource):

    def get(self, id):
        episode = Episode.query.filter_by(id=id).one_or_none()

        if episode is None:
            return make_response({'error': 'Episode not found'}, 404)

        return make_response(episode.to_dict(), 200)

    def delete(self, id):
        episode = Episode.query.filter_by(id=id).one_or_none()

        if episode is None:
            return make_response({'error': 'Episode not found'}, 404)

        # deletes should cascade if configured in model
        db.session.delete(episode)
        db.session.commit()
        return make_response({}, 204)


api.add_resource(EpisodesById, "/episodes/<int:id>")


class Guests(Resource):
    def get(self):
        guests = [guest.to_dict(rules=('-appearances',))
                  for guest in Guest.query.all()]

        return make_response(guests, 200)


api.add_resource(Guests, "/guests")


class Appearances(Resource):
    def post(self):
        try:
            fields = request.get_json()
            appearance = Appearance(
                rating=fields.get('rating'),
                episode_id=fields.get('episode_id'),
                guest_id=fields.get('guest_id'),
            )

            db.session.add(appearance)
            db.session.commit()

            return make_response(appearance.to_dict(), 201)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)


api.add_resource(Appearances, "/appearances")

if __name__ == '__main__':
    app.run(port=5555, debug=True)