"""App Receptionist Functionality Router """
from flask import Blueprint, request, make_response
from src.app.database.receptionist_queries.details import receptionist_details_query
from src.app.utils.validation.receptionist_validation import receptionist_validator
from src.app.utils.security.encryption import hashing
from src.app.utils.authorisation.access_control import verify_auth
from src.main import app_logger
from src.app.utils.celery_tasks.email_tasks import send_email_task

receptionist = Blueprint('receptionist', __name__)

@receptionist.route("/", methods=["GET"])
@verify_auth(permission_needed = ["get_receptionists"])
def get_receptionists():
    all_receptionist = receptionist_details_query.get_records()
    response_json=[]
    if all_receptionist:
        for row in all_receptionist:
            receptionist_data={
                "ID":row.REC_UNIQ_ID,
                "First Name":row.REC_FNAME,
                "Last Name":row.REC_LNAME,
                "Email":row.REC_EMAIL,
                "Phone":row.REC_CELL,
                "Alter Phone":row.REC_ALTR_CELL,
                "Gender":row.REC_GENDER,
                "Address":row.REC_ADDRESS,
                "City":row.REC_CITY,
                "State":row.REC_STATE,
                "Is Admin":row.Is_Admin,
            }
            response_json.append(receptionist_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("no records found") 
    return make_response({"Message":"No records found"}, 200)
    

@receptionist.route("/<int:rec_id>", methods=["GET"])
@verify_auth(permission_needed = ["get_receptionists","get_receptionist_by_id"])
def get_receptionist(rec_id):
    all_receptionist = receptionist_details_query.get_records_by_id(rec_id)
    response_json=[]
    if all_receptionist:
        receptionist_data={
            "First Name":all_receptionist.REC_FNAME,
            "Last Name":all_receptionist.REC_LNAME,
            "Email":all_receptionist.REC_EMAIL,
            "Phone":all_receptionist.REC_CELL,
            "Alter Phone":all_receptionist.REC_ALTR_CELL,
            "Gender":all_receptionist.REC_GENDER,
            "Address":all_receptionist.REC_ADDRESS,
            "City":all_receptionist.REC_CITY,
            "State":all_receptionist.REC_STATE,
            "Is Admin":all_receptionist.Is_Admin,
        }
        response_json.append(receptionist_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("invalid ID")
    return make_response({"Message":"Invalid ID"}, 404)


@receptionist.route("/add", methods=["POST"])
@verify_auth(permission_needed = ["create_receptionist"])
def create_receptionist():
    data = request.json
    if not receptionist_validator.data_validator_create(data):
        status_code = 400
        response_message = {"Message":"Invalid Data"}
        app_logger.info("Invalid request data")
    elif receptionist_details_query.check_data(data):
        status_code = 400
        response_message = {"Message":"Receptionist user already exists."}
        app_logger.error("Receptionist user already exists.")
    else:
        salt = hashing.create_salt()
        data["REC_PASSWORD"] = hashing.create_password(data["REC_PASSWORD"], salt)
        receptionist_details_query.create_record(data, salt)
        email_context = {"first_name":data["REC_FNAME"], \
            "subject":"Registration Successful", \
            "message":"You are successfuly registered as a receptionist in our system."}
        send_email_task.delay("notification_email.html", email_context, [data["REC_EMAIL"]])
        status_code = 200
        response_message = {"Message":"Record created successfully!"}
        app_logger.info("record created successfully")
    return make_response(response_message, status_code)
    
    
@receptionist.route("/update/<int:rec_id>", methods=["PUT"])
@verify_auth(permission_needed = ["update_receptionist","update_self"])
def update_receptionist(rec_id):
    new_data = request.json
    new_data = receptionist_validator.data_eliminate_password(new_data)
    rec_data_temp = receptionist_details_query.get_records_by_id(rec_id)
    if rec_data_temp:
        rec_data_temp2 = rec_data_temp.__dict__
        rec_data = rec_data_temp2.copy()
        del rec_data["_sa_instance_state"]
        rec_data.update(new_data)
        if not receptionist_validator.data_validator_update(new_data):
            status_code = 400
            response_message = {"Message":"Invalid Data"}
            app_logger.info("Invalid request data")
        elif receptionist_details_query.check_data_by_id(rec_data, rec_id):
            status_code = 400
            response_message = {"Message":"Receptionist user already exists."}
            app_logger.error("Receptionist user already exists.")
        else:
            receptionist_details_query.update_record(rec_id, new_data)
            email_context = {"first_name":rec_data["REC_FNAME"], \
                "subject":"User Details Updated", \
                "message":"Your details are successfuly updated in our system."}
            send_email_task.delay("notification_email.html", email_context, [rec_data["REC_EMAIL"]])
            status_code = 200
            response_message = {"Message":"Record updated successfully!"}
            app_logger.info("record updated successfully")
    else:
        status_code = 404
        response_message = {"Message":"Invalid ID"}
        app_logger.error("Invalid ID")
    return make_response(response_message, status_code)

    
@receptionist.route("/delete/<int:rec_id>", methods=["DELETE"])
@verify_auth(permission_needed = ["delete_receptionist"])
def delete_receptionist(rec_id):
    result = receptionist_details_query.delete_record(rec_id)
    if result:
        status_code = 200
        response_message = {"Message":"Record deleted successfully!"}
        app_logger.info("record deleted successfully")
    else:
        status_code = 400
        response_message = {"Message":"Invalid ID"}
        app_logger.info("Invalid ID")
    return make_response(response_message, status_code)
