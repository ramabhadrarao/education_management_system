# app/domain/models/faculty.py
from app import db
import datetime

class Faculty(db.Model):
    __tablename__ = 'faculty'
    
    faculty_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    regdno = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    gender = db.Column(db.Enum('Male', 'Female', 'Other'))
    dob = db.Column(db.Date)
    contact_no = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text)
    join_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    edit_enabled = db.Column(db.Boolean, default=True)
    aadhar_attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    pan_attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    photo_attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    additional_details = db.relationship('FacultyAdditionalDetails', backref='faculty', uselist=False, lazy=True)
    work_experiences = db.relationship('WorkExperiences', backref='faculty', lazy=True)
    teaching_activities = db.relationship('TeachingActivities', backref='faculty', lazy=True)
    research_publications = db.relationship('ResearchPublications', backref='faculty', lazy=True)
    workshops_seminars = db.relationship('WorkshopsSeminars', backref='faculty', lazy=True)
    mdp_fdp = db.relationship('MDPFDP', backref='faculty', lazy=True)
    honours_awards = db.relationship('HonoursAwards', backref='faculty', lazy=True)
    research_consultancy = db.relationship('ResearchConsultancy', backref='faculty', lazy=True)
    activities = db.relationship('Activities', backref='faculty', lazy=True)
    
    # Additional relationships for the leave management system
    leaves = db.relationship('FacultyLeave', backref='faculty', lazy=True)
    period_adjustments = db.relationship('PeriodAdjustment', backref='faculty', lazy=True)