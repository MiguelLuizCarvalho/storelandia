from flask import Blueprint, json, render_template, request, jsonify
from flask_cors import CORS
import jwt
import datetime
import os
import re

from app.routes import USERS_FILE

auth_bp = Blueprint('auth', __name__)
CORS(app=auth_bp)

SECRET_KEY = "5a82596bde152386cdc97fc3735256407e6c4260102761ff"

USERS_FILE = os.path.join(os.getcwd(), 'user.json')
PRODUCTS_FILE = os.path.join(os.getcwd(), 'products.json')

def is_valid_email(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email)

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as u:
        return json.load(u)
    
def save_users(users_to_save):
    with open(USERS_FILE, 'w') as u:
        json.dump(users_to_save, u, indent=4)
    
@auth_bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')

    users = load_users()
    if any(u['username'] == username or u['email'] == email for u in users):
        return jsonify({'message': 'Usuário ou email já cadastrados!'}), 400

    new_user = {
        'id': len(users) + 1,
        'username': username,
        'email': email,
        'password': password,
        'role': role
    }
    users.append(new_user)

    if not is_valid_email(email):
        return jsonify({'message': 'Formato de e-mail inválido!'}), 400

    save_users(users)

    return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201

 
@auth_bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    login_input = data.get('login') 
    password = data.get('password')

    users = load_users()
    
    user = next((u for u in users if (u['username'] == login_input or u['email'] == login_input) and u['password'] == password), None)

    if user:
        payload = {
            'user_id': user['id'],
            'username': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token, 'message': f'Bem-vindo, {user["username"]}!'}), 200

    return jsonify({'message': 'Dados incorretos!'}), 401