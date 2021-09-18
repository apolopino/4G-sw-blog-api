"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, FavPeople, FavPlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    response = People.query.all()
    response = list(map(lambda x: x.serialize(), response))

    return jsonify(response), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_person(id):
    response = People.query.filter_by(id=id).first()
    response = response.serialize()

    return jsonify(response), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    response = Planets.query.all()
    response = list(map(lambda x: x.serialize(), response))

    return jsonify(response), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    response = Planets.query.filter_by(id=id).first()
    response = response.serialize()

    return jsonify(response), 200

@app.route('/users', methods=['GET'])
def get_users():
    response = User.query.all()
    response = list(map(lambda x: x.serialize(), response))

    return jsonify(response), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favs():
    body = request.get_json()
    user = body['user_id']

    response_people = FavPeople.query.filter_by(user_id=user).all()
    response_people = list(map(lambda x: x.serialize(), response_people))

    response_planet = FavPlanet.query.filter_by(user_id=user).all()
    response_planet = list(map(lambda x: x.serialize(), response_planet))

    response = {
        "Fav_People": response_people,
        "Fav_Planets": response_planet
    }

    return jsonify(response), 200

@app.route('/favorite/planet/<int:pid>', methods=['POST'])
def post_fav_planet(pid):
    body = request.get_json()
    user = body['user_id']

    element = FavPlanet(
        planet_id= pid,
        user_id=body['user_id'],
        )
    db.session.add(element)
    db.session.commit()

    response = FavPlanet.query.filter_by(user_id=user).all()
    response = list(map(lambda x: x.serialize(), response))

    return jsonify(response), 200

@app.route('/favorite/people/<int:pid>', methods=['POST'])
def post_fav_people(pid):
    body = request.get_json()
    user = body['user_id']

    element = FavPeople(
        people_id= pid,
        user_id=body['user_id'],
        )
    db.session.add(element)
    db.session.commit()

    response = FavPeople.query.filter_by(user_id=user).all()
    response = list(map(lambda x: x.serialize(), response))

    return jsonify(response), 200

@app.route('/favorite/planet/<int:pid>', methods=['DELETE'])
def delete_fav_planet(pid):
    element = FavPlanet.query.get(pid)
    body = request.get_json()
    user = body['user_id']

    if not user: 
        response = {
            "msg": "user not defined"
        }
        return jsonify(response), 200

    if not element:
        response = {
            "msg": "no such planet"
        }
        return jsonify(response), 200
    
    db.session.delete(element)
    db.session.commit()
    response = FavPlanet.query.filter_by(user_id=user).all()
    response = list(map(lambda x: x.serialize(), response))

    return jsonify(response), 200

@app.route('/favorite/people/<int:pid>', methods=['DELETE'])
def delete_fav_person(pid):
    element = FavPeople.query.get(pid)
    body = request.get_json()
    user = body['user_id']

    if not user: 
        response = {
            "msg": "user not defined"
        }
        return jsonify(response), 200

    if not element:
        response = {
            "msg": "no such person"
        }
        return jsonify(response), 200
    
    db.session.delete(element)
    db.session.commit()
    response = FavPeople.query.filter_by(user_id=user).all()
    response = list(map(lambda x: x.serialize(), response))

    return jsonify(response), 200




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
