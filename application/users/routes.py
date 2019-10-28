from flask import Blueprint, jsonify, request

from . import db
from .models import User

UserAPI = Blueprint('user_api', __name__)


@UserAPI.route('/create', methods=['POST'])
def create_user():
    """API request to Create a new User"""

    try:
        user = User.from_user(request.json)
    except KeyError as e:
        return jsonify(f'Missing key: {e.args[0]}'), 400

    db.session.add(user)
    db.session.commit()
    return jsonify(), 200


@UserAPI.route('/<int:UserID>')
def get_user_byid(UserID):
    """API request to Get a User by ID"""

    user = User.query.filter(User.UserID == UserID).first()
    if user is None:
        return 'User not found', 404
    return jsonify(user.to_user()), 200


@UserAPI.route('/<string:username>')
def get_user_byusername(UserID):
    """API request to Get a User by username"""

    user = User.query.filter(User.username == username).first()
    if user is None:
        return 'User not found', 404
    return jsonify(user.to_user()), 200


@UserAPI.route('/', methods=['GET'])
def get_all():
    user = User.query.all()
    jsonuser = [usr.to_dict() for usr in User]
    return jsonify(jsonuser), 200


@UserAPI.route('<int:UserID>', methods=['PUT'])
def edit_user(UserID):

    User.query.filter(User.UserID == UserID).update(request.json)
    user = User.query.filter(User.UserID == UserID).first_or_404()
    db.session.commit()
    return jsonify(User.to_user()), 200

@TodoAPI.route('/<int:UserID>', methods=['DELETE'])
def delete_user(UserID):

    user = User.query.filter(User.UserID == UserID).first()
    if user is None:
        return 'User not found', 404

    db.session.delete(user)
    db.session.commit()
    return jsonify(), 200
