"""App Doctor Functionality Router """
from flask import Blueprint, request, make_response
from src.app.database.doctor_queries.details import doctor_details_query
from src.app.utils.validation.doctor_validation import doctor_validator
from src.app.utils.authorisation.access_control import verify_auth
from src.app.utils.security.encryption import hashing
from src.main import app_logger
from src.app.utils.celery_tasks.email_tasks import send_email_task

doctor = Blueprint('doctor', __name__)

@doctor.route("/", methods=["GET"])
@verify_auth(permission_needed = ["get_doctors"])
def get_doctors():
    all_doctors = doctor_details_query.get_records()
    response_json=[]
    if all_doctors:
        for row in all_doctors:
            doctor_data={
                "ID":row.DOC_UNIQ_ID,
                "First Name":row.DOC_FNAME,
                "Last Name":row.DOC_LNAME,
                "Licence Number":row.DOC_LICENCE_NUMBER,
                "Years of Experience":row.DOC_YOE,
                "Role":row.DOC_ROLE,
                "Email":row.DOC_EMAIL,
                "Phone":row.DOC_CELL,
                "Alter Phone":row.DOC_ALTR_CELL,
                "Speciality":row.DOC_SPECIALITY,
                "Gender":row.DOC_GENDER,
                "Address":row.DOC_ADDRESS
            }
            response_json.append(doctor_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("no records found") 
    return make_response({"Message":"No records found"}, 200)
    

@doctor.route("/<int:doc_id>", methods=["GET"])
@verify_auth(permission_needed = ["get_doctors","get_doctor_by_id"])
def get_doctor(doc_id):
    all_doctor = doctor_details_query.get_records_by_id(doc_id)
    response_json=[]
    if all_doctor:
        doctor_data={
            "First Name":all_doctor.DOC_FNAME,
            "Last Name":all_doctor.DOC_LNAME,
            "Licence Number":all_doctor.DOC_LICENCE_NUMBER,
            "Years of Experience":all_doctor.DOC_YOE,
            "Role":all_doctor.DOC_ROLE,
            "Email":all_doctor.DOC_EMAIL,
            "Phone":all_doctor.DOC_CELL,
            "Alter Phone":all_doctor.DOC_ALTR_CELL,
            "Speciality":all_doctor.DOC_SPECIALITY,
            "Gender":all_doctor.DOC_GENDER,
            "Address":all_doctor.DOC_ADDRESS
        }
        response_json.append(doctor_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("invalid ID")
    return make_response({"Message":"Invalid ID"}, 404)


@doctor.route("/add", methods=["POST"])
@verify_auth(permission_needed = ["create_doctor"])
def create_doctor():
    data = request.json
    if not doctor_validator.data_validator_create(data):
        status_code = 400
        response_message = {"Message":"Invalid Data"}
        app_logger.info("Invalid request data")
    elif doctor_details_query.check_data(data):
        status_code = 400
        response_message = {"Message":"Doctor user already exists."}
        app_logger.error("Doctor user already exists.")
    else:
        salt = hashing.create_salt()
        data["DOC_PASSWORD"] = hashing.create_password(data["DOC_PASSWORD"], salt)
        doctor_details_query.create_record(data, salt)
        email_context = {"first_name":data["DOC_FNAME"], \
            "subject":"Registration Successful", \
            "message":"You are successfuly registered as a doctor in our system."}
        send_email_task.delay("notification_email.html", email_context, [data["DOC_EMAIL"]])
        status_code = 200
        response_message = {"Message":"Record created successfully!"}
        app_logger.info("record created successfully")
    return make_response(response_message, status_code)
    
    
@doctor.route("/update/<int:doc_id>", methods=["PUT"])
@verify_auth(permission_needed = ["update_doctor","update_self"])
def update_doctor(doc_id):
    new_data = request.json
    new_data = doctor_validator.data_eliminate_password(new_data)
    doc_data_temp = doctor_details_query.get_records_by_id(doc_id)
    if doc_data_temp:
        doc_data_temp2 = doc_data_temp.__dict__
        doc_data = doc_data_temp2.copy()
        del doc_data["_sa_instance_state"]
        doc_data.update(new_data)
        if not doctor_validator.data_validator_update(new_data):
            status_code = 400
            response_message = {"Message":"Invalid Data"}
            app_logger.info("Invalid request data")
        elif doctor_details_query.check_data_by_id(doc_data, doc_id):
            status_code = 400
            response_message = {"Message":"Doctor user already exists."}
            app_logger.error("Doctor user already exists.")
        else:
            doctor_details_query.update_record(doc_id, new_data)
            email_context = {"first_name":doc_data["DOC_FNAME"], \
                "subject":"User Details Updated", \
                "message":"Your details are successfuly updated in our system."}
            send_email_task.delay("notification_email.html", email_context, [doc_data["DOC_EMAIL"]])
            status_code = 200
            response_message = {"Message":"Record updated successfully!"}
            app_logger.info("record updated successfully")
    else:
        status_code = 404
        response_message = {"Message":"Invalid ID"}
        app_logger.error("Invalid ID")
    return make_response(response_message, status_code)

    
@doctor.route("/delete/<int:doc_id>", methods=["DELETE"])
@verify_auth(permission_needed = ["delete_doctor"])
def delete_doctor(doc_id):
    result = doctor_details_query.delete_record(doc_id)
    if result:
        status_code = 200
        response_message = {"Message":"Record deleted successfully!"}
        app_logger.info("record deleted successfully")
    else:
        status_code = 400
        response_message = {"Message":"Invalid ID"}
        app_logger.info("Invalid ID")
    return make_response(response_message, status_code)
