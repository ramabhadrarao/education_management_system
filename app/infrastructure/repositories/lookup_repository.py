# app/infrastructure/repositories/lookup_repository.py
from app.application.interfaces.repositories import LookupRepository
from app.domain.models.faculty_details import LookupTable
from app import db

class SQLAlchemyLookupRepository(LookupRepository):
    def create(self, lookup):
        db.session.add(lookup)
        db.session.commit()
        return lookup
    
    def get_by_id(self, lookup_id):
        return LookupTable.query.get(lookup_id)
    
    def get_by_type(self, lookup_type):
        return LookupTable.query.filter_by(lookup_type=lookup_type).all()
    
    def get_by_value(self, lookup_value):
        return LookupTable.query.filter_by(lookup_value=lookup_value).first()
    
    def update(self, lookup):
        db.session.commit()
        return lookup
    
    def delete(self, lookup_id):
        lookup = self.get_by_id(lookup_id)
        if lookup:
            db.session.delete(lookup)
            db.session.commit()
            return True
        return False