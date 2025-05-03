# app/interfaces/web/controllers/leave_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.application.use_cases.leave_management import LeaveManagementUseCase
from app.infrastructure.repositories.leave_repository import SQLAlchemyLeaveRepository
from app.infrastructure.repositories.faculty_repository import SQLAlchemyFacultyRepository
from app.domain.models.leave_management import LeaveType
from datetime import datetime

web_leave_bp = Blueprint('web_leave', __name__)
leave_repository = SQLAlchemyLeaveRepository()
faculty_repository = SQLAlchemyFacultyRepository()
leave_use_case = LeaveManagementUseCase(leave_repository, faculty_repository)

@web_leave_bp.route('/')
@login_required
def leave_list():
    if current_user.role not in ['admin', 'hod', 'faculty']:
        flash('Access denied', 'danger')
        return redirect(url_for('web_dashboard.index'))
    
    if current_user.role == 'faculty' and current_user.faculty:
        leaves = leave_use_case.get_faculty_leaves(current_user.faculty.faculty_id)
    elif current_user.role in ['admin', 'hod']:
        department_id = request.args.get('department_id', type=int)
        leaves = leave_use_case.get_pending_leaves(department_id)
    else:
        leaves = []
    
    return render_template('leave/list.html', leaves=leaves)

@web_leave_bp.route('/apply', methods=['GET', 'POST'])
@login_required
def apply_leave():
    if current_user.role != 'faculty' or not current_user.faculty:
        flash('Access denied', 'danger')
        return redirect(url_for('web_dashboard.index'))
    
    leave_types = LeaveType.query.all()
    
    if request.method == 'POST':
        leave_type_id = request.form.get('leave_type_id', type=int)
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        reason = request.form.get('reason')
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            leave = leave_use_case.apply_leave(
                faculty_id=current_user.faculty.faculty_id,
                leave_type_id=leave_type_id,
                start_date=start_date,
                end_date=end_date,
                reason=reason
            )
            
            flash('Leave application submitted successfully', 'success')
            return redirect(url_for('web_leave.leave_list'))
        
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('leave/apply.html', leave_types=leave_types)

@web_leave_bp.route('/approve/<int:leave_id>', methods=['GET', 'POST'])
@login_required
def approve_leave(leave_id):
    if current_user.role not in ['admin', 'hod']:
        flash('Access denied', 'danger')
        return redirect(url_for('web_dashboard.index'))
    
    leave = leave_repository.get_leave_by_id(leave_id)
    
    if not leave:
        flash('Leave request not found', 'danger')
        return redirect(url_for('web_leave.leave_list'))
    
    if leave.status != 'Pending':
        flash('Leave request already processed', 'warning')
        return redirect(url_for('web_leave.leave_list'))
    
    if request.method == 'POST':
        status = request.form.get('status')
        
        if status not in ['Approved', 'Rejected']:
            flash('Invalid status', 'danger')
            return render_template('leave/approve.html', leave=leave)
        
        try:
            leave = leave_use_case.approve_leave(
                leave_id=leave_id,
                approver_id=current_user.user_id,
                status=status
            )
            
            flash(f'Leave {status.lower()} successfully', 'success')
            return redirect(url_for('web_leave.leave_list'))
        
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('leave/approve.html', leave=leave)