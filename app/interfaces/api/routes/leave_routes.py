# app/interfaces/api/routes/leave_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.application.use_cases.leave_management import LeaveManagementUseCase
from app.infrastructure.repositories.leave_repository import SQLAlchemyLeaveRepository
from app.infrastructure.repositories.faculty_repository import SQLAlchemyFacultyRepository
from app.infrastructure.auth.permissions import permission_required
from datetime import datetime

leave_bp = Blueprint('leave', __name__)
leave_repository = SQLAlchemyLeaveRepository()
faculty_repository = SQLAlchemyFacultyRepository()
leave_use_case = LeaveManagementUseCase(leave_repository, faculty_repository)

@leave_bp.route('/', methods=['POST'])
@jwt_required()
@permission_required('create', 'leave')
def apply_leave():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['leave_type_id', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify(message="Missing required fields"), 400
    
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        leave = leave_use_case.apply_leave(
            faculty_id=data['faculty_id'],
            leave_type_id=data['leave_type_id'],
            start_date=start_date,
            end_date=end_date,
            reason=data.get('reason')
        )
        
        return jsonify(
            message="Leave application submitted successfully",
            leave_id=leave.leave_id,
            status=leave.status
        ), 201
    
    except ValueError as e:
        return jsonify(message=str(e)), 400

@leave_bp.route('/<int:leave_id>/approve', methods=['PUT'])
@jwt_required()
@permission_required('approve', 'leave')
def approve_leave(leave_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if 'status' not in data or data['status'] not in ['Approved', 'Rejected']:
        return jsonify(message="Invalid status"), 400
    
    try:
        leave = leave_use_case.approve_leave(
            leave_id=leave_id,
            approver_id=current_user_id,
            status=data['status']
        )
        
        return jsonify(
            message=f"Leave {leave.status.lower()} successfully",
            leave_id=leave.leave_id,
            status=leave.status
        ), 200
    
    except ValueError as e:
        return jsonify(message=str(e)), 400

@leave_bp.route('/faculty/<int:faculty_id>', methods=['GET'])
@jwt_required()
@permission_required('view', 'leave')
def get_faculty_leaves(faculty_id):
    status = request.args.get('status')
    
    leaves = leave_use_case.get_faculty_leaves(faculty_id, status)
    
    return jsonify([
        {
            'leave_id': leave.leave_id,
            'leave_type': leave.leave_type.name,
            'start_date': leave.start_date.strftime('%Y-%m-%d'),
            'end_date': leave.end_date.strftime('%Y-%m-%d'),
            'reason': leave.reason,
            'status': leave.status,
            'approval_date': leave.approval_date.strftime('%Y-%m-%d') if leave.approval_date else None
        }
        for leave in leaves
    ]), 200

@leave_bp.route('/pending', methods=['GET'])
@jwt_required()
@permission_required('approve', 'leave')
def get_pending_leaves():
    department_id = request.args.get('department_id', type=int)
    
    leaves = leave_use_case.get_pending_leaves(department_id)
    
    return jsonify([
        {
            'leave_id': leave.leave_id,
            'faculty': f"{leave.faculty.first_name} {leave.faculty.last_name}",
            'leave_type': leave.leave_type.name,
            'start_date': leave.start_date.strftime('%Y-%m-%d'),
            'end_date': leave.end_date.strftime('%Y-%m-%d'),
            'reason': leave.reason,
            'status': leave.status
        }
        for leave in leaves
    ]), 200