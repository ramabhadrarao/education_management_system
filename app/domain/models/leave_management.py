# Additional domain models for leave management system
# app/domain/models/leave_management.py
from app import db
import datetime

class LeaveType(db.Model):
    __tablename__ = 'leave_types'
    
    leave_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    max_days_allowed = db.Column(db.Integer, default=0)
    requires_approval = db.Column(db.Boolean, default=True)
    
class FacultyLeave(db.Model):
    __tablename__ = 'faculty_leaves'
    
    leave_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_types.leave_type_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected'), default='Pending')
    approved_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    approval_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    leave_type = db.relationship('LeaveType', backref='faculty_leaves')
    approver = db.relationship('User', foreign_keys=[approved_by])

class PeriodAdjustment(db.Model):
    __tablename__ = 'period_adjustments'
    
    adjustment_id = db.Column(db.Integer, primary_key=True)
    leave_id = db.Column(db.Integer, db.ForeignKey('faculty_leaves.leave_id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    substitute_faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batches.batch_id'), nullable=False)
    adjustment_date = db.Column(db.Date, nullable=False)
    period_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('Pending', 'Accepted', 'Rejected'), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    leave = db.relationship('FacultyLeave', backref='period_adjustments')
    substitute_faculty = db.relationship('Faculty', foreign_keys=[substitute_faculty_id], backref='substituting_periods')
    course = db.relationship('Course')
    batch = db.relationship('Batch')