"""Doctor Details Database Queries"""
from sqlalchemy import or_
from src.main import app_logger, db
from src.app.models.doctor_details import DoctorDetails

class DoctorDetailsQuery:
    def get_records(self):
        result = DoctorDetails.query.all()
        app_logger.info("db select query run")
        return result
    
    
    def get_records_by_id(self, doc_id):
        result = DoctorDetails.query.filter(DoctorDetails.DOC_UNIQ_ID == doc_id).first()
        app_logger.info("db select query run")
        return result
        
            
    def create_record(self, data, salt):
        doctor_obj = DoctorDetails(**data, DOC_PASSWORD_SALT = salt)
        db.session.add(doctor_obj)
        db.session.commit()
        app_logger.info("db create query sucessful")
        return
    
    
    def update_record(self, doc_id, data):
        DoctorDetails.query.filter(DoctorDetails.DOC_UNIQ_ID == doc_id).update(data)
        db.session.commit()
        app_logger.info("db update query sucessful")
        return True
    
    
    def check_data(self, doc_data):
        result = DoctorDetails.query.filter(or_(
            DoctorDetails.DOC_LICENCE_NUMBER == doc_data["DOC_LICENCE_NUMBER"],
            DoctorDetails.DOC_EMAIL == doc_data["DOC_EMAIL"],
            DoctorDetails.DOC_CELL == doc_data["DOC_CELL"]
            )).first()
        if result:
            app_logger.info("record exists in db with same values")
            return True
        app_logger.error("no record in db with same values")
        return False
    
    
    def check_data_by_id(self, doc_data, doc_id):
        result = DoctorDetails.query.filter(DoctorDetails.DOC_UNIQ_ID != doc_id)\
            .filter(or_(DoctorDetails.DOC_LICENCE_NUMBER == doc_data["DOC_LICENCE_NUMBER"],
            DoctorDetails.DOC_EMAIL == doc_data["DOC_EMAIL"],
            DoctorDetails.DOC_CELL== doc_data["DOC_CELL"]
            )).first()
        if result:
            app_logger.info("record exists in db with same values")
            return True
        app_logger.error("no record in db with same values")
        return False
    
    
    def delete_record(self, doc_id):
        result = DoctorDetails.query.filter(DoctorDetails.DOC_UNIQ_ID == doc_id).delete()
        if result != 0:
            db.session.commit()
            app_logger.info("db delete query sucessful")
            return True
        app_logger.error("invalid id")
        return False
    
    
doctor_details_query = DoctorDetailsQuery()
