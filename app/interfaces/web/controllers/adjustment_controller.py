# app/interfaces/web/controllers/adjustment_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.application.use_cases.leave_management import LeaveManagementUseCase
from app.infrastructure.repositories.leave_repository import SQLAlchemyLeaveRepository
from app.infrastructure.repositories.faculty_repository import SQLAlchemyFacultyRepository
from app.domain.models.faculty import Faculty
from app.domain.models.course import Course
from app.domain.models.batch import Batch
from datetime import datetime

web_adjustment_bp = Blueprint('web_adjustment', __name__)
leave_repository = SQLAlchemyLeaveRepository()
faculty_repository = SQLAlchemyFacultyRepository()
leave_use_case = LeaveManagementUseCase(leave_repository, faculty_repository)

@web_adjustment_bp.route('/request/<int:leave_id>', methods=['GET', 'POST'])
@login_required
def request_adjustment(leave_id):
    if current_user.role != 'faculty' or not current_user.faculty:
        flash('Access denied', 'danger')
        return redirect(url_for('web_dashboard.index'))
    
    leave = leave_repository.get_leave_by_id(leave_id)
    
    if not leave or leave.faculty_id != current_user.faculty.faculty_id:
        flash('Leave request not found', 'danger')
        return redirect(url_for('web_leave.leave_list'))
    
    # Get faculties, courses, and batches for the form
    faculties = Faculty.query.filter(Faculty.faculty_id != current_user.faculty.faculty_id).all()
    courses = Course.query.all()
    batches = Batch.query.all()
    
    if request.method == 'POST':
        substitute_faculty_id = request.form.get('substitute_faculty_id', type=int)
        course_id = request.form.get('course_id', type=int)
        batch_id = request.form.get('batch_id', type=int)
        adjustment_date = request.form.get('adjustment_date')
        period_number = request.form.get('period_number', type=int)
        
        try:
            adjustment_date = datetime.strptime(adjustment_date, '%Y-%m-%d').date()
            
            adjustment = leave_use_case.create_period_adjustment(
                leave_id=leave_id,
                faculty_id=current_user.faculty.faculty_id,
                substitute_faculty_id=substitute_faculty_id,
                course_id=course_id,
                batch_id=batch_id,
                adjustment_date=adjustment_date,
                period_number=period_number
            )
            
            flash('Period adjustment request submitted successfully', 'success')
            return redirect(url_for('web_leave.leave_list'))
        
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('adjustment/request.html', leave=leave, faculties=faculties, courses=courses, batches=batches)

@web_adjustment_bp.route('/respond/<int:adjustment_id>', methods=['GET', 'POST'])
@login_required
def respond_adjustment(adjustment_id):
    adjustment = leave_repository.get_adjustment_by_id(adjustment_id)
    
    if not adjustment or (current_user.role == 'faculty' and current_user.faculty and adjustment.substitute_faculty_id != current_user.faculty.faculty_id):
        flash('Adjustment request not found', 'danger')
        return redirect(url_for('web_dashboard.index'))
    
    if adjustment.status != 'Pending':
        flash('Adjustment request already processed', 'warning')
        return redirect(url_for('web_dashboard.index'))
    
    if request.method == 'POST':
        status = request.form.get('status')
        
        if status not in ['Accepted', 'Rejected']:
            flash('Invalid status', 'danger')
            return render_template('adjustment/respond.html', adjustment=adjustment)
        
        try:
            adjustment = leave_use_case.respond_to_adjustment(
                adjustment_id=adjustment_id,
                status=status
            )
            
            flash(f'Adjustment request {status.lower()} successfully', 'success')
            return redirect(url_for('web_dashboard.index'))
        
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('adjustment/respond.html', adjustment=adjustment)