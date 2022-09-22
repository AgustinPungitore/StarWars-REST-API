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
from models import db, User
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/planets', methods=['GET'])

def get_planets():

    planets=Planets.query.all()

    results= list(map(lambda item: item.serialize(),planets))
    response_body = {
        "msg": "Todo bien",
        "results": results
    }

    return jsonify(results), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])

def get_one_planet(planet_id):
    planet=Planets.query.filter_by(id=planet_id).first()

    print(planet.serialize)
    response_body = {
        "msg": "Todo bien",
        "results": results
    }

    return jsonify(results), 200



@app.route('/people', methods=['GET'])

def get_people():

    people=People.query.all()

    results= list(map(lambda item: item.serialize(),people))
    response_body = {
        "msg": "Todo bien",
        "results": results
    }

    return jsonify(results), 200


@app.route('/people/<int:people_id>', methods=['GET'])

def get_one_people(people_id):
    planet=People.query.filter_by(id=people_id).first()

    print(people.serialize)
    response_body = {
        "msg": "Todo bien",
        "results": results
    }

    return jsonify(results), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])

def post_one_people(people_id):
    body = request.get_json()
    post_people = People(id=body["id"], name=body["name"], description=body["description"])
    db.session.add(post_people)
    db.session.commit
    
    response_body = {
        "msg": "Se ha guardado el personaje",
        "results": post_people.serialize()
    }

    return jsonify(response_body), 200



@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])

def delete_one_people(people_id):
    delete_people = People.query.get(people_id)
    db.session.delete(delete_people)
    db.session.commit()
 
#if user1 is None:
   # raise APIException('User not found', status_code=404)

    response_body = {
        "msg": "Se ha eliminado el personaje",
        "results": delete_people.serialize()
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
