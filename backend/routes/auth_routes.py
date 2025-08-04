from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from extensions import mysql
from utils.email_service import send_email

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user:
        return jsonify({'error': 'User already exists'}), 409

    hashed_pw = generate_password_hash(password)
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                   (name, email, hashed_pw))
    mysql.connection.commit()
    cursor.close()

    send_email(email, name, is_todo=False)

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not check_password_hash(user[3], password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user[0]), expires_delta=datetime.timedelta(days=1))

    return jsonify({
        'token': access_token,
        'user': {'id': user[0], 'name': user[1], 'email': user[2]}
    })

@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    data = request.json
    email = data.get('email')
    name = data.get('name')

    if not email or not name:
        return jsonify({'error': 'Email and name are required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, '')
        )
        mysql.connection.commit()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        send_email(email, name, is_todo=False)

    cursor.close()

    access_token = create_access_token(identity=str(user[0]), expires_delta=datetime.timedelta(days=1))
    return jsonify({
        'token': access_token,
        'user': {'id': user[0], 'name': user[1], 'email': user[2]}
    })
