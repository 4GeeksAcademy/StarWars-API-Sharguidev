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
from models import db, People, Planets, Favorites, Fans
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


# tomar todos los personajes de la base de datos
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people_list = [person.serialize() for person in people]
    return jsonify(people_list), 200

# tomar un personaje por id
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    people = People.query.get(people_id)
    if people is None:
        raise APIException('People not found', status_code=404)
    return jsonify(people.serialize()), 200

# tomar todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    planets_list = [planet.serialize() for planet in planets]
    return jsonify(planets_list), 200

# tomar un planeta por id
@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets_by_id(planets_id):
    planets = Planets.query.get(planets_id)
    if planets is None:
        raise APIException('Planets not found', status_code=404)
    return jsonify(planets.serialize()), 200

# # tomar todos los usuarios
@app.route('/fans', methods=['GET'])
def get_users():
    fans = Fans.query.all()
    user = list(map(lambda x: x.serialize(), fans))
    return jsonify(user), 200

# tomar los favoritos de un usuario
@app.route('/fans/<int:fan_id>/favorites', methods=['GET'])
def get_users_fav_by_id(fan_id):
    favorites = Favorites.query.filter_by(fan_id=fan_id).all()
    favorites_list = [favorite.serialize() for favorite in favorites]
    return jsonify(favorites_list), 200

# añadir favoritos a un usuario especifico
@app.route('/fans/<int:fan_id>/favorites/planet/<int:planets_id>', methods=['POST'])
def add_fav_planet(fan_id, planets_id):
    planet = Planets.query.get(planets_id)
    fan = Fans.query.get(fan_id)
    if planet is None and fan is None:
        raise APIException('Planet or fan not found', status_code=404)
    favorite = Favorites(fan_id=fan_id, planets_id=planets_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 200

# añadir un personaje favorito a un usuario
@app.route('/fans/<int:fan_id>/favorites/people/<int:people_id>', methods=['POST'])
def add_fav_people(fan_id, people_id):
    people = People.query.get(people_id)
    if people is None:  
        raise APIException('Cannot find people', status_code=404)
    favorite_people = Favorites(fan_id=fan_id, people_id=people_id)
    db.session.add(favorite_people)
    db.session.commit()
    return jsonify(favorite_people.serialize()), 200

#borrar un planeta favorito
@app.route('/fans/<int:fan_id>/favorites/planet/<int:planets_id>', methods=['DELETE'])
def delete_fav_planet(fan_id, planets_id):
    favorite_planet = Favorites.query.filter_by(fan_id=fan_id, planets_id=planets_id).first()
    if favorite_planet is None:
        raise APIException('Planet not found', status_code=404)
    db.session.delete(favorite_planet)
    db.session.commit()
    return jsonify(favorite_planet.serialize()), 200

#borrar un personaje favorito
@app.route('/fans/<int:fan_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(fan_id, people_id):
    favorite_people = Favorites.query.filter_by(fan_id=fan_id, people_id=people_id).first()
    if favorite_people is None:
        raise APIException('People not found', status_code=404)
    db.session.delete(favorite_people)
    db.session.commit()
    return jsonify(favorite_people.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
