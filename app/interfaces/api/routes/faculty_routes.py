# app/interfaces/api/routes/faculty_routes.py
from flask import Blueprint

faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.route('/', methods=['GET'])
def get_faculty_list():
    return "Get faculty list endpoint"