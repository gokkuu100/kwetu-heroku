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


# Token Blacklisting
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return redis_store.get(jti) is not None

# Authorization Middleware
def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] == required_role:
                return fn(*args, **kwargs)
            else:
                return jsonify(message='Unauthorized'), 403
        return wrapper
    return decorator

@app.route('/houses', methods=['GET'])
def get_houses():
    houses = House.query.all()
    house_list = []
    for house in houses:
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
        house_list.append(house_data)
    return make_response(jsonify(house_list), 200)

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

# @app.route('/agents/<int:agent_id>/dashboard', methods=['GET'])
# @jwt_required()
# def get_agent_dashboard(agent_id):
#     current_user = get_jwt_identity()
#     if current_user['role'] == 'agent':
#         # Get agent details based on the current user's username (assuming it's unique)
#         agent = Agent.query.filter_by(username=current_user['username']).first()
#         if agent:
#             agent_data = {
#                 'id': agent.id,
#                 'name': agent.name,
#                 'email': agent.email,
#                 'phonebook': agent.phonebook
#             }
#             return make_response(jsonify(agent_data), 200)
#         else:
#             return jsonify({"error": "Agent not found"}), 404
#     else:
#         return jsonify(message='Unauthorized'), 403


@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    user_list = []
    for user in all_users:
        user_data = {
            'id': user.id,
            'email;': user.email
        }
        user_list.append(user_data)
    return make_response(jsonify(user_list), 200)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    response_data = {
        'id': user.id,
        'email': user.email
    }

    return make_response(jsonify(response_data), 200)

@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    password = data.get('password')
    email = data.get('email')

    # Validate email and password
    if not email or not password:
        return jsonify({"error": "Invalid email or password"}), 400

    # Check if the email already exists in the database
    existing_user = User.query.filter_by(email=email).first()
    existing_agent = Agent.query.filter_by(email=email).first()
    if existing_user or existing_agent:
        return jsonify({"error": "Email already exists"}), 400

    # Create a new user
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

# /login route
@app.route('/login', methods=['POST', 'OPTIONS'])
def sign_in():
    if request.method == 'OPTIONS':
        # Respond to preflight requests
        response = make_response()
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate email and password
    if not email or not password:
        return jsonify({"error": "Invalid email or password"}), 401

    # Check if the email exists in the database
    user = User.query.filter_by(email=email).first()
    agent = Agent.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # User authenticated successfully, generate JWT token with role=user
        access_token = create_access_token(identity={'email': email, 'role': 'user', 'user_id': user.id})
        response_data = {
            'success': True,
            'role': 'user',
            'id': user.id,
            'access_token': access_token
        }
        response = make_response(jsonify(response_data))
        response.set_cookie('access_token', access_token)
        return response, 200

    elif agent and agent.check_password(password):
        # Agent authenticated successfully, generate JWT token with role=agent
        access_token = create_access_token(identity={'email': email, 'role': 'agent', 'agent_id': agent.id})
        response_data = {
            'success': True,
            'role': 'agent',
            'id': agent.id,
            'access_token': access_token
        }
        response = make_response(jsonify(response_data))
        response.set_cookie('access_token', access_token)
        return response, 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt_identity()['jti']
    # Add the token's JTI (JWT ID) to the blacklist
    redis_store.set(jti, 'true', ex=3600)  # Token will be blacklisted for 1 hour
    return jsonify(message='Logged out successfully'), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def restricted_resource():
    current_user = get_jwt_identity()
    if current_user['role'] == 'agent':
        # Logic for agent role
        pass
    elif current_user['role'] == 'user':
        # Logic for user role
        pass
    else:
        # Invalid role
        return jsonify(message='Unauthorized'), 403


if __name__ == "__main__":
    app.run(port=5555)
