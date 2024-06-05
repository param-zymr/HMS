"""Patient Details Database Queries"""
from sqlalchemy import or_
from src.main import app_logger, db
from src.app.models.patient_details import PatientDetails
from src.app.models.doctor_details import DoctorDetails

class PatientDetailsQuery:
    def get_records(self):
        result = PatientDetails.query.all()
        app_logger.info("db select query run")
        return result
    
    
    def get_records_by_id(self, pat_id):
        result = PatientDetails.query.filter(PatientDetails.PAT_UNIQ_ID == pat_id).first()
        app_logger.info("db select query run")
        return result
        
            
    def create_record(self, data, salt):
        patient_obj = PatientDetails(**data, PAT_PASSWORD_SALT = salt)
        db.session.add(patient_obj)
        db.session.commit()
        app_logger.info("db create query sucessful")
        return
    
    
    def update_record(self, pat_id, data):
        PatientDetails.query.filter(PatientDetails.PAT_UNIQ_ID == pat_id).update(data)
        db.session.commit()
        app_logger.info("db update query sucessful")
        return True
    
    
    def check_data(self, pat_data):
        result = PatientDetails.query.filter(or_(
            PatientDetails.PAT_ADHAR == pat_data["PAT_ADHAR"],
            PatientDetails.PAT_EMAIL == pat_data["PAT_EMAIL"],
            PatientDetails.PAT_CELL== pat_data["PAT_CELL"]
            )).first()
        if result:
            app_logger.info("record exists in db with same values")
            return True
        app_logger.error("no record in db with same values")
        return False
    
    
    def check_data_by_id(self, pat_data, pat_id):
        result = PatientDetails.query.filter(PatientDetails.PAT_UNIQ_ID != pat_id)\
            .filter(or_(PatientDetails.PAT_ADHAR == pat_data["PAT_ADHAR"],
            PatientDetails.PAT_EMAIL == pat_data["PAT_EMAIL"],
            PatientDetails.PAT_CELL== pat_data["PAT_CELL"]
            )).first()
        if result:
            app_logger.info("record exists in db with same values")
            return True
        app_logger.error("no record in db with same values")
        return False
    
    
    def check_foreign_keys(self, pat_data):
        doctor_id  = DoctorDetails.query.filter\
            (DoctorDetails.DOC_UNIQ_ID == pat_data["PAT_DOC_ASSIGNED"]).first()
        if doctor_id:
            app_logger.info("Valid Doctor ID")
            return True
        app_logger.error("Invalid Doctor ID")
        return False
    
    
    def delete_record(self, pat_id):
        result = PatientDetails.query.filter(PatientDetails.PAT_UNIQ_ID == pat_id).delete()
        if result != 0:
            db.session.commit()
            app_logger.info("db delete query sucessful")
            return True
        app_logger.error("invalid id")
        return False
    
    
patient_details_query = PatientDetailsQuery()
