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