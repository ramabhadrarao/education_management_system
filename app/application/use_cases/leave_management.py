# app/application/use_cases/leave_management.py
import datetime
from app.domain.models.leave_management import FacultyLeave, PeriodAdjustment

class LeaveManagementUseCase:
    def __init__(self, leave_repository, faculty_repository):
        self.leave_repository = leave_repository
        self.faculty_repository = faculty_repository
    
    def apply_leave(self, faculty_id, leave_type_id, start_date, end_date, reason=None):
        # Validate the leave request
        faculty = self.faculty_repository.get_by_id(faculty_id)
        
        if not faculty:
            raise ValueError("Faculty not found")
        
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")
        
        # Calculate leave duration
        leave_duration = (end_date - start_date).days + 1
        
        # Create the leave request
        leave = FacultyLeave(
            faculty_id=faculty_id,
            leave_type_id=leave_type_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status='Pending'
        )
        
        return self.leave_repository.create_leave(leave)
    
    def approve_leave(self, leave_id, approver_id, status):
        leave = self.leave_repository.get_leave_by_id(leave_id)
        
        if not leave:
            raise ValueError("Leave request not found")
        
        if leave.status != 'Pending':
            raise ValueError("Leave request already processed")
        
        leave.status = status
        leave.approved_by = approver_id
        leave.approval_date = datetime.datetime.utcnow()
        
        return self.leave_repository.update_leave(leave)
    
    def get_faculty_leaves(self, faculty_id, status=None):
        return self.leave_repository.get_leaves_by_faculty(faculty_id, status)
    
    def get_pending_leaves(self, department_id=None):
        return self.leave_repository.get_leaves_by_status('Pending', department_id)
    
    def create_period_adjustment(self, leave_id, faculty_id, substitute_faculty_id, course_id, batch_id, adjustment_date, period_number):
        # Create a period adjustment request
        adjustment = PeriodAdjustment(
            leave_id=leave_id,
            faculty_id=faculty_id,
            substitute_faculty_id=substitute_faculty_id,
            course_id=course_id,
            batch_id=batch_id,
            adjustment_date=adjustment_date,
            period_number=period_number,
            status='Pending'
        )
        
        return self.leave_repository.create_adjustment(adjustment)
    
    def respond_to_adjustment(self, adjustment_id, status):
        adjustment = self.leave_repository.get_adjustment_by_id(adjustment_id)
        
        if not adjustment:
            raise ValueError("Adjustment request not found")
        
        if adjustment.status != 'Pending':
            raise ValueError("Adjustment request already processed")
        
        adjustment.status = status
        
        return self.leave_repository.update_adjustment(adjustment)