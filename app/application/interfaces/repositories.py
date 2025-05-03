# app/application/interfaces/repositories.py
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def create(self, user):
        pass
    
    @abstractmethod
    def get_by_id(self, user_id):
        pass
    
    @abstractmethod
    def get_by_username(self, username):
        pass
    
    @abstractmethod
    def get_by_email(self, email):
        pass
    
    @abstractmethod
    def update(self, user):
        pass
    
    @abstractmethod
    def delete(self, user_id):
        pass

class FacultyRepository(ABC):
    @abstractmethod
    def create(self, faculty):
        pass
    
    @abstractmethod
    def get_by_id(self, faculty_id):
        pass
    
    @abstractmethod
    def get_by_regdno(self, regdno):
        pass
    
    @abstractmethod
    def update(self, faculty):
        pass
    
    @abstractmethod
    def delete(self, faculty_id):
        pass

class StudentRepository(ABC):
    @abstractmethod
    def create(self, student):
        pass
    
    @abstractmethod
    def get_by_id(self, student_id):
        pass
    
    @abstractmethod
    def get_by_admission_no(self, admission_no):
        pass
    
    @abstractmethod
    def get_by_regd_no(self, regd_no):
        pass
    
    @abstractmethod
    def update(self, student):
        pass
    
    @abstractmethod
    def delete(self, student_id):
        pass
    
    @abstractmethod
    def get_by_batch(self, batch_id):
        pass

class LeaveRepository(ABC):
    @abstractmethod
    def create_leave(self, leave):
        pass
    
    @abstractmethod
    def get_leave_by_id(self, leave_id):
        pass
    
    @abstractmethod
    def update_leave(self, leave):
        pass
    
    @abstractmethod
    def delete_leave(self, leave_id):
        pass
    
    @abstractmethod
    def get_leaves_by_faculty(self, faculty_id, status=None):
        pass
    
    @abstractmethod
    def get_leaves_by_status(self, status, department_id=None):
        pass
    
    @abstractmethod
    def create_adjustment(self, adjustment):
        pass
    
    @abstractmethod
    def get_adjustment_by_id(self, adjustment_id):
        pass
    
    @abstractmethod
    def update_adjustment(self, adjustment):
        pass
    
    @abstractmethod
    def get_adjustments_by_faculty(self, faculty_id):
        pass
    
    @abstractmethod
    def get_adjustments_by_substitute(self, faculty_id, status=None):
        pass

class AttachmentRepository(ABC):
    @abstractmethod
    def create(self, attachment):
        pass
    
    @abstractmethod
    def get_by_id(self, attachment_id):
        pass
    
    @abstractmethod
    def update(self, attachment):
        pass
    
    @abstractmethod
    def delete(self, attachment_id):
        pass

class LookupRepository(ABC):
    @abstractmethod
    def create(self, lookup):
        pass
    
    @abstractmethod
    def get_by_id(self, lookup_id):
        pass
    
    @abstractmethod
    def get_by_type(self, lookup_type):
        pass
    
    @abstractmethod
    def get_by_value(self, lookup_value):
        pass
    
    @abstractmethod
    def update(self, lookup):
        pass
    
    @abstractmethod
    def delete(self, lookup_id):
        pass

class DepartmentRepository(ABC):
    @abstractmethod
    def create(self, department):
        pass
    
    @abstractmethod
    def get_by_id(self, department_id):
        pass
    
    @abstractmethod
    def get_by_code(self, department_code):
        pass
    
    @abstractmethod
    def get_all(self):
        pass
    
    @abstractmethod
    def update(self, department):
        pass
    
    @abstractmethod
    def delete(self, department_id):
        pass

class CourseRepository(ABC):
    @abstractmethod
    def create(self, course):
        pass
    
    @abstractmethod
    def get_by_id(self, course_id):
        pass
    
    @abstractmethod
    def get_by_code(self, course_code):
        pass
    
    @abstractmethod
    def get_by_semester(self, semester_id):
        pass
    
    @abstractmethod
    def get_by_regulation(self, regulation_id):
        pass
    
    @abstractmethod
    def update(self, course):
        pass
    
    @abstractmethod
    def delete(self, course_id):
        pass
# Similar interfaces for StudentRepository, LeaveRepository, etc.