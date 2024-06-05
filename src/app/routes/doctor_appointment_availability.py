"""App Doctor Appointment Availability Router"""
from datetime import datetime
from flask import Blueprint, request, make_response
from src.app.core.patient import appointments
from src.app.database.doctor_queries.details import doctor_details_query
from src.app.utils.authorisation.access_control import verify_auth
from src.main import app_logger

doctor_appointment_availability = Blueprint('doctor_appointment_availability', __name__)

@doctor_appointment_availability.route("/<int:doc_id>", methods=["GET"])
@verify_auth(permission_needed = ["doctor_appointment_availability"])
def get_doctor_appointment_availability(doc_id):
    date = datetime.strptime(request.json["APNT_DATE"], "%d/%m/%Y").date()
    doctor = doctor_details_query.get_records_by_id(doc_id)
    response_json=[]
    if doctor:
        doc_availability_list = appointments.availibility_list(doc_id, date)
        if doc_availability_list:
            availibality_json=[]
            for row in doc_availability_list:
                availability_data={
                    "Start Time":row[0].strftime('%H:%M'),
                    "End Time":row[1].strftime('%H:%M')
                }
                availibality_json.append(availability_data)
            doctor_data = {
                "Doctor ID": doctor.DOC_UNIQ_ID,
                "Doctor Name": doctor.DOC_FNAME + " " + doctor.DOC_LNAME,
                "Date": date.strftime('%d/%m/%Y'),
                "Availability": availibality_json
            }
            response_json.append(doctor_data)
            app_logger.info("records fetched successfully")
            return make_response(response_json, 200)
        app_logger.info("doctor not available") 
        return make_response({"Message":"Doctor not available."}, 200)
    app_logger.info("invalid ID") 
    return make_response({"Message":"Invalid ID"}, 400)
