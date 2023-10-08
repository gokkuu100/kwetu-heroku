import os
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, House, Agent, User
from flask_jwt_extended import JWTManager, jwt_required
import jwt
from functools import wraps
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import redis
from flask import make_response

redis_store = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///housing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '\xaa\x8eJ\x81[\x15\x1bPM\xa7n\xdaZ\x90=\xe3\xf3\x9d\xbaW\x11\xb4\x8b\x94\x95\xe1\xff\x1d^\xa7\x04rc\x8a\x99\xe38\x0e,?=\xf0\xdbm\xa4\xfb\xc1'
app.config['REDIS_URL'] = "redis://localhost:6379/0"

jwt = JWTManager(app)
app.json.compact = False
CORS(app, supports_credentials=True)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


@app.route('/houses', methods=['POST'])
@jwt_required()
@role_required('agent')
def create_house():
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    bedrooms = data.get('bedrooms')
    bathrooms = data.get('bathrooms')
    city = data.get('city')
    image_paths = data.get('image_paths')
    agent_id = data.get('agent_id')
    size = data.get('size')
    county = data.get('county')

    new_house = House(
        title=title,
        description=description,
        price=price,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        city=city,
        agent_id=agent_id,
        image_paths=image_paths,
        size=size,
        county=county
    )

    db.session.add(new_house)
    db.session.commit()

    house_data = {
        'id': new_house.id,
        'title': new_house.title,
        'description': new_house.description,
        'price': new_house.price,
        'bedrooms': new_house.bedrooms,
        'bathrooms': new_house.bathrooms,
        'city': new_house.city,
        'agent_id': new_house.agent_id,
        'image_paths': new_house.image_paths,
        'size': new_house.size,
        "county": new_house.county
    }

    return make_response(jsonify(house_data), 201)

@app.route('/houses/<int:id>', methods=['GET'])
def get_house_by_id(id):
    house = House.query.filter_by(id=id).first()

    if not house:
        return jsonify({"error": "House not found"}), 404

    house_data = {
        'id': house.id,
        'title': house.title,
        'description': house.description,
        'price': house.price,
        'bedrooms': house.bedrooms,
        'bathrooms': house.bathrooms,
        'city': house.city,
        'agent_id': house.agent_id,
        'image_paths': house.image_paths,
        'size': house.size,
        "county": house.county
    }
    return make_response(jsonify(house_data), 200)

@app.route('/houses/<int:id>', methods=['PATCH'])
@jwt_required()
@role_required('agent')
def update_house(id):
    house = House.query.filter_by(id=id).first()

    if not house:
        return jsonify({"error": "House not found"}), 404

    data = request.get_json()

    house.title = data.get('title', house.title)
    house.description = data.get('description', house.description)
    house.price = data.get('price', house.price)
    house.bedrooms = data.get('bedrooms', house.bedrooms)
    house.bathrooms = data.get('bathrooms', house.bathrooms)
    house.city = data.get('city', house.city)
    house.agent_id = data.get('agent_id', house.agent_id)
    house.image_paths = data.get('image_paths', house.image_paths)
    house.size = data.get('size', house.size)
    house.county = data.get('county', house.county)

    db.session.commit()
    return make_response(jsonify({"message": "House updated successfully"}), 200)

@app.route('/houses/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('agent')
def delete_house(id):
    house = House.query.filter_by(id=id).first()

    if not house:
        return jsonify({"error": "House not found"}), 404

    db.session.delete(house)
    db.session.commit()
    return make_response(jsonify({"message": "House deleted successfully"}), 200)
@app.route('/agents', methods=['GET'])
def get_agents():
    all_agents = Agent.query.all()
    agent_list = []
    for agent in all_agents:
        agent_data = {
            'id': agent.id,
            'name': agent.name,
            'email': agent.email,
            'phonebook': agent.phonebook
        }
        agent_list.append(agent_data)
    return make_response(jsonify(agent_list), 200)

@app.route('/agents/<int:agent_id>', methods=['GET'])
def get_agent_by_id(agent_id):
    agent = Agent.query.get(agent_id)

    if agent is None:
        return jsonify({"error": "Agent not found"}), 400

    response_data = {
        'id': agent.id,
        'name': agent.name,
        'email': agent.email,
        'phonebook': agent.phonebook,
    }

    return make_response(jsonify(response_data), 200)