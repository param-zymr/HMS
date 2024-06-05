"""App Patient Functionality Router """
from datetime import datetime
from flask import Blueprint, request, make_response
from src.app.database.patient_queries.details import patient_details_query
from src.main import app_logger
from src.app.utils.validation.patient_validation import patient_validator
from src.app.utils.authorisation.access_control import verify_auth
from src.app.utils.security.encryption import hashing
from src.app.utils.celery_tasks.email_tasks import send_email_task

patient = Blueprint('patient', __name__)

@patient.route("/", methods=["GET"])
@verify_auth(permission_needed = ["get_patients"])
def get_patients():
    all_patient = patient_details_query.get_records()
    response_json=[]
    if all_patient:
        for row in all_patient:
            patient_data={
                "ID":row.PAT_UNIQ_ID,
                "First Name":row.PAT_FNAME,
                "Middle Name":row.PAT_MNAME,
                "Last Name":row.PAT_LNAME,
                "Adhaar":row.PAT_ADHAR,
                "Email":row.PAT_EMAIL,
                "Phone":row.PAT_CELL,
                "Alter Phone":row.PAT_ALTR_CELL,
                "Gender":row.PAT_GENDER,
                "Date of Birth":datetime.strftime(row.PAT_DOB,'%d/%m/%Y'),
                "Address":row.PAT_ADDRESS,
                "City":row.PAT_CITY,
                "State":row.PAT_STATE,
                "ZIP/PIN Code":row.PAT_ZIP,
                "Country":row.PAT_COUNTRY,
                "Family Doctor":row.PAT_FAMILY_DOC,
                "Family Doctor Phone":row.PAT_FAMILY_DOC_CELL,
                "Doctor Assigned":row.PAT_DOC_ASSIGNED
            }
            response_json.append(patient_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("no records found") 
    return make_response({"Message":"No records found"}, 200)
    

@patient.route("/<int:pat_id>", methods=["GET"])
@verify_auth(permission_needed = ["get_patients","get_patient_by_id"])
def get_patient(pat_id):
    all_patient = patient_details_query.get_records_by_id(pat_id)
    response_json=[]
    if all_patient:
        patient_data={
            "ID":all_patient.PAT_UNIQ_ID,
            "First Name":all_patient.PAT_FNAME,
            "Middle Name":all_patient.PAT_MNAME,
            "Last Name":all_patient.PAT_LNAME,
            "Adhaar":all_patient.PAT_ADHAR,
            "Email":all_patient.PAT_EMAIL,
            "Phone":all_patient.PAT_CELL,
            "Alter Phone":all_patient.PAT_ALTR_CELL,
            "Gender":all_patient.PAT_GENDER,
            "Date of Birth":datetime.strftime(all_patient.PAT_DOB,'%d/%m/%Y'),
            "Address":all_patient.PAT_ADDRESS,
            "City":all_patient.PAT_CITY,
            "State":all_patient.PAT_STATE,
            "ZIP/PIN Code":all_patient.PAT_ZIP,
            "Country":all_patient.PAT_COUNTRY,
            "Family Doctor":all_patient.PAT_FAMILY_DOC,
            "Family Doctor Phone":all_patient.PAT_FAMILY_DOC_CELL,
            "Doctor Assigned":all_patient.PAT_DOC_ASSIGNED
        }
        response_json.append(patient_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("invalid ID")
    return make_response({"Message":"Invalid ID"}, 404)

@patient.route("/add", methods=["POST"])
@verify_auth(permission_needed = ["create_patient"])
def create_patient():
    data = request.json
    if not (patient_validator.data_validator_create(data) and \
        patient_details_query.check_foreign_keys(data)):
        status_code = 400
        response_message = {"Message":"Invalid Data"}
        app_logger.info("Invalid request data")
    elif patient_details_query.check_data(data):
        status_code = 400
        response_message = {"Message":"Patient user already exists."}
        app_logger.error("Patient user already exists.")
    else:
        salt = hashing.create_salt()
        data["PAT_PASSWORD"] = hashing.create_password(data["PAT_PASSWORD"], salt)
        patient_details_query.create_record(data, salt)
        email_context = {"first_name":data["PAT_FNAME"], \
            "subject":"Registration Successful", \
            "message":"You are successfuly registered as a patient in our system."}
        send_email_task.delay("notification_email.html", email_context, [data["PAT_EMAIL"]])
        status_code = 200
        response_message = {"Message":"Record created successfully!"}
        app_logger.info("record created successfully")
    return make_response(response_message, status_code)
    
    
@patient.route("/update/<int:pat_id>", methods=["PUT"])
@verify_auth(permission_needed = ["update_patient","update_self"])
def update_patient(pat_id):
    new_data = request.json
    new_data = patient_validator.data_eliminate_password(new_data)
    pat_data_temp = patient_details_query.get_records_by_id(pat_id)
    if pat_data_temp:
        pat_data_temp2 = pat_data_temp.__dict__
        pat_data = pat_data_temp2.copy()
        del pat_data["_sa_instance_state"]
        pat_data.update(new_data)
        if not (patient_validator.data_validator_update(pat_data) and \
            patient_details_query.check_foreign_keys(pat_data)):
            status_code = 400
            response_message = {"Message":"Invalid Data"}
            app_logger.info("Invalid request data")
        elif patient_details_query.check_data_by_id(pat_data, pat_id):
            status_code = 400
            response_message = {"Message":"Patient user already exists."}
            app_logger.error("Patient user already exists.")
        else:
            patient_details_query.update_record(pat_id, new_data)
            email_context = {"first_name":pat_data["PAT_FNAME"], \
                "subject":"User Details Updated", \
                "message":"Your details are successfuly updated in our system."}
            send_email_task.delay("notification_email.html", email_context, [pat_data["PAT_EMAIL"]])
            status_code = 200
            response_message = {"Message":"Record updated successfully!"}
            app_logger.info("record updated successfully")
    else:
        status_code = 404
        response_message = {"Message":"Invalid ID"}
        app_logger.error("Invalid ID")
    return make_response(response_message, status_code)

    
@patient.route("/delete/<int:pat_id>", methods=["DELETE"])
@verify_auth(permission_needed = ["delete_patient"])
def delete_patient(pat_id):
    result = patient_details_query.delete_record(pat_id)
    if result:
        status_code = 200
        response_message = {"Message":"Record deleted successfully!"}
        app_logger.info("record deleted successfully")
    else:
        status_code = 400
        response_message = {"Message":"Invalid ID"}
        app_logger.info("Invalid ID")
    return make_response(response_message, status_code)
