# app/infrastructure/repositories/department_repository.py
from app.application.interfaces.repositories import DepartmentRepository
from app.domain.models.department import Department
from app import db

class SQLAlchemyDepartmentRepository(DepartmentRepository):
    def create(self, department):
        db.session.add(department)
        db.session.commit()
        return department
    
    def get_by_id(self, department_id):
        return Department.query.get(department_id)
    
    def get_by_code(self, department_code):
        return Department.query.filter_by(department_code=department_code).first()
    
    def get_all(self):
        return Department.query.all()
    
    def update(self, department):
        db.session.commit()
        return department
    
    def delete(self, department_id):
        department = self.get_by_id(department_id)
        if department:
            db.session.delete(department)
            db.session.commit()
            return True
        return False