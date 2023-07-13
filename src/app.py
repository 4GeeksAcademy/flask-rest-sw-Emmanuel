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
    users = User.query.all()
    
    user_list = []
    for user in users:
        user_data = {
            "username": user.username,
            "email": user.email,
            "password":user.password
        }
        user_list.append(user_data)

    return jsonify(user_list), 200

@app.route('/characters', methods=['GET'])
def getCharacters():
    characters = Characters.query.all()
    
    character_list = []
    for character in characters:
        character_data = {
            "id": character.id,
            "name": character.name,
            "birth_date": character.birth_date,
            "height": character.height,
            "hair_color": character.hair_color,
            "eye_color": character.eye_color,
            "gender": character.gender
        }
        character_list.append(character_data)

    return jsonify(character_list), 200

@app.route('/planets', methods=['GET'])
def getPlanets():
    planets = Planets.query.all()
    
    planet_list = []
    for planet in planets:
        planet_data = {
            "id": planet.id,
            "name": planet.name,
            "population": planet.population,
            "diameter": planet.diameter,
            "climate": planet.climate,
            "gravity": planet.gravity,
            "terrain": planet.terrain
        }
        planet_list.append(planet_data)

    return jsonify(planet_list), 200

@app.route('/ships', methods=['GET'])
def getShips():
    ships = Ships.query.all()
    
    ship_list = []
    for ship in ships:
        ship_data = {
            "id": ship.id,
            "name": ship.name,
            "model": ship.model,
            "max_speed": ship.max_speed,
            "passengers": ship.passengers,
            "starship_class": ship.starship_class
        }
        ship_list.append(ship_data)

    return jsonify(ship_list), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def getUserId(user_id):
    user_name = User.query.get("username")
    user = User.query.get(user_id)
    user.username = user_name
    db.session.commit()
    return ("updated user:"+user),200
    
@app.route('/users/<int:user_id>', methods=['PUT'])
def upUserId(user_id):
    new_name=request.json.get()
    user = User.query.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error":"el usuario no existe"}),404

@app.route('/users/favorites', methods=['GET'])
def getUsersFav():

    favorite_character = [elem.character_id for elem in CharacterFavorites.query.all()]
    favorite_planets = [elem.planet_id for elem in PlanetsFavorites.query.all()]
    favorite_ships = [elem.starship_id for elem in ShipsFavorites.query.all()]

    favorites = {
        'character': favorite_character,
        'planets': favorite_planets,
        'ships': favorite_ships
    }
    
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(favorites), 200

@app.route('/users', methods=['POST'])
def postUsers():
    user_data = request.json
    user = User(username=user_data['username'], email=user_data['email'], password=user_data['password'])
    db.session.add(user)
    db.session.commit()

    response_body = {
        "username": user.username,
        "email": user.email,
        "password":user.password
    }
    return jsonify(response_body), 200


@app.route('/characters', methods=['POST'])
def postCharacter():
    character_data = request.json
    character = Characters(name=character_data['name'], birth_date=character_data['birth_date'], height=character_data['height'], hair_color=character_data['hair_color'], eye_color=character_data['eye_color'], gender=character_data['gender'])
    db.session.add(character)
    db.session.commit()

    response_body = {
        "id": character.id,
        "name": character.name,
        "birth_date": character.birth_date,
        "height": character.height,
        "hair_color": character.hair_color,
        "eye_color": character.eye_color,
        "gender": character.gender
    }

    return jsonify(response_body), 200

@app.route('/planets', methods=['POST'])
def postPlanet():
    planet_data = request.json
    planet = Planets(name=planet_data['name'], population=planet_data['population'], diameter=planet_data['diameter'], climate=planet_data['climate'], gravity=planet_data['gravity'], terrain=planet_data['terrain'])
    db.session.add(planet)
    db.session.commit()

    response_body = {
        "id": planet.id,
        "name": planet.name,
        "population": planet.population,
        "diameter": planet.diameter,
        "climate": planet.climate,
        "gravity": planet.gravity,
        "terrain": planet.terrain
    }

    return jsonify(response_body), 200

@app.route('/ships', methods=['POST'])
def postShip():
    ship_data = request.json
    ship = Ships(name=ship_data['name'], model=ship_data['model'], max_speed=ship_data['max_speed'], passengers=ship_data['passengers'], starship_class=ship_data['starship_class'])
    db.session.add(ship)
    db.session.commit()

    response_body = {
        "id": ship.id,
        "name": ship.name,
        "model": ship.model,
        "max_speed": ship.max_speed,
        "passengers": ship.passengers,
        "starship_class": ship.starship_class
    }

    return jsonify(response_body), 200






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

# @app.route('/users/favorites', methods=['GET'])
# def getFavorites():
    
#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200


# @app.route('/favorite/people/<int:people_id>', methods=['POST'])
# def getFavorites(people_id):
    
#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

# @app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
# def getFavorites(planet_id):
    
#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

# @app.route('/favorite/ships/<int:ship_id>', methods=['POST'])
# def getFavorites(ship_id):
    
#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

# @app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
# def deleteFavorites(people_id):
    
#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

# @app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
# def deleteFavorites(planet_id):
    
#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

# @app.route('/favorite/ships/<int:ship_id>', methods=['DELETE'])
# def deleteFavorites(ship_id):
    
#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
