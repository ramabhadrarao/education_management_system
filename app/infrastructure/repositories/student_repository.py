# app/infrastructure/repositories/student_repository.py
from app.application.interfaces.repositories import StudentRepository
from app.domain.models.student import Student
from app import db

class SQLAlchemyStudentRepository(StudentRepository):
    def create(self, student):
        db.session.add(student)
        db.session.commit()
        return student
    
    def get_by_id(self, student_id):
        return Student.query.get(student_id)
    
    def get_by_admission_no(self, admission_no):
        return Student.query.filter_by(admission_no=admission_no).first()
    
    def get_by_regd_no(self, regd_no):
        return Student.query.filter_by(regd_no=regd_no).first()
    
    def update(self, student):
        db.session.commit()
        return student
    
    def delete(self, student_id):
        student = self.get_by_id(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return True
        return False
    
    def get_by_batch(self, batch_id):
        return Student.query.filter_by(batch_id=batch_id).all()