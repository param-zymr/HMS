"""App Doctor Appointment List Router"""
from datetime import datetime
from flask import Blueprint, request, make_response
from src.app.database.doctor_queries.appointments import doctor_appointment_query
from src.app.utils.authorisation.access_control import verify_auth
from src.main import app_logger

doctor_appointments_list = Blueprint('doctor_appointments_list', __name__)

@doctor_appointments_list.route("/<int:doc_id>", methods=["GET"])
@verify_auth(permission_needed = ["doctor_appointment_list"])
def get_doctor_appointments_list(doc_id):
    date = datetime.strptime(request.json["APNT_DATE"], "%d/%m/%Y").date()
    all_appointments = doctor_appointment_query.appointments_list(doc_id, date)
    response_json=[]
    if all_appointments:
        for row in all_appointments:
            appointments_data={
                "Appintment ID":row.APNT_UNIQ_ID,
                "Patient ID":row.APNT_PAT_ID,
                "Patient Name":row.patient_details.PAT_FNAME + " " \
                    + row.patient_details.PAT_LNAME,
                "Title":row.APNT_TITLE,
                "Details":row.APNT_DETAILS,
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
