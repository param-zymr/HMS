"""Patient Appointments Database Queries"""
from datetime import datetime
from sqlalchemy import and_
from src.main import app_logger, db
from src.app.models.patient_details import PatientDetails
from src.app.models.patient_appointments import PatientAppointments
from src.app.models.doctor_details import DoctorDetails
from src.app.models.receptionist_details import ReceptionistDetails

class PatientAppointmentsQuery:
    def get_records(self):
        result = PatientAppointments.query.all()
        app_logger.info("db select query run")
        return result
    
    
    def get_records_by_id(self, apnt_id):
        result = PatientAppointments.query.filter\
            (PatientAppointments.APNT_UNIQ_ID == apnt_id).first()
        app_logger.info("db select query run")
        return result
        
            
    def create_record(self, data):
        appointment_obj = PatientAppointments(**data)
        db.session.add(appointment_obj)
        db.session.commit()
        app_logger.info("db create query sucessful")
        return
    
    
    def update_record(self, apnt_id, data):
        PatientAppointments.query.filter\
        (PatientAppointments.APNT_UNIQ_ID == apnt_id).update(data)
        db.session.commit()
        app_logger.info("db update query sucessful")
        return True
    
    
    def check_data(self, data):
        result = False
        apnt_date, apnt_reg_date, apnt_start_time, apnt_end_time = data["APNT_DATE"], \
            data["APNT_REG_DATE"], data["APNT_START_TIME"], data["APNT_END_TIME"]
        if isinstance(apnt_date, str):
            apnt_date = datetime.strptime(data["APNT_DATE"], "%d/%m/%Y").date()
        if isinstance(apnt_reg_date, str):
            apnt_reg_date = datetime.strptime(data["APNT_REG_DATE"], "%Y/%m/%d").date()
        if isinstance(apnt_start_time, str):
            apnt_start_time = datetime.strptime(data["APNT_START_TIME"], "%H:%M").time()
        if isinstance(apnt_end_time, str):
            apnt_end_time = datetime.strptime(data["APNT_END_TIME"], "%H:%M").time()
        if (apnt_date >= apnt_reg_date and apnt_end_time > apnt_start_time):
            result = True
            app_logger.info("valid appointment data")
        else:
            app_logger.error("Invalid appointment data")
        return result
    
    
    def check_foreign_keys(self, data):
        pat_id  = PatientDetails.query.filter\
            (PatientDetails.PAT_UNIQ_ID == data["APNT_PAT_ID"]).first()
        doc_id  = DoctorDetails.query.filter\
            (DoctorDetails.DOC_UNIQ_ID == data["APNT_DOC_ID"]).first()
        rec_id  = ReceptionistDetails.query.filter\
            (ReceptionistDetails.REC_UNIQ_ID == data["APNT_REC_ID"]).first()
        if None in [pat_id, doc_id, rec_id]:
            app_logger.error("Invalid foreign key data")
            return False
        app_logger.info("Valid foreign key data")
        return True
    
    
    def delete_record(self, apnt_id):
        result = PatientAppointments.query.filter\
        (PatientAppointments.APNT_UNIQ_ID == apnt_id).delete()
        if result != 0:
            db.session.commit()
            app_logger.info("db delete query sucessful")
            return True
        app_logger.error("invalid id")
        return False
    
    
    def appointments_list(self, data):
        result = PatientAppointments.query.filter(and_(
            PatientAppointments.APNT_DOC_ID == data["APNT_DOC_ID"],
            PatientAppointments.APNT_DATE == data["APNT_DATE"],
            )).order_by(PatientAppointments.APNT_START_TIME.asc()).all()
        app_logger.info("appointment list fetched from db")
        return result
    
    
    def appointments_list_by_id(self, data, apnt_id):
        result = PatientAppointments.query.filter(and_(
            PatientAppointments.APNT_UNIQ_ID != apnt_id,
            PatientAppointments.APNT_DOC_ID == data["APNT_DOC_ID"],
            PatientAppointments.APNT_DATE == data["APNT_DATE"],
            )).order_by(PatientAppointments.APNT_START_TIME.asc()).all()
        app_logger.info("appointment list fetched from db")
        return result
    
    
    
patient_appointments_query = PatientAppointmentsQuery()
