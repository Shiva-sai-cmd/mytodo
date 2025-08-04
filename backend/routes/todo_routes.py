from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql
from utils.email_service import send_email 
from utils.user_helpers import get_user_email_username

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/test', methods=['GET'])
def test_todo():
    return {'message': 'Todo route working!'}

@todo_bp.route('/create', methods=['POST'])
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO todos (user_id, title, description) VALUES (%s, %s, %s)",
        (user_id, title, description)
    )
    mysql.connection.commit()

    name, email = get_user_email_username(user_id)
    cursor.close()

    if email and name:
        send_email(to_email=email, username=name, is_todo=True, todo_title=title)

    return jsonify({'message': 'Todo created and email sent!'}), 201

@todo_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_todos():
    user_id = get_jwt_identity()

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, title, description, completed, created_at FROM todos WHERE user_id = %s", (user_id,))
    todos = cursor.fetchall()
    cursor.close()

    result = [{
        'id': row[0],
        'title': row[1],
        'description': row[2],
        'completed': bool(row[3]),
        'created_at': row[4].strftime("%Y-%m-%d %H:%M:%S")
    } for row in todos]

    return jsonify({'todos': result}), 200

@todo_bp.route('/update/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed', False)

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE todos SET title=%s, description=%s, completed=%s WHERE id=%s AND user_id=%s",
        (title, description, completed, todo_id, user_id)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Todo updated successfully'}), 200

@todo_bp.route('/delete/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    user_id = get_jwt_identity()

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM todos WHERE id=%s AND user_id=%s", (todo_id, user_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Todo deleted successfully'}), 200
