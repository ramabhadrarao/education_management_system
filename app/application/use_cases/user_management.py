# app/application/use_cases/user_management.py
from app.domain.models.user import User

class UserManagementUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository
    
    def register_user(self, username, email, password, role, department_id=None):
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError("Username already exists")
        
        existing_email = self.user_repository.get_by_email(email)
        if existing_email:
            raise ValueError("Email already exists")
        
        user = User(username=username, email=email, role=role, department_id=department_id)
        user.set_password(password)
        
        return self.user_repository.create(user)
    
    def authenticate_user(self, username, password):
        user = self.user_repository.get_by_username(username)
        
        if not user or not user.check_password(password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def get_user(self, user_id):
        return self.user_repository.get_by_id(user_id)
    
    def update_user(self, user_id, **kwargs):
        user = self.user_repository.get_by_id(user_id)
        
        if not user:
            raise ValueError("User not found")
        
        for key, value in kwargs.items():
            if key == 'password':
                user.set_password(value)
            elif hasattr(user, key):
                setattr(user, key, value)
        
        return self.user_repository.update(user)
    
    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)

# Similar use cases for faculty, student, leave management, etc.