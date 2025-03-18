from flask import Blueprint, request, jsonify
import os
from schemas.user_schemas import UserCreate, UserResponse, UserDelete
from models.entities.User import User
from werkzeug.security import generate_password_hash,  check_password_hash
from pydantic import ValidationError
from db_config import db
import jwt
import datetime
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

user_routes = Blueprint('user_routes', __name__, url_prefix='/users')

def generate_token(user_id):
    payload = {
        'user_id': user_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


@user_routes.route('/register', methods=['POST'])

def register_user():
    try:
        user = UserCreate(**request.json)

    except ValidationError as e:
        return jsonify(e.errors()), 400

    existing_user = User.query.filter_by(email=user.email).first()
    if existing_user:
        return jsonify({"error": "Usuario ya registrado"}), 400
    
    hased_password = generate_password_hash(user.password)
    user = User(
        name = user.name,
        email = user.email,
        password = hased_password,
        token=None
    )

    try:
        db.session.add(user)
        db.session.commit()

        token = generate_token(user.id)
        user.token = token
        db.session.commit()

        return jsonify({
            "message": "Usuario registrado correctamente",
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "token": user.token,
            "created_at": user.created_at,
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error al registrar usuario: {e}")
        return jsonify({"error": "Error al registrar usuario"}), 500

@user_routes.route('/all-user', methods=['GET'])
def all_users():
    users = User.query.all()
    result = [UserResponse.from_orm(user) for user in users]
    return jsonify([user.dict() for user in result])   

@user_routes.route('/find-user/<int:user_id>', methods=['GET'])
def find_user(user_id):

    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    try:
        user_data = UserResponse.model_validate(user)
        return jsonify(user_data.model_dump())
    except ValidationError as e:
        print(f"Error al validar datos de la empresa: {e}")
        return jsonify({"error": "Error al validar datos de la empresa"}), 500
    

@user_routes.route('/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    if 'name' in data:
        user.name = data['name']
    
    if 'email' in data:
        user.email = data['email']
    
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    
    if 'created_at' in data:
        user.created_at = data['created_at']

    if 'updated_at' in data:
        user.updated_at = data['updated_at']

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuario actualizada correctamente", "updated_fields":{key: data[key] for key in data if key in ["name", "email", "password", "created_at", "updated_at"]}})
    except Exception as e:
        db.session.rollback()
        print(f"Error al actualizar usuario: {e}")
        return jsonify({"error": "Error al actualizar usuario"}), 400

@user_routes.route('/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id): 
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    user_id_delete = user.id

    try:
        db.session.delete(user)
        db.session.commit()
        
        response = UserDelete(
            message="Usuario eliminado correctamente", 
            delete_user_id=user_id_delete
        )
        return jsonify(response.model_dump()),200
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar usuario: {e}")
        return jsonify({"error": "Error al eliminar usuario"}), 400
    
