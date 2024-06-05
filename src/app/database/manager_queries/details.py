"""Manager Details Database Queries"""
from sqlalchemy import or_
from src.main import app_logger, db
from src.app.models.manager_details import ManagerDetails

class ManagerDetailsQuery:
    def get_records(self):
        result = ManagerDetails.query.all()
        app_logger.info("db select query run")
        return result
    
    
    def get_records_by_id(self, doc_id):
        result = ManagerDetails.query.filter(ManagerDetails.MNGR_UNIQ_ID == doc_id).first()
        app_logger.info("db select query run")
        return result
        
            
    def create_record(self, data, salt):
        manager_obj = ManagerDetails(**data, MNGR_PASSWORD_SALT = salt)
        db.session.add(manager_obj)
        db.session.commit()
        app_logger.info("db create query sucessful")
        return
    
    
    def update_record(self, mngr_id, data):
        ManagerDetails.query.filter(ManagerDetails.MNGR_UNIQ_ID == mngr_id).update(data)
        db.session.commit()
        app_logger.info("db update query sucessful")
        return True
    
    
    def check_data(self, mngr_data):
        result = ManagerDetails.query.filter(or_(
            ManagerDetails.MNGR_EMAIL == mngr_data["MNGR_EMAIL"],
            ManagerDetails.MNGR_CELL == mngr_data["MNGR_CELL"]
            )).first()
        if result:
            app_logger.info("record exists in db with same values")
            return True
        app_logger.error("no record in db with same values")
        return False
    
    
    def check_data_by_id(self, mngr_data, mngr_id):
        result = ManagerDetails.query.filter(ManagerDetails.MNGR_UNIQ_ID != mngr_id)\
            .filter(or_(ManagerDetails.MNGR_EMAIL == mngr_data["MNGR_EMAIL"],
            ManagerDetails.MNGR_CELL== mngr_data["MNGR_CELL"]
            )).first()
        if result:
            app_logger.info("record exists in db with same values")
            return True
        app_logger.error("no record in db with same values")
        return False
    
    
    def delete_record(self, doc_id):
        result = ManagerDetails.query.filter(ManagerDetails.MNGR_UNIQ_ID == doc_id).delete()
        if result != 0:
            db.session.commit()
            app_logger.info("db delete query sucessful")
            return True
        app_logger.error("invalid id")
        return False
    
    
manager_details_query = ManagerDetailsQuery()
