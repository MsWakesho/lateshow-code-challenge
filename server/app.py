#!/usr/bin/env python3

from models import db, Episode, Guest, Appearance
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
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

@app.route('/')
def index():
    return '<h1>LATE SHOW </h1>'

@app.route('/episodes', methods=['GET'])
def episodes():
    if request.method == 'GET':
        episodes = Episode.query.all()
        print("Episodes:", episodes) 
        episode_dicts = [episode.to_dict() for episode in episodes]
        print("Episode JSON:", episode_dicts) 
        return make_response(jsonify(episode_dicts), 200)

        
@app.route('/episodes/<int:id>', methods=['GET', 'DELETE'])
def episode_by_id(id):
    if request.method == 'GET':
        episode = Episode.query.filter_by(id=id).first()

        if episode is None:
            return jsonify({"error": "Episode not found"}), 404

        episode_data = {
            "id": episode.id,
            "date": episode.date,
            "number": episode.number,
            "appearances": []
        }

        for appearance in episode.appearances:
            appearance_data = {
                "id": appearance.id,
                "episode_id": appearance.episode_id,
                "guest": {
                    "id": appearance.guest.id,
                    "name": appearance.guest.name,
                    "occupation": appearance.guest.occupation
                },
                "guest_id": appearance.guest_id,
                "rating": appearance.rating
            }

            episode_data["appearances"].append(appearance_data)

        return jsonify(episode_data)

    elif request.method == 'DELETE':
        episode = Episode.query.filter_by(id=id).first()

        if episode is None:
            return jsonify({"error": "Episode not found"}), 404

        db.session.delete(episode)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Episode deleted."
        }

        response = make_response(response_body, 200)

        return response

@app.route('/guests', methods=['GET'])
def guests():
    if request.method == 'GET':
        guests = Guest.query.all()

        return make_response(
            jsonify([guest.to_dict() for guest in guests]), 200
        )
        
        
@app.route('/appearances', methods= ['POST'])
def create_appearances():
    if request.method == 'POST':
        
        data = request.json
        rating = data.get('rating')
        episode_id = data.get('episode_id')
        guest_id = data.get('guest_id')
        
        if not all([rating, episode_id,guest_id ]):
            return jsonify({"errors":["Missing required fields"]}),400
        
        episode = Episode.query.get(episode_id)
        guest = Guest.query.get(guest_id)
        
        if not episode or not guest:
            return jsonify({"errors": ['Episode or guest not found']}), 404
        
        
        appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
        db.session.add(appearance)
        db.session.commit()
        
        appearance_data = {
            "id":appearance.id,
            "rating":appearance.rating,
            "guest_id":appearance.guest_id,
            "episode_id":appearance.episode_id,
            "episode":{
                "id":episode.id,
                "date":episode.date,
                "number":episode.number
            },
            "guest":{
                "id":guest.id,
                "name":guest.name,
                "occupation":guest.occupation
            }
        }
        
        return jsonify(appearance_data), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
