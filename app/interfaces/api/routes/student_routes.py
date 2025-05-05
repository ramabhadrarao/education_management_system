# app/interfaces/api/routes/student_routes.py
from flask import Blueprint

student_bp = Blueprint('student', __name__)

@student_bp.route('/', methods=['GET'])
def get_student_list():
    return "Get student list endpoint"