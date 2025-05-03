# app/infrastructure/auth/permissions.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify, request, g
from app.domain.models.user import User

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify(message="User not found"), 404
            
            if user.role not in roles:
                return jsonify(message="Insufficient permissions"), 403
            
            g.current_user = user
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# ABAC implementation
class Permission:
    def __init__(self, action, resource, conditions=None):
        self.action = action
        self.resource = resource
        self.conditions = conditions or {}
    
    def check(self, user):
        # This is a simplified ABAC implementation
        # In a real-world scenario, you would have more complex rules
        
        # Check role-based permissions first
        if user.role == 'admin':
            return True
        
        if user.role == 'hod' and self.resource in ['faculty', 'student', 'course', 'leave']:
            if self.action in ['view', 'approve']:
                return True
            if self.action in ['create', 'update', 'delete'] and self.resource != 'leave':
                return True
        
        if user.role == 'faculty':
            if self.resource == 'faculty' and hasattr(self, 'faculty_id'):
                # Faculty can manage their own data
                if user.faculty and user.faculty.faculty_id == self.faculty_id:
                    if self.action in ['view', 'update']:
                        return user.faculty.edit_enabled
            
            if self.resource == 'leave' and self.action in ['create', 'view']:
                return True
        
        if user.role == 'student':
            if self.resource == 'student' and hasattr(self, 'student_id'):
                # Students can manage their own data
                if user.student and user.student.student_id == self.student_id:
                    if self.action in ['view', 'update']:
                        return user.student.edit_enabled
        
        return False

def permission_required(action, resource):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify(message="User not found"), 404
            
            permission = Permission(action, resource)
            
            # Add resource-specific conditions
            for key, value in kwargs.items():
                setattr(permission, key, value)
            
            if not permission.check(user):
                return jsonify(message="Permission denied"), 403
            
            g.current_user = user
            return fn(*args, **kwargs)
        return decorator
    return wrapper