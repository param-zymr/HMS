"""Doctor Appointment Database Queries"""
from sqlalchemy import and_
from src.main import app_logger
from src.app.models.patient_details import PatientDetails
from src.app.models.patient_appointments import PatientAppointments
from src.app.models.receptionist_details import ReceptionistDetails

class DoctorAppointmentsQuery:
    def appointments_list(self, doc_id, apnt_date):
        result = PatientAppointments.query.join\
            (PatientDetails, PatientAppointments.APNT_PAT_ID==PatientDetails.PAT_UNIQ_ID).join\
            (ReceptionistDetails, PatientAppointments.APNT_REC_ID==ReceptionistDetails.REC_UNIQ_ID)\
            .filter(and_(PatientAppointments.APNT_DOC_ID == doc_id,
            PatientAppointments.APNT_DATE == apnt_date))\
            .order_by(PatientAppointments.APNT_START_TIME.asc()).all()
        app_logger.info("appointment list fetched from db")
        return result
    
doctor_appointment_query = DoctorAppointmentsQuery()
