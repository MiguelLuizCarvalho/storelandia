import token

from flask import Blueprint, render_template, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import re

from . import db
from .models import User

auth_bp = Blueprint('auth', __name__)
CORS(app=auth_bp)

SECRET_KEY = "5a82596bde152386cdc97fc3735256407e6c4260102761ff"

def is_valid_email(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email)

@auth_bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not is_valid_email(email):
        return jsonify({'message': 'Formato de e-mail inválido!'}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'message': 'Usuário ou email já cadastrados!'}), 400

    new_user = User(
        username=username,
        email=email,
        password=password,
        role=data.get('role', 'user')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201

@auth_bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    login_input = data.get('login') 
    password = data.get('password')

    user = User.query.filter((User.username == login_input) | (User.email == login_input)).first()

    if user and user.password == password:
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'token': token, 
        'role': user.role, # sending the user role to frontend in login.js
        'message': f'Bem-vindo, {user.username}!'
    }), 200

@auth_bp.route('/logout/', methods=['POST'])
def logout():
    if request.method == 'POST':
        return jsonify({'message': 'Logout successful!'}), 200
    
    db.session.commit()