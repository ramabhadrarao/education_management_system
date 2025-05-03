# app/infrastructure/repositories/user_repository.py
from app.application.interfaces.repositories import UserRepository
from app.domain.models.user import User
from app import db

class SQLAlchemyUserRepository(UserRepository):
    def create(self, user):
        db.session.add(user)
        db.session.commit()
        return user
    
    def get_by_id(self, user_id):
        return User.query.get(user_id)
    
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()
    
    def get_by_email(self, email):
        return User.query.filter_by(email=email).first()
    
    def update(self, user):
        db.session.commit()
        return user
    
    def delete(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False