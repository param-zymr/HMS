"""Patient Appointment History Database Queries"""
from src.main import app_logger
from src.app.models.patient_appointments import PatientAppointments
from src.app.models.doctor_details import DoctorDetails
from src.app.models.receptionist_details import ReceptionistDetails

class PatientAppointmentsHistory:
    def appointments_list(self, pat_id):
        result = PatientAppointments.query.join\
            (DoctorDetails, PatientAppointments.APNT_DOC_ID==DoctorDetails.DOC_UNIQ_ID).join\
            (ReceptionistDetails, PatientAppointments.APNT_REC_ID==ReceptionistDetails.REC_UNIQ_ID)\
            .filter(PatientAppointments.APNT_PAT_ID == pat_id)\
            .order_by(PatientAppointments.APNT_DATE.desc(), \
            PatientAppointments.APNT_START_TIME.asc()).all()
        app_logger.info("appointment list fetched from db")
        return result
    
    
patient_appointments_history_query = PatientAppointmentsHistory()
