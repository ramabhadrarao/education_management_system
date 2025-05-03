# app/domain/models/faculty_details.py
from app import db
import datetime

class FacultyAdditionalDetails(db.Model):
    __tablename__ = 'faculty_additional_details'
    
    detail_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    department = db.Column(db.String(255))
    position = db.Column(db.String(255))
    profilepic = db.Column(db.String(255))
    father_name = db.Column(db.String(255))
    father_occupation = db.Column(db.String(255))
    mother_name = db.Column(db.String(255))
    mother_occupation = db.Column(db.String(255))
    marital_status = db.Column(db.String(20))
    spouse_name = db.Column(db.String(255))
    spouse_occupation = db.Column(db.String(255))
    nationality = db.Column(db.String(255))
    religion = db.Column(db.String(255))
    category = db.Column(db.String(255))
    caste = db.Column(db.String(255))
    sub_caste = db.Column(db.String(255))
    aadhar_no = db.Column(db.String(20))
    pan_no = db.Column(db.String(20))
    contact_no2 = db.Column(db.String(20))
    blood_group = db.Column(db.String(10))
    permanent_address = db.Column(db.Text)
    correspondence_address = db.Column(db.Text)
    scopus_author_id = db.Column(db.String(255))
    orcid_id = db.Column(db.String(255))
    google_scholar_id_link = db.Column(db.String(255))
    aicte_id = db.Column(db.String(255))
    scet_id = db.Column(db.String(255))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class WorkExperiences(db.Model):
    __tablename__ = 'work_experiences'
    
    experience_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    institution_name = db.Column(db.String(255), nullable=False)
    experience_type = db.Column(db.Enum('Teaching', 'Industry'), nullable=False)
    designation = db.Column(db.String(255))
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    number_of_years = db.Column(db.Integer)
    responsibilities = db.Column(db.Text)
    service_certificate_attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationship
    service_certificate = db.relationship('Attachment', foreign_keys=[service_certificate_attachment_id])

class TeachingActivities(db.Model):
    __tablename__ = 'teaching_activities'
    
    activity_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    semester = db.Column(db.String(20))
    year = db.Column(db.Integer)
    course_code = db.Column(db.String(20))
    description = db.Column(db.Text)
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationship
    attachment = db.relationship('Attachment', foreign_keys=[attachment_id])

class ResearchPublications(db.Model):
    __tablename__ = 'research_publications'
    
    publication_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    journal_name = db.Column(db.String(200))
    type_id = db.Column(db.Integer, db.ForeignKey('lookup_tables.lookup_id'))
    publication_date = db.Column(db.Date)
    doi = db.Column(db.String(50))
    description = db.Column(db.Text)
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    publication_type = db.relationship('LookupTable', foreign_keys=[type_id])
    attachment = db.relationship('Attachment', foreign_keys=[attachment_id])

class WorkshopsSeminars(db.Model):
    __tablename__ = 'workshops_seminars'
    
    workshop_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('lookup_tables.lookup_id'))
    location = db.Column(db.String(100))
    organized_by = db.Column(db.String(200))
    date = db.Column(db.Date)
    description = db.Column(db.Text)
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    workshop_type = db.relationship('LookupTable', foreign_keys=[type_id])
    attachment = db.relationship('Attachment', foreign_keys=[attachment_id])

class MDPFDP(db.Model):
    __tablename__ = 'mdp_fdp'
    
    fdp_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('lookup_tables.lookup_id'))
    location = db.Column(db.String(100))
    organized_by = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    fdp_type = db.relationship('LookupTable', foreign_keys=[type_id])
    attachment = db.relationship('Attachment', foreign_keys=[attachment_id])

class HonoursAwards(db.Model):
    __tablename__ = 'honours_awards'
    
    award_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    award_title = db.Column(db.String(200), nullable=False)
    awarded_by = db.Column(db.String(200))
    date = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('lookup_tables.lookup_id'))
    description = db.Column(db.Text)
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    award_category = db.relationship('LookupTable', foreign_keys=[category_id])
    attachment = db.relationship('Attachment', foreign_keys=[attachment_id])

class ResearchConsultancy(db.Model):
    __tablename__ = 'research_consultancy'
    
    project_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    project_title = db.Column(db.String(200), nullable=False)
    agency_id = db.Column(db.Integer, db.ForeignKey('lookup_tables.lookup_id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.Enum('Ongoing', 'Completed'))
    description = db.Column(db.Text)
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    funding_agency = db.relationship('LookupTable', foreign_keys=[agency_id])
    attachment = db.relationship('Attachment', foreign_keys=[attachment_id])

class Activities(db.Model):
    __tablename__ = 'activities'
    
    activity_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'), nullable=False)
    activity_title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100))
    date = db.Column(db.Date)
    description = db.Column(db.Text)
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachments.attachment_id'))
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationship
    attachment = db.relationship('Attachment', foreign_keys=[attachment_id])

# We also need to define the Attachment and LookupTable models
class Attachment(db.Model):
    __tablename__ = 'attachments'
    
    attachment_id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    attachment_type = db.Column(db.Enum('attachment', 'gallery_image'), nullable=False)
    visibility = db.Column(db.Enum('show', 'hide'), default='show')
    uploaded_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class LookupTable(db.Model):
    __tablename__ = 'lookup_tables'
    
    lookup_id = db.Column(db.Integer, primary_key=True)
    lookup_type = db.Column(db.String(50), nullable=False)
    lookup_value = db.Column(db.String(100), nullable=False, unique=True)