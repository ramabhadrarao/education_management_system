# app/interfaces/web/controllers/dashboard_controller.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.domain.models.leave_management import PeriodAdjustment
from app.domain.models.user import User

web_dashboard_bp = Blueprint('web_dashboard', __name__)

@web_dashboard_bp.route('/')
@login_required
def index():
    context = {
        'user': current_user
    }
    
    # Faculty-specific dashboard data
    if current_user.role == 'faculty' and current_user.faculty:
        # Get pending adjustments where this faculty is requested as substitute
        pending_adjustments = PeriodAdjustment.query.filter_by(
            substitute_faculty_id=current_user.faculty.faculty_id,
            status='Pending'
        ).all()
        
        context['pending_adjustments'] = pending_adjustments
    
    # HOD or Admin dashboard data
    if current_user.role in ['admin', 'hod']:
        # For HOD, get faculty count in their department
        if current_user.role == 'hod' and current_user.department_id:
            faculty_count = User.query.filter_by(
                role='faculty',
                department_id=current_user.department_id
            ).count()
            
            student_count = User.query.filter_by(
                role='student',
                department_id=current_user.department_id
            ).count()
        else:  # For admin, get total count
            faculty_count = User.query.filter_by(role='faculty').count()
            student_count = User.query.filter_by(role='student').count()
        
        context['faculty_count'] = faculty_count
        context['student_count'] = student_count
    
    return render_template('dashboard/index.html', **context)