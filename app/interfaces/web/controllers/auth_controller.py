# app/interfaces/web/controllers/auth_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.application.use_cases.user_management import UserManagementUseCase
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository

web_auth_bp = Blueprint('web_auth', __name__)
user_repository = SQLAlchemyUserRepository()
user_use_case = UserManagementUseCase(user_repository)

@web_auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('web_dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password', 'danger')
            return render_template('auth/login.html')
        
        user = user_use_case.authenticate_user(username, password)
        
        if not user:
            flash('Invalid credentials', 'danger')
            return render_template('auth/login.html')
        
        login_user(user)
        next_page = request.args.get('next')
        
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('web_dashboard.index')
        
        return redirect(next_page)
    
    return render_template('auth/login.html')

@web_auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web_auth.login'))

@web_auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('web_dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('Please fill in all fields', 'danger')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/register.html')
        
        try:
            user = user_use_case.register_user(
                username=username,
                email=email,
                password=password,
                role='student'  # Default role for self-registration
            )
            
            flash('Registration successful! Please wait for approval.', 'success')
            return redirect(url_for('web_auth.login'))
        
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')