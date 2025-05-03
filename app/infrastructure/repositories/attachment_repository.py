# app/infrastructure/repositories/attachment_repository.py
from app.application.interfaces.repositories import AttachmentRepository
from app.domain.models.faculty_details import Attachment
from app import db

class SQLAlchemyAttachmentRepository(AttachmentRepository):
    def create(self, attachment):
        db.session.add(attachment)
        db.session.commit()
        return attachment
    
    def get_by_id(self, attachment_id):
        return Attachment.query.get(attachment_id)
    
    def update(self, attachment):
        db.session.commit()
        return attachment
    
    def delete(self, attachment_id):
        attachment = self.get_by_id(attachment_id)
        if attachment:
            db.session.delete(attachment)
            db.session.commit()
            return True
        return False