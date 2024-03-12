from flask import Blueprint, jsonify


main = Blueprint('index', __name__)


@main.get('api/data')
def index():
    return jsonify({"message": "Hello world"})