from flask import Flask, request, response, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import jwt
import datetime
from functools import wraps
from config import MONGO_URI, SECRET_KEY



app.config['SECRET_KEY'] = SECRET_KEY 

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client.travel_reviews

@app.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = list(db.destinations.find())
    destinations = [convert_id(d) for d in destinations]
    return jsonify(destinations)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"message": "Token is invalid"}), 401
        return f(*args, **kwargs)
    return decorated
