from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('register', methods = ['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email = email).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    user = User(email = email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email = email).first()
    if user and user.check_password(password):
        token =  create_access_token(identity=user.id)
        return jsonify({'token': token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401