# app/interfaces/web/controllers/faculty_profile_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.domain.models.faculty import Faculty
from app.domain.models.faculty_details import *
from app.domain.models.user import User
from app import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime

web_faculty_profile_bp = Blueprint('web_faculty_profile', __name__)

@web_faculty_profile_bp.route('/<int:faculty_id>')
@login_required
def view_profile(faculty_id):
    # Check if current user has permission to view this profile
    if current_user.role not in ['admin', 'hod'] and (current_user.role != 'faculty' or 
                                                     current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_dashboard.index'))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    
    # Get all related data
    additional_details = FacultyAdditionalDetails.query.filter_by(faculty_id=faculty_id).first()
    work_experiences = WorkExperiences.query.filter_by(faculty_id=faculty_id).all()
    teaching_activities = TeachingActivities.query.filter_by(faculty_id=faculty_id).all()
    research_publications = ResearchPublications.query.filter_by(faculty_id=faculty_id).all()
    workshops_seminars = WorkshopsSeminars.query.filter_by(faculty_id=faculty_id).all()
    mdp_fdp = MDPFDP.query.filter_by(faculty_id=faculty_id).all()
    honours_awards = HonoursAwards.query.filter_by(faculty_id=faculty_id).all()
    research_consultancy = ResearchConsultancy.query.filter_by(faculty_id=faculty_id).all()
    activities = Activities.query.filter_by(faculty_id=faculty_id).all()
    
    return render_template('faculty_profile/view.html', 
                           faculty=faculty,
                           additional_details=additional_details,
                           work_experiences=work_experiences,
                           teaching_activities=teaching_activities,
                           research_publications=research_publications,
                           workshops_seminars=workshops_seminars,
                           mdp_fdp=mdp_fdp,
                           honours_awards=honours_awards,
                           research_consultancy=research_consultancy,
                           activities=activities)

@web_faculty_profile_bp.route('/<int:faculty_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(faculty_id):
    # Check if current user has permission to edit this profile
    faculty = Faculty.query.get_or_404(faculty_id)
    
    if current_user.role != 'admin' and (current_user.role != 'faculty' or 
                                       current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    # Check if editing is enabled for this faculty
    if current_user.role != 'admin' and not faculty.edit_enabled:
        flash('Profile editing is currently disabled', 'warning')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    additional_details = FacultyAdditionalDetails.query.filter_by(faculty_id=faculty_id).first()
    
    if request.method == 'POST':
        # Update basic faculty information
        faculty.first_name = request.form.get('first_name')
        faculty.last_name = request.form.get('last_name')
        faculty.gender = request.form.get('gender')
        faculty.dob = datetime.strptime(request.form.get('dob'), '%Y-%m-%d').date() if request.form.get('dob') else None
        faculty.contact_no = request.form.get('contact_no')
        faculty.email = request.form.get('email')
        faculty.address = request.form.get('address')
        
        # Update or create additional details
        if not additional_details:
            additional_details = FacultyAdditionalDetails(faculty_id=faculty_id)
            db.session.add(additional_details)
        
        additional_details.department = request.form.get('department')
        additional_details.position = request.form.get('position')
        additional_details.father_name = request.form.get('father_name')
        additional_details.father_occupation = request.form.get('father_occupation')
        additional_details.mother_name = request.form.get('mother_name')
        additional_details.mother_occupation = request.form.get('mother_occupation')
        additional_details.marital_status = request.form.get('marital_status')
        additional_details.spouse_name = request.form.get('spouse_name')
        additional_details.spouse_occupation = request.form.get('spouse_occupation')
        additional_details.nationality = request.form.get('nationality')
        additional_details.religion = request.form.get('religion')
        additional_details.category = request.form.get('category')
        additional_details.caste = request.form.get('caste')
        additional_details.sub_caste = request.form.get('sub_caste')
        additional_details.aadhar_no = request.form.get('aadhar_no')
        additional_details.pan_no = request.form.get('pan_no')
        additional_details.contact_no2 = request.form.get('contact_no2')
        additional_details.blood_group = request.form.get('blood_group')
        additional_details.permanent_address = request.form.get('permanent_address')
        additional_details.correspondence_address = request.form.get('correspondence_address')
        additional_details.scopus_author_id = request.form.get('scopus_author_id')
        additional_details.orcid_id = request.form.get('orcid_id')
        additional_details.google_scholar_id_link = request.form.get('google_scholar_id_link')
        additional_details.aicte_id = request.form.get('aicte_id')
        
        # Handle file uploads
        if 'profile_photo' in request.files and request.files['profile_photo'].filename:
            file = request.files['profile_photo']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create attachment record
            attachment = Attachment(
                file_path=filename,
                attachment_type='attachment'
            )
            db.session.add(attachment)
            db.session.flush()  # Get the ID without committing
            
            # Update faculty photo attachment
            faculty.photo_attachment_id = attachment.attachment_id
            
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    return render_template('faculty_profile/edit.html', faculty=faculty, additional_details=additional_details)

# Routes for managing specific sections of faculty profile

@web_faculty_profile_bp.route('/<int:faculty_id>/work-experience/add', methods=['GET', 'POST'])
@login_required
def add_work_experience(faculty_id):
    # Permission check
    if current_user.role != 'admin' and (current_user.role != 'faculty' or 
                                       current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    
    if request.method == 'POST':
        # Create new work experience
        work_exp = WorkExperiences(
            faculty_id=faculty_id,
            institution_name=request.form.get('institution_name'),
            experience_type=request.form.get('experience_type'),
            designation=request.form.get('designation'),
            from_date=datetime.strptime(request.form.get('from_date'), '%Y-%m-%d').date() if request.form.get('from_date') else None,
            to_date=datetime.strptime(request.form.get('to_date'), '%Y-%m-%d').date() if request.form.get('to_date') else None,
            number_of_years=request.form.get('number_of_years', type=int),
            responsibilities=request.form.get('responsibilities')
        )
        
        # Handle certificate upload
        if 'certificate' in request.files and request.files['certificate'].filename:
            file = request.files['certificate']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create attachment record
            attachment = Attachment(
                file_path=filename,
                attachment_type='attachment'
            )
            db.session.add(attachment)
            db.session.flush()  # Get the ID without committing
            
            # Update work experience with attachment
            work_exp.service_certificate_attachment_id = attachment.attachment_id
        
        db.session.add(work_exp)
        db.session.commit()
        
        flash('Work experience added successfully', 'success')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    return render_template('faculty_profile/work_experience_form.html', faculty=faculty)

@web_faculty_profile_bp.route('/<int:faculty_id>/publication/add', methods=['GET', 'POST'])
@login_required
def add_publication(faculty_id):
    # Permission check
    if current_user.role != 'admin' and (current_user.role != 'faculty' or 
                                       current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    publication_types = LookupTable.query.filter_by(lookup_type='publication_type').all()
    
    if request.method == 'POST':
        # Create new publication
        publication = ResearchPublications(
            faculty_id=faculty_id,
            title=request.form.get('title'),
            journal_name=request.form.get('journal_name'),
            type_id=request.form.get('type_id', type=int),
            publication_date=datetime.strptime(request.form.get('publication_date'), '%Y-%m-%d').date() if request.form.get('publication_date') else None,
            doi=request.form.get('doi'),
            description=request.form.get('description')
        )
        
        # Handle publication attachment
        if 'publication_file' in request.files and request.files['publication_file'].filename:
            file = request.files['publication_file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create attachment record
            attachment = Attachment(
                file_path=filename,
                attachment_type='attachment'
            )
            db.session.add(attachment)
            db.session.flush()  # Get the ID without committing
            
            # Update publication with attachment
            publication.attachment_id = attachment.attachment_id
        
        db.session.add(publication)
        db.session.commit()
        
        flash('Publication added successfully', 'success')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    return render_template('faculty_profile/publication_form.html', faculty=faculty, publication_types=publication_types)

# Similar routes can be created for other sections like:
# - add_teaching_activity
# - add_workshop_seminar
# - add_mdp_fdp
# - add_honour_award
# - add_research_consultancy
# - add_activity

@web_faculty_profile_bp.route('/<int:faculty_id>/teaching-activity/add', methods=['GET', 'POST'])
@login_required
def add_teaching_activity(faculty_id):
    # Permission check
    if current_user.role != 'admin' and (current_user.role != 'faculty' or 
                                       current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    
    if request.method == 'POST':
        # Create new teaching activity
        teaching_activity = TeachingActivities(
            faculty_id=faculty_id,
            course_name=request.form.get('course_name'),
            semester=request.form.get('semester'),
            year=request.form.get('year', type=int),
            course_code=request.form.get('course_code'),
            description=request.form.get('description')
        )
        
        # Handle attachment upload
        if 'activity_file' in request.files and request.files['activity_file'].filename:
            file = request.files['activity_file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create attachment record
            attachment = Attachment(
                file_path=filename,
                attachment_type='attachment'
            )
            db.session.add(attachment)
            db.session.flush()  # Get the ID without committing
            
            teaching_activity.attachment_id = attachment.attachment_id
        
        db.session.add(teaching_activity)
        db.session.commit()
        
        flash('Teaching activity added successfully', 'success')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    return render_template('faculty_profile/teaching_activity_form.html', faculty=faculty)

@web_faculty_profile_bp.route('/<int:faculty_id>/workshop/add', methods=['GET', 'POST'])
@login_required
def add_workshop(faculty_id):
    # Permission check
    if current_user.role != 'admin' and (current_user.role != 'faculty' or 
                                       current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    workshop_types = LookupTable.query.filter_by(lookup_type='workshop_type').all()
    
    if request.method == 'POST':
        # Create new workshop/seminar
        workshop = WorkshopsSeminars(
            faculty_id=faculty_id,
            title=request.form.get('title'),
            type_id=request.form.get('type_id', type=int),
            location=request.form.get('location'),
            organized_by=request.form.get('organized_by'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else None,
            description=request.form.get('description')
        )
        
        # Handle certificate upload
        if 'certificate' in request.files and request.files['certificate'].filename:
            file = request.files['certificate']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create attachment record
            attachment = Attachment(
                file_path=filename,
                attachment_type='attachment'
            )
            db.session.add(attachment)
            db.session.flush()  # Get the ID without committing
            
            workshop.attachment_id = attachment.attachment_id
        
        db.session.add(workshop)
        db.session.commit()
        
        flash('Workshop/Seminar added successfully', 'success')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    return render_template('faculty_profile/workshop_form.html', faculty=faculty, workshop_types=workshop_types)

@web_faculty_profile_bp.route('/<int:faculty_id>/mdp-fdp/add', methods=['GET', 'POST'])
@login_required
def add_mdp_fdp(faculty_id):
    # Permission check
    if current_user.role != 'admin' and (current_user.role != 'faculty' or 
                                       current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    fdp_types = LookupTable.query.filter_by(lookup_type='fdp_type').all()
    
    if request.method == 'POST':
        # Create new MDP/FDP entry
        mdp_fdp = MDPFDP(
            faculty_id=faculty_id,
            title=request.form.get('title'),
            type_id=request.form.get('type_id', type=int),
            location=request.form.get('location'),
            organized_by=request.form.get('organized_by'),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None,
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
            description=request.form.get('description')
        )
        
        # Handle certificate upload
        if 'certificate' in request.files and request.files['certificate'].filename:
            file = request.files['certificate']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create attachment record
            attachment = Attachment(
                file_path=filename,
                attachment_type='attachment'
            )
            db.session.add(attachment)
            db.session.flush()  # Get the ID without committing
            
            mdp_fdp.attachment_id = attachment.attachment_id
        
        db.session.add(mdp_fdp)
        db.session.commit()
        
        flash('MDP/FDP record added successfully', 'success')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    return render_template('faculty_profile/mdp_fdp_form.html', faculty=faculty, fdp_types=fdp_types)

@web_faculty_profile_bp.route('/<int:faculty_id>/award/add', methods=['GET', 'POST'])
@login_required
def add_award(faculty_id):
    # Permission check
    if current_user.role != 'admin' and (current_user.role != 'faculty' or 
                                       current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    award_categories = LookupTable.query.filter_by(lookup_type='award_category').all()
    
    if request.method == 'POST':
        # Create new award
        award = HonoursAwards(
            faculty_id=faculty_id,
            award_title=request.form.get('award_title'),
            awarded_by=request.form.get('awarded_by'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else None,
            category_id=request.form.get('category_id', type=int),
            description=request.form.get('description')
        )
        
        # Handle certificate upload
        if 'certificate' in request.files and request.files['certificate'].filename:
            file = request.files['certificate']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create attachment record
            attachment = Attachment(
                file_path=filename,
                attachment_type='attachment'
            )
            db.session.add(attachment)
            db.session.flush()  # Get the ID without committing
            
            award.attachment_id = attachment.attachment_id
        
        db.session.add(award)
        db.session.commit()
        
        flash('Award added successfully', 'success')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    return render_template('faculty_profile/award_form.html', faculty=faculty, award_categories=award_categories)

@web_faculty_profile_bp.route('/<int:faculty_id>/research-consultancy/add', methods=['GET', 'POST'])
@login_required
def add_research_consultancy(faculty_id):
    # Permission check
    if current_user.role != 'admin' and (current_user.role != 'faculty' or 
                                       current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    funding_agencies = LookupTable.query.filter_by(lookup_type='funding_agency').all()
    
    if request.method == 'POST':
        # Create new research/consultancy project
        project = ResearchConsultancy(
            faculty_id=faculty_id,
            project_title=request.form.get('project_title'),
            agency_id=request.form.get('agency_id', type=int),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date() if request.form.get('start_date') else None,
            end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
            status=request.form.get('status'),
            description=request.form.get('description')
        )
        
        # Handle attachment upload
        if 'project_file' in request.files and request.files['project_file'].filename:
            file = request.files['project_file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create attachment record
            attachment = Attachment(
                file_path=filename,
                attachment_type='attachment'
            )
            db.session.add(attachment)
            db.session.flush()  # Get the ID without committing
            
            project.attachment_id = attachment.attachment_id
        
        db.session.add(project)
        db.session.commit()
        
        flash('Research/Consultancy project added successfully', 'success')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    return render_template('faculty_profile/research_consultancy_form.html', faculty=faculty, funding_agencies=funding_agencies)

@web_faculty_profile_bp.route('/<int:faculty_id>/activity/add', methods=['GET', 'POST'])
@login_required
def add_activity(faculty_id):
    # Permission check
    if current_user.role != 'admin' and (current_user.role != 'faculty' or 
                                       current_user.faculty.faculty_id != faculty_id):
        flash('Access denied', 'danger')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    faculty = Faculty.query.get_or_404(faculty_id)
    
    if request.method == 'POST':
        # Create new activity
        activity = Activities(
            faculty_id=faculty_id,
            activity_title=request.form.get('activity_title'),
            type=request.form.get('type'),
            date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else None,
            description=request.form.get('description')
        )
        
        # Handle attachment upload
        if 'activity_file' in request.files and request.files['activity_file'].filename:
            file = request.files['activity_file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Create attachment record
            attachment = Attachment(
                file_path=filename,
                attachment_type='attachment'
            )
            db.session.add(attachment)
            db.session.flush()  # Get the ID without committing
            
            activity.attachment_id = attachment.attachment_id
        
        db.session.add(activity)
        db.session.commit()
        
        flash('Activity added successfully', 'success')
        return redirect(url_for('web_faculty_profile.view_profile', faculty_id=faculty_id))
    
    return render_template('faculty_profile/activity_form.html', faculty=faculty)