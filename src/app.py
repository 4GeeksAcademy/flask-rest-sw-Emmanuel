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
from models import db, User , Characters , Planets , Ships , CharacterFavorites, PlanetsFavorites, ShipsFavorites

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

@app.route('/users', methods=['GET'])
def getUsers():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/users', methods=['POST'])
def postUsers():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def getPeople():
    people = Characters.query.all()
    result = []
    for person in people:
        result.append({
            'id': person.id,
            'name': person.name,
        })
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body+result), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def getOnePeople(char_id):
    person = Characters.query.get(char_id)
    if person:
        result = {
            'id': person.id,
            'name': person.name,
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Person not found'}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    result = []
    for planet in planets:
        result.append({
            'id': planet.id,
            'name': planet.name,
        })
    return jsonify(result)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        result = {
            'id': planet.id,
            'name': planet.name,
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Planet not found'}), 404

@app.route('/ships', methods=['GET'])
def getShips():
    ships = Ships.query.all()
    result = []
    for ship in ships:
        result.append({
            'id': ship.id,
            'name': ship.name,
        })
    return jsonify(result)

@app.route('/ships/<int:ship_id>', methods=['GET'])
def getOneShip(ship_id):
    ship = Ships.query.get(ship_id)
    if ship:
        result = {
            'id': ship.id,
            'name': ship.name,
        }
        return jsonify(result)
    else:
        return jsonify({'message': 'Planet not found'}), 404

@app.route('/users/favorites', methods=['GET'])
def getFavorites():
    favoriteChar = CharacterFavorites.query.all()
    favoriteChar = CharacterFavorites.query.all()
    favoriteChar = CharacterFavorites.query.all()
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def getFavorites():
    
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def getFavorites():
    
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/favorite/ships/<int:ship_id>', methods=['POST'])
def getFavorites():
    
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
