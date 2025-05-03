# app/infrastructure/repositories/course_repository.py
from app.application.interfaces.repositories import CourseRepository
from app.domain.models.course import Course
from app import db

class SQLAlchemyCourseRepository(CourseRepository):
    def create(self, course):
        db.session.add(course)
        db.session.commit()
        return course
    
    def get_by_id(self, course_id):
        return Course.query.get(course_id)
    
    def get_by_code(self, course_code):
        return Course.query.filter_by(course_code=course_code).first()
    
    def get_by_semester(self, semester_id):
        return Course.query.filter_by(semester_id=semester_id).all()
    
    def get_by_regulation(self, regulation_id):
        return Course.query.filter_by(regulation_id=regulation_id).all()
    
    def update(self, course):
        db.session.commit()
        return course
    
    def delete(self, course_id):
        course = self.get_by_id(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return True
        return False