"""App Patient Appointment CRUD Functionality Router """
from datetime import datetime
from flask import Blueprint, request, make_response
from src.app.database.patient_queries.appointments import patient_appointments_query
from src.app.core.patient import appointments
from src.app.utils.authorisation.access_control import verify_auth
from src.main import app_logger

patient_appointments = Blueprint('patient_appointments', __name__)

@patient_appointments.route("/", methods=["GET"])
@verify_auth(permission_needed = ["get_appointments"])
def get_patient_appointments():
    all_appointments = patient_appointments_query.get_records()
    response_json=[]
    if all_appointments:
        for row in all_appointments:
            appointments_data={
                "Appintment ID":row.APNT_UNIQ_ID,
                "Patient ID":row.APNT_PAT_ID,
                "Doctor ID":row.APNT_DOC_ID,
                "Title":row.APNT_TITLE,
                "Details":row.APNT_DETAILS,
                "Date":row.APNT_DATE.strftime('%d/%m/%Y'),
                "Start Time":row.APNT_START_TIME.strftime('%H:%M'),
                "End Time":row.APNT_END_TIME.strftime('%H:%M'),
                "Receptionist ID":row.APNT_REC_ID,
                "Registration Date":row.APNT_REG_DATE.strftime('%d/%m/%Y'),
                "Registration Time":row.APNT_REG_TIME.strftime('%H:%M:%S')
            }
            response_json.append(appointments_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("no records found") 
    return make_response({"Message":"No records found"}, 200)
    

@patient_appointments.route("/<int:apnt_id>", methods=["GET"])
@verify_auth(permission_needed = ["get_appointments","get_appointment_by_id"])
def get_patient_appointment(apnt_id):
    all_appointments = patient_appointments_query.get_records_by_id(apnt_id)
    response_json=[]
    if all_appointments:
        appointments_data={
            "Appintment ID":all_appointments.APNT_UNIQ_ID,
            "Patient ID":all_appointments.APNT_PAT_ID,
            "Doctor ID":all_appointments.APNT_DOC_ID,
            "Title":all_appointments.APNT_TITLE,
            "Details":all_appointments.APNT_DETAILS,
            "Date":all_appointments.APNT_DATE.strftime('%d/%m/%Y'),
            "Start Time":all_appointments.APNT_START_TIME.strftime('%H:%M'),
            "End Time":all_appointments.APNT_END_TIME.strftime('%H:%M'),
            "Receptionist ID":all_appointments.APNT_REC_ID,
            "Registration Date":all_appointments.APNT_REG_DATE.strftime('%d/%m/%Y'),
            "Registration Time":all_appointments.APNT_REG_TIME.strftime('%H:%M:%S')
        }
        response_json.append(appointments_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("invalid ID")
    return make_response({"Message":"Invalid ID"}, 404)


@patient_appointments.route("/add", methods=["POST"])
@verify_auth(permission_needed = ["create_appointment"])
def create_patient_appointment():
    data = request.json
    current_datetime = datetime.now()
    data["APNT_REG_DATE"] = datetime.strftime(current_datetime,'%Y/%m/%d')
    data["APNT_REG_TIME"] = datetime.strftime(current_datetime,'%H:%M:%S')
    check_data = patient_appointments_query.check_data(data)
    check_foreign_keys = patient_appointments_query.check_foreign_keys(data)
    if check_data and check_foreign_keys:
        appointment_availibility = appointments.check_availibility(data)
        if appointment_availibility:
            patient_appointments_query.create_record(data)
            status_code = 200
            response_message = {"Message":"Record created successfully!"}
            app_logger.info("record created successfully")
        else:
            status_code = 400
            response_message = {"Message":"Appointment time slot not available."}
            app_logger.error("Appointment time slot not available")
    else:
        status_code = 400
        response_message = {"Message":"Appointment data is not valid"}
        app_logger.error("Invalid appointment data")
    return make_response(response_message, status_code)
    
    
@patient_appointments.route("/update/<int:apnt_id>", methods=["PUT"])
@verify_auth(permission_needed = ["update_appointment"])
def update_patient_appointment(apnt_id):
    new_data = request.json
    apnt_data_temp = patient_appointments_query.get_records_by_id(apnt_id)
    if apnt_data_temp:
        apnt_data = apnt_data_temp.__dict__
        apnt_data.update(new_data)
        check_data = patient_appointments_query.check_data(apnt_data)
        check_foreign_keys = patient_appointments_query.check_foreign_keys(apnt_data)
        if check_data and check_foreign_keys:
            appointment_availibility = appointments.check_availibility(apnt_data, apnt_id)
            if appointment_availibility:
                patient_appointments_query.update_record(apnt_id, new_data)
                status_code = 200
                response_message = {"Message":"Record update successfully!"}
                app_logger.info("record updated successfully")
            else:
                status_code = 400
                response_message = {"Message":"Appointment time slot not available."}
                app_logger.error("Appointment time slot not available")
        else:
            status_code = 400
            response_message = {"Message":"Appointment data is not valid"}
            app_logger.error("Invalid appointment data")
    else:
        status_code = 404
        response_message = {"Message":"Invalid ID"}
        app_logger.error("Invalid ID")
    return make_response(response_message, status_code)

    
@patient_appointments.route("/delete/<int:apnt_id>", methods=["DELETE"])
@verify_auth(permission_needed = ["delete_appointment"])
def delete_patient_appointment(apnt_id):
    result = patient_appointments_query.delete_record(apnt_id)
    if result:
        status_code = 200
        response_message = {"Message":"Record deleted successfully!"}
        app_logger.info("record deleted successfully")
    else:
        status_code = 400
        response_message = {"Message":"Invalid ID"}
        app_logger.info("Invalid ID")
    return make_response(response_message, status_code)
