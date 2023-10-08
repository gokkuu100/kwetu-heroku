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

