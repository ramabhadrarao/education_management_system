# app/interfaces/web/controllers/user_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.domain.models.user import User
from app.domain.models.faculty import Faculty
from app.domain.models.student import Student
from app.domain.models.department import Department
from app import db
from werkzeug.security import generate_password_hash

web_user_bp = Blueprint('web_user', __name__)

@web_user_bp.route('/')
@login_required
def user_list():
    if current_user.role not in ['admin', 'hod']:
        flash('Access denied', 'danger')
        return redirect(url_for('web_dashboard.index'))
    
    # Get query parameters for filtering
    role = request.args.get('role', 'all')
    department_id = request.args.get('department_id', type=int)
    
    # Build query based on filters
    query = User.query
    
    if role != 'all':
        query = query.filter_by(role=role)
    
    if department_id:
        query = query.filter_by(department_id=department_id)
    elif current_user.role == 'hod' and current_user.department_id:
        # HODs can only see users in their department
        query = query.filter_by(department_id=current_user.department_id)
    
    users = query.all()
    departments = Department.query.all()
    
    return render_template('user/list.html', users=users, departments=departments, current_role=role)

@web_user_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.role not in ['admin', 'hod']:
        flash('Access denied', 'danger')
        return redirect(url_for('web_dashboard.index'))
    
    departments = Department.query.all()
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        department_id = request.form.get('department_id', type=int)
        
        # Validate if the user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return render_template('user/create.html', departments=departments)
        
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email already exists', 'danger')
            return render_template('user/create.html', departments=departments)
        
        # HODs can only create users in their department
        if current_user.role == 'hod' and department_id != current_user.department_id:
            flash('You can only create users in your department', 'danger')
            return render_template('user/create.html', departments=departments)
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            role=role,
            department_id=department_id
        )
        new_user.password_hash = generate_password_hash(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('User created successfully', 'success')
        return redirect(url_for('web_user.user_list'))
    
    return render_template('user/create.html', departments=departments)

@web_user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role not in ['admin', 'hod']:
        flash('Access denied', 'danger')
        return redirect(url_for('web_dashboard.index'))
    
    user = User.query.get_or_404(user_id)
    
    # HODs can only edit users in their department
    if current_user.role == 'hod' and user.department_id != current_user.department_id:
        flash('Access denied', 'danger')
        return redirect(url_for('web_user.user_list'))
    
    departments = Department.query.all()
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_active = 'is_active' in request.form
        department_id = request.form.get('department_id', type=int)
        
        # Validate if the username is taken by another user
        existing_user = User.query.filter(User.username == username, User.user_id != user_id).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return render_template('user/edit.html', user=user, departments=departments)
        
        # Validate if the email is taken by another user
        existing_email = User.query.filter(User.email == email, User.user_id != user_id).first()
        if existing_email:
            flash('Email already exists', 'danger')
            return render_template('user/edit.html', user=user, departments=departments)
        
        # HODs can only assign users to their department
        if current_user.role == 'hod' and department_id != current_user.department_id:
            flash('You can only assign users to your department', 'danger')
            return render_template('user/edit.html', user=user, departments=departments)
        
        # Update user
        user.username = username
        user.email = email
        user.is_active = is_active
        user.department_id = department_id
        
        if password:
            user.password_hash = generate_password_hash(password)
        
        db.session.commit()
        
        flash('User updated successfully', 'success')
        return redirect(url_for('web_user.user_list'))
    
    return render_template('user/edit.html', user=user, departments=departments)

@web_user_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('web_user.user_list'))
    
    user = User.query.get_or_404(user_id)
    
    if user.user_id == current_user.user_id:
        flash('You cannot delete your own account', 'danger')
        return redirect(url_for('web_user.user_list'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully', 'success')
    return redirect(url_for('web_user.user_list'))