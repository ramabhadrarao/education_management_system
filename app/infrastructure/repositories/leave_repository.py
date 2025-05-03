# app/infrastructure/repositories/leave_repository.py
from app.application.interfaces.repositories import LeaveRepository
from app.domain.models.leave_management import FacultyLeave, PeriodAdjustment
from app import db

class SQLAlchemyLeaveRepository(LeaveRepository):
    def create_leave(self, leave):
        db.session.add(leave)
        db.session.commit()
        return leave
    
    def get_leave_by_id(self, leave_id):
        return FacultyLeave.query.get(leave_id)
    
    def update_leave(self, leave):
        db.session.commit()
        return leave
    
    def delete_leave(self, leave_id):
        leave = self.get_leave_by_id(leave_id)
        if leave:
            db.session.delete(leave)
            db.session.commit()
            return True
        return False
    
    def get_leaves_by_faculty(self, faculty_id, status=None):
        query = FacultyLeave.query.filter_by(faculty_id=faculty_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(FacultyLeave.created_at.desc()).all()
    
    def get_leaves_by_status(self, status, department_id=None):
        query = FacultyLeave.query.filter_by(status=status)
        if department_id:
            query = query.join(FacultyLeave.faculty).filter(Faculty.additional_details.has(department_id=department_id))
        return query.order_by(FacultyLeave.created_at.desc()).all()
    
    def create_adjustment(self, adjustment):
        db.session.add(adjustment)
        db.session.commit()
        return adjustment
    
    def get_adjustment_by_id(self, adjustment_id):
        return PeriodAdjustment.query.get(adjustment_id)
    
    def update_adjustment(self, adjustment):
        db.session.commit()
        return adjustment
    
    def get_adjustments_by_faculty(self, faculty_id):
        return PeriodAdjustment.query.filter_by(faculty_id=faculty_id).all()
    
    def get_adjustments_by_substitute(self, faculty_id, status=None):
        query = PeriodAdjustment.query.filter_by(substitute_faculty_id=faculty_id)
        if status:
            query = query.filter_by(status=status)
        return query.all()