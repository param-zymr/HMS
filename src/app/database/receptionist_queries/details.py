"""Receptionist Details Database Queries"""
from sqlalchemy import or_
from src.main import app_logger, db
from src.app.models.receptionist_details import ReceptionistDetails

class ReceptionistQuery:
    def get_records(self):
        result = ReceptionistDetails.query.all()
        app_logger.info("db select query run")
        return result
    
    
    def get_records_by_id(self, rec_id):
        result = ReceptionistDetails.query.filter(\
        ReceptionistDetails.REC_UNIQ_ID == rec_id).first()
        app_logger.info("db select query run")
        return result
    
            
    def create_record(self, data, salt):
        receptionist_obj = ReceptionistDetails(**data, REC_PASSWORD_SALT = salt)
        db.session.add(receptionist_obj)
        db.session.commit()
        app_logger.info("db create query sucessful")
        return
    
    
    def update_record(self, rec_id, data):
        ReceptionistDetails.query.filter\
        (ReceptionistDetails.REC_UNIQ_ID == rec_id).update(data)
        db.session.commit()
        app_logger.info("db update query sucessful")
        return True
    
    
    def check_data(self, rec_data):
        result = ReceptionistDetails.query.filter(or_(
            ReceptionistDetails.REC_EMAIL == rec_data["REC_EMAIL"],
            ReceptionistDetails.REC_CELL == rec_data["REC_CELL"]
            )).first()
        if result:
            app_logger.info("record exists in db with same values")
            return True
        app_logger.error("no record in db with same values")
        return False
    
    
    def check_data_by_id(self, rec_data, rec_id):
        result = ReceptionistDetails.query.filter(ReceptionistDetails.REC_UNIQ_ID != rec_id)\
            .filter(or_(ReceptionistDetails.REC_EMAIL == rec_data["REC_EMAIL"],
            ReceptionistDetails.REC_CELL == rec_data["REC_CELL"]
            )).first()
        if result:
            app_logger.info("record exists in db with same values")
            return True
        app_logger.error("no record in db with same values")
        return False
    
    
    def delete_record(self, rec_id):
        result = ReceptionistDetails.query.filter\
        (ReceptionistDetails.REC_UNIQ_ID == rec_id).delete()
        if result != 0:
            db.session.commit()
            app_logger.info("db delete query sucessful")
            return True
        app_logger.error("invalid id")
        return False
    
    
receptionist_details_query = ReceptionistQuery()
