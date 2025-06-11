"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, FavoritePlanet, FavoritePeople, FavoriteVehicle

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

# PEOPLE ENDPOINTS


@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200

# PLANETS ENDPOINTS


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# VEHICLES ENDPOINTS


@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicles.query.all()
    return jsonify([vehicle.serialize() for vehicle in vehicles]), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200

# USERS ENDPOINTS


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_with_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

# FAVORITES PLANET


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # Simulación de usuario actual
    user_id = request.args.get('user_id', default=1, type=int)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    exists = FavoritePlanet.query.filter_by(
        user_id=user.id, planet_id=planet_id).first()
    if exists:
        return jsonify({"msg": "Planet already in favorites"}), 400

    favorite = FavoritePlanet(user_id=user.id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Planet added to favorites"}), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Simulación de usuario actual
    user_id = request.args.get('user_id', default=1, type=int)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    favorite = FavoritePlanet.query.filter_by(
        user_id=user.id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorite planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet deleted"}), 200

# FAVORITES PEOPLE


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    # Simulación de usuario actual
    user_id = request.args.get('user_id', default=1, type=int)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    exists = FavoritePeople.query.filter_by(
        user_id=user.id, people_id=people_id).first()
    if exists:
        return jsonify({"msg": "People already in favorites"}), 400

    favorite = FavoritePeople(user_id=user.id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "People added to favorites"}), 201


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    # Simulación de usuario actual
    user_id = request.args.get('user_id', default=1, type=int)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    favorite = FavoritePeople.query.filter_by(
        user_id=user.id, people_id=people_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorite people not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite people deleted"}), 200

# FAVORITES VEHICLE


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    # Simulación de usuario actual
    user_id = request.args.get('user_id', default=1, type=int)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    exists = FavoriteVehicle.query.filter_by(
        user_id=user.id, vehicle_id=vehicle_id).first()
    if exists:
        return jsonify({"msg": "Vehicle already in favorites"}), 400

    favorite = FavoriteVehicle(user_id=user.id, vehicle_id=vehicle_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Vehicle added to favorites"}), 201


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_id):
    # Simulación de usuario actual
    user_id = request.args.get('user_id', default=1, type=int)
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    favorite = FavoriteVehicle.query.filter_by(
        user_id=user.id, vehicle_id=vehicle_id).first()
    if favorite is None:
        return jsonify({"msg": "Favorite vehicle not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite vehicle deleted"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
