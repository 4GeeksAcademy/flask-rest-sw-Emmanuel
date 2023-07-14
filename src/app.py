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
            "id": user.id,
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
def getUser(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }

    return jsonify(user_data), 200

    
@app.route('/characters/<int:character_id>', methods=['GET'])
def getCharacter(character_id):
    character = Characters.query.get(character_id)

    if character is None:
        return jsonify({"error": "Character not found"}), 404

    character_data = {
        "id": character.id,
        "name": character.name,
        "birth_date": character.birth_date,
        "height": character.height,
        "hair_color": character.hair_color,
        "eye_color": character.eye_color,
        "gender": character.gender
    }

    return jsonify(character_data), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def getPlanet(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    planet_data = {
        "id": planet.id,
        "name": planet.name,
        "population": planet.population,
        "diameter": planet.diameter,
        "climate": planet.climate,
        "gravity": planet.gravity,
        "terrain": planet.terrain
    }

    return jsonify(planet_data), 200

@app.route('/ships/<int:ship_id>', methods=['GET'])
def getShip(ship_id):
    ship = Ships.query.get(ship_id)

    if ship is None:
        return jsonify({"error": "Ship not found"}), 404

    ship_data = {
        "id": ship.id,
        "name": ship.name,
        "model": ship.model,
        "max_speed": ship.max_speed,
        "passengers": ship.passengers,
        "starship_class": ship.starship_class
    }

    return jsonify(ship_data), 200

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

@app.route('/users/<int:user_id>', methods=['PUT'])
def updateUser(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    updated_data = request.get_json()

    user.username = updated_data.get('username', user.username)
    user.email = updated_data.get('email', user.email)
    user.password = updated_data.get('password', user.password)

    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

@app.route('/characters/<int:character_id>', methods=['PUT'])
def updateCharacter(character_id):
    character = Characters.query.get(character_id)

    if character is None:
        return jsonify({"error": "Character not found"}), 404

    updated_data = request.get_json()

    character.name = updated_data.get('name', character.name)
    character.birth_date = updated_data.get('birth_date', character.birth_date)
    character.height = updated_data.get('height', character.height)
    character.hair_color = updated_data.get('hair_color', character.hair_color)
    character.eye_color = updated_data.get('eye_color', character.eye_color)
    character.gender = updated_data.get('gender', character.gender)

    db.session.commit()

    return jsonify({"message": "Character updated successfully"}), 200


@app.route('/planets/<int:planet_id>', methods=['PUT'])
def updatePlanet(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    updated_data = request.get_json()

    planet.name = updated_data.get('name', planet.name)
    planet.population = updated_data.get('population', planet.population)
    planet.diameter = updated_data.get('diameter', planet.diameter)
    planet.climate = updated_data.get('climate', planet.climate)
    planet.gravity = updated_data.get('gravity', planet.gravity)
    planet.terrain = updated_data.get('terrain', planet.terrain)

    db.session.commit()

    return jsonify({"message": "Planet updated successfully"}), 200

@app.route('/ships/<int:ship_id>', methods=['PUT'])
def updateShip(ship_id):
    ship = Ships.query.get(ship_id)

    if ship is None:
        return jsonify({"error": "Ship not found"}), 404

    updated_data = request.get_json()

    ship.name = updated_data.get('name', ship.name)
    ship.model = updated_data.get('model', ship.model)
    ship.max_speed = updated_data.get('max_speed', ship.max_speed)
    ship.passengers = updated_data.get('passengers', ship.passengers)
    ship.starship_class = updated_data.get('starship_class', ship.starship_class)

    db.session.commit()

    return jsonify({"message": "Ship updated successfully"}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def deleteUser(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200

@app.route('/characters/<int:character_id>', methods=['DELETE'])
def deleteCharacter(character_id):
    character = Characters.query.get(character_id)

    if character is None:
        return jsonify({"error": "Character not found"}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({"message": "Character deleted successfully"}), 200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def deletePlanet(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()

    return jsonify({"message": "Planet deleted successfully"}), 200

@app.route('/ships/<int:ship_id>', methods=['DELETE'])
def deleteShip(ship_id):
    ship = Ships.query.get(ship_id)

    if ship is None:
        return jsonify({"error": "Ship not found"}), 404

    db.session.delete(ship)
    db.session.commit()

    return jsonify({"message": "Ship deleted successfully"}), 200

@app.route('/users/favorites', methods=['GET'])
def getUserFavorites():
    user_id = get_current_user_id()  

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    favorites_list = []

    character_favorites = CharacterFavorites.query.filter_by(user=user_id).all()
    for favorite in character_favorites:
        character = Characters.query.get(favorite.char_id)
        if character:
            favorites_list.append({
                "favorite_id": favorite.id,
                "name": character.name,
                "type": "character"
            })

    planet_favorites = PlanetsFavorites.query.filter_by(user=user_id).all()
    for favorite in planet_favorites:
        planet = Planets.query.get(favorite.planet_id)
        if planet:
            favorites_list.append({
                "favorite_id": favorite.id,
                "name": planet.name,
                "type": "planet"
            })

    ship_favorites = ShipsFavorites.query.filter_by(user=user_id).all()
    for favorite in ship_favorites:
        ship = Ships.query.get(favorite.ship_id)
        if ship:
            favorites_list.append({
                "favorite_id": favorite.id,
                "name": ship.name,
                "type": "ship"
            })

    return jsonify(favorites_list), 200

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def addCharacterFavorite(character_id):
    character = Characters.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404

    existing_favorite = CharacterFavorites.query.filter_by(char_id=character_id).first()
    if existing_favorite:
        return jsonify({"error": "Character already a favorite"}), 400

    character_favorite = CharacterFavorites(char_id=character_id)
    db.session.add(character_favorite)
    db.session.commit()

    return jsonify({"message": "Character favorite added successfully"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def addPlanetFavorite(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    existing_favorite = PlanetsFavorites.query.filter_by(planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"error": "Planet already a favorite"}), 400

    planet_favorite = PlanetsFavorites(planet_id=planet_id)
    db.session.add(planet_favorite)
    db.session.commit()

    return jsonify({"message": "Planet favorite added successfully"}), 200

@app.route('/favorite/ship/<int:ship_id>', methods=['POST'])
def addShipFavorite(ship_id):
    ship = Ships.query.get(ship_id)
    if ship is None:
        return jsonify({"error": "Ship not found"}), 404

    existing_favorite = ShipsFavorites.query.filter_by(ship_id=ship_id).first()
    if existing_favorite:
        return jsonify({"error": "Ship already a favorite"}), 400

    ship_favorite = ShipsFavorites(ship_id=ship_id)
    db.session.add(ship_favorite)
    db.session.commit()

    return jsonify({"message": "Ship favorite added successfully"}), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def deletePlanetFavorite(planet_id):
    favorite = PlanetsFavorites.query.filter_by(planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"error": "Planet favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Planet favorite deleted successfully"}), 200


@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def deleteCharacterFavorite(character_id):
    favorite = CharacterFavorites.query.filter_by(char_id=character_id).first()
    if favorite is None:
        return jsonify({"error": "Character favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Character favorite deleted successfully"}), 200


@app.route('/favorite/ship/<int:ship_id>', methods=['DELETE'])
def deleteShipFavorite(ship_id):
    favorite = ShipsFavorites.query.filter_by(ship_id=ship_id).first()
    if favorite is None:
        return jsonify({"error": "Ship favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Ship favorite deleted successfully"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
