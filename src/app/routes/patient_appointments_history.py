"""App Patient Appointment History Functionality Router """
from flask import Blueprint, make_response
from src.app.database.patient_queries.appointments_history import patient_appointments_history_query
from src.app.utils.authorisation.access_control import verify_auth
from src.main import app_logger

patient_appointments_history = Blueprint('patient_appointments_history', __name__)

@patient_appointments_history.route("/<int:pat_id>", methods=["GET"])
@verify_auth(permission_needed = ["patient_appointment_history"])
def get_patient_appointments_history(pat_id):
    all_appointments = patient_appointments_history_query.appointments_list(pat_id)
    response_json=[]
    if all_appointments:
        for row in all_appointments:
            appointments_data={
                "Appintment ID":row.APNT_UNIQ_ID,
                "Doctor ID":row.APNT_DOC_ID,
                "Doctor Name":row.doctor_details.DOC_FNAME + " " \
                    + row.doctor_details.DOC_LNAME,
                "Title":row.APNT_TITLE,
                "Details":row.APNT_DETAILS,
                "Date":row.APNT_DATE.strftime('%d/%m/%Y'),
                "Start Time":row.APNT_START_TIME.strftime('%H:%M'),
                "End Time":row.APNT_END_TIME.strftime('%H:%M'),
                "Receptionist ID":row.APNT_REC_ID,
                "Receptionist Name":row.receptionist_details.REC_FNAME + " " \
                    + row.receptionist_details.REC_LNAME,
                "Registration Date":row.APNT_REG_DATE.strftime('%d/%m/%Y'),
                "Registration Time":row.APNT_REG_TIME.strftime('%H:%M:%S')
            }
            response_json.append(appointments_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("no records found") 
    return make_response({"Message":"No records found"}, 200)
