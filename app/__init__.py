# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.interfaces.api.routes import auth_bp, user_bp, faculty_bp, student_bp
    from app.interfaces.web.controllers import web_auth_bp, web_dashboard_bp, web_faculty_bp, web_student_bp
    
    # API routes
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(faculty_bp, url_prefix='/api/faculty')
    app.register_blueprint(student_bp, url_prefix='/api/students')
    
    # Web routes
    app.register_blueprint(web_auth_bp, url_prefix='/auth')
    app.register_blueprint(web_dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(web_faculty_bp, url_prefix='/faculty')
    app.register_blueprint(web_student_bp, url_prefix='/students')

    return app