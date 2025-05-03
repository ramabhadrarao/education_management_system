# app/interfaces/api/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.application.use_cases.user_management import UserManagementUseCase
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository

auth_bp = Blueprint('auth', __name__)
user_repository = SQLAlchemyUserRepository()
user_use_case = UserManagementUseCase(user_repository)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify(message="Missing username or password"), 400
    
    user = user_use_case.authenticate_user(data['username'], data['password'])
    
    if not user:
        return jsonify(message="Invalid credentials"), 401
    
    access_token = create_access_token(identity=user.user_id)
    
    return jsonify(
        access_token=access_token,
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        role=user.role
    ), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify(message="Missing required fields"), 400
    
    try:
        user = user_use_case.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data['role'],
            department_id=data.get('department_id')
        )
        
        return jsonify(
            message="User registered successfully",
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role
        ), 201
    
    except ValueError as e:
        return jsonify(message=str(e)), 400

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = user_use_case.get_user(current_user_id)
    
    if not user:
        return jsonify(message="User not found"), 404
    
    return jsonify(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        role=user.role,
        department_id=user.department_id,
        is_active=user.is_active
    ), 200