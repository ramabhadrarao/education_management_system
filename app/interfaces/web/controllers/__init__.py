# app/interfaces/web/controllers/__init__.py
from flask import Blueprint

web_auth_bp = Blueprint('web_auth', __name__)
web_dashboard_bp = Blueprint('web_dashboard', __name__)
web_faculty_bp = Blueprint('web_faculty', __name__)
web_student_bp = Blueprint('web_student', __name__)

@web_auth_bp.route('/')
def auth_index():
    return "Auth index"

@web_dashboard_bp.route('/')
def dashboard_index():
    return "Dashboard index"

@web_faculty_bp.route('/')
def faculty_index():
    return "Faculty index"

@web_student_bp.route('/')
def student_index():
    return "Student index"