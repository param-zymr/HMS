"""Doctor Schedule Database Queries"""
from datetime import datetime, timedelta
from sqlalchemy import and_
from src.main import app_logger, db
from src.app.models.doctor_details import DoctorDetails
from src.app.models.doctor_schedule import DoctorSchedule
from src.main import app_settings

class DoctorScheduleQuery:
    def get_records(self):
        result = DoctorSchedule.query.all()
        app_logger.info("db select query run")
        return result
    
    
    def get_records_by_id(self, shift_id):
        result = DoctorSchedule.query.filter(DoctorSchedule.SHIFT_UNIQ_ID == shift_id).first()
        app_logger.info("db select query run")
        return result
        
            
    def create_record(self, data):
        doctor_schedule_obj = DoctorSchedule(**data)
        db.session.add(doctor_schedule_obj)
        db.session.commit()
        app_logger.info("db create query sucessful")
        return
    
    
    def update_record(self, shift_id, data):
        DoctorSchedule.query.filter(DoctorSchedule.SHIFT_UNIQ_ID == shift_id).update(data)
        db.session.commit()
        app_logger.info("db update query sucessful")
        return True
    
    
    def check_data(self, shift_data):
        shift_check = DoctorSchedule.query.filter(and_(
            DoctorSchedule.SHIFT_DOC_ID == shift_data["SHIFT_DOC_ID"],
            DoctorSchedule.SHIFT_DATE == shift_data["SHIFT_DATE"],)).first()
        if shift_check:
            app_logger.info("shift already exists")
            return True
        app_logger.error("shift doesn't exists")
        return False
    
    
    def check_data_by_id(self, shift_data, shift_id):
        shift_check = DoctorSchedule.query.filter(and_(
            DoctorSchedule.SHIFT_UNIQ_ID != shift_id,
            DoctorSchedule.SHIFT_DOC_ID == shift_data["SHIFT_DOC_ID"],
            DoctorSchedule.SHIFT_DATE == shift_data["SHIFT_DATE"],)).first()
        if shift_check:
            app_logger.info("shift already exists")
            return True
        app_logger.error("shift doesn't exists")
        return False
    
    
    def validate_shift_data(self, data):
        result = False
        shift_date, shift_start_time, shift_end_time = data["SHIFT_DATE"], \
            data["SHIFT_START_TIME"], data["SHIFT_END_TIME"]
        if isinstance(shift_date, str):
            shift_date = datetime.strptime(data["SHIFT_DATE"], "%d/%m/%Y").date()
        if isinstance(shift_start_time, str):
            shift_start_time = datetime.strptime(data["SHIFT_START_TIME"], "%H:%M").time()
        if isinstance(shift_end_time, str):
            shift_end_time = datetime.strptime(data["SHIFT_END_TIME"], "%H:%M").time()
        if (shift_date >= datetime.now().date()) and (shift_end_time > shift_start_time):
            result = True
            app_logger.info("valid schedule data")
        else:
            app_logger.error("Invalid schedule data")
        return result
    
    
    def delete_record(self, shift_id):
        result = DoctorSchedule.query.filter(DoctorSchedule.SHIFT_UNIQ_ID == shift_id).delete()
        if result != 0:
            db.session.commit()
            app_logger.info("db delete query sucessful")
            return True
        app_logger.error("invalid id")
        return False
    
    
    def check_foreign_keys(self, shift_data):
        doctor_id  = DoctorDetails.query.filter\
            (DoctorDetails.DOC_UNIQ_ID == shift_data["SHIFT_DOC_ID"]).first()
        if doctor_id:
            app_logger.info("Valid Doctor ID")
            return True
        app_logger.error("Invalid Doctor ID")
        return False
    
    
    def check_shift_availibility(self, data):
        shift_date = datetime.strptime(data["APNT_DATE"], "%d/%m/%Y").date()
        shift_start_time_temp = datetime.strptime(data["APNT_START_TIME"], "%H:%M")\
            - timedelta(minutes=app_settings.APPOINTMENT_OFFSET)
        shift_end_time_temp = datetime.strptime(data["APNT_END_TIME"], "%H:%M")\
            + timedelta(minutes=app_settings.APPOINTMENT_OFFSET)
        shift_start_time = shift_start_time_temp.time()
        shift_end_time = shift_end_time_temp.time()
        result = DoctorSchedule.query.filter(and_(
            DoctorSchedule.SHIFT_DOC_ID == data["APNT_DOC_ID"],
            DoctorSchedule.SHIFT_DATE == shift_date,
            DoctorSchedule.SHIFT_IS_AVAILABLE == True, 
            DoctorSchedule.SHIFT_START_TIME <= shift_start_time,
            DoctorSchedule.SHIFT_END_TIME >= shift_end_time,
            )).first()
        app_logger.info("doctor shift fetched from db")
        return result
    
    
    def get_doctor_shift(self, doc_id, date):
        result = DoctorSchedule.query.filter(and_(DoctorSchedule.SHIFT_DOC_ID == doc_id,
                DoctorSchedule.SHIFT_DATE == date,
                DoctorSchedule.SHIFT_IS_AVAILABLE == True)).first()
        app_logger.info("doctor shift fetched from db")
        return result
    
    
doctor_schedule_query = DoctorScheduleQuery()
