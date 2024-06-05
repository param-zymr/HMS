"""App Manager Functionality Router """
from flask import Blueprint, request, make_response
from src.app.database.manager_queries.details import manager_details_query
from src.app.utils.validation.manager_validation import manager_validator
from src.app.utils.authorisation.access_control import verify_auth
from src.app.utils.security.encryption import hashing
from src.main import app_logger
from src.app.utils.celery_tasks.email_tasks import send_email_task

manager = Blueprint('manager', __name__)

@manager.route("/", methods=["GET"])
@verify_auth(permission_needed = ["get_managers"])
def get_managers():
    all_managers = manager_details_query.get_records()
    response_json=[]
    if all_managers:
        for row in all_managers:
            manager_data={
                "ID":row.MNGR_UNIQ_ID,
                "First Name":row.MNGR_FNAME,
                "Last Name":row.MNGR_LNAME,
                "Role":row.MNGR_ROLE,
                "Email":row.MNGR_EMAIL,
                "Phone":row.MNGR_CELL,
                "Alter Phone":row.MNGR_ALTR_CELL,
                "Years of Experiance":row.MNGR_YOE,
                "Gender":row.MNGR_GENDER,
                "Address":row.MNGR_ADDRESS
            }
            response_json.append(manager_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("no records found") 
    return make_response({"Message":"No records found"}, 200)
    

@manager.route("/<int:mngr_id>", methods=["GET"])
@verify_auth(permission_needed = ["get_managers","get_manager_by_id"])
def get_manager(mngr_id):
    all_manager = manager_details_query.get_records_by_id(mngr_id)
    response_json=[]
    if all_manager:
        manager_data={
            "ID":all_manager.MNGR_UNIQ_ID,
            "First Name":all_manager.MNGR_FNAME,
            "Last Name":all_manager.MNGR_LNAME,
            "Role":all_manager.MNGR_ROLE,
            "Email":all_manager.MNGR_EMAIL,
            "Phone":all_manager.MNGR_CELL,
            "Alter Phone":all_manager.MNGR_ALTR_CELL,
            "Years of Experiance":all_manager.MNGR_YOE,
            "Gender":all_manager.MNGR_GENDER,
            "Address":all_manager.MNGR_ADDRESS
        }
        response_json.append(manager_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("invalid ID")
    return make_response({"Message":"Invalid ID"}, 404)


@manager.route("/add", methods=["POST"])
@verify_auth(permission_needed = ["create_manager"])
def create_manager():
    data = request.json
    if not manager_validator.data_validator_create(data):
        status_code = 400
        response_message = {"Message":"Invalid Data"}
        app_logger.info("Invalid request data")
    elif manager_details_query.check_data(data):
        status_code = 400
        response_message = {"Message":"Manager user already exists."}
        app_logger.error("Manager user already exists.")
    else:
        salt = hashing.create_salt()
        data["MNGR_PASSWORD"] = hashing.create_password(data["MNGR_PASSWORD"], salt)
        manager_details_query.create_record(data, salt)
        email_context = {"first_name":data["MNGR_FNAME"], \
            "subject":"Registration Successful", \
            "message":"You are successfuly registered as a manager in our system."}
        send_email_task.delay("notification_email.html", email_context, [data["MNGR_EMAIL"]])
        status_code = 200
        response_message = {"Message":"Record created successfully!"}
        app_logger.info("record created successfully")
    return make_response(response_message, status_code)
    
    
@manager.route("/update/<int:mngr_id>", methods=["PUT"])
@verify_auth(permission_needed = ["update_manager","update_self"])
def update_manager(mngr_id):
    new_data = request.json
    new_data = manager_validator.data_eliminate_password(new_data)
    mngr_data_temp = manager_details_query.get_records_by_id(mngr_id)
    if mngr_data_temp:
        mngr_data_temp2 = mngr_data_temp.__dict__
        mngr_data = mngr_data_temp2.copy()
        del mngr_data["_sa_instance_state"]
        mngr_data.update(new_data)
        if not manager_validator.data_validator_update(new_data):
            status_code = 400
            response_message = {"Message":"Invalid Data"}
            app_logger.info("Invalid request data")
        elif manager_details_query.check_data_by_id(mngr_data, mngr_id):
            status_code = 400
            response_message = {"Message":"Manager user already exists."}
            app_logger.error("manager user already exists.")
        else:
            manager_details_query.update_record(mngr_id, new_data)
            email_context = {"first_name":mngr_data["MNGR_FNAME"], \
                "subject":"User Details Updated", \
                "message":"Your details are successfuly updated in our system."}
            send_email_task.delay("notification_email.html", email_context, [mngr_data["MNGR_EMAIL"]])
            status_code = 200
            response_message = {"Message":"Record updated successfully!"}
            app_logger.info("record updated successfully")
    else:
        status_code = 404
        response_message = {"Message":"Invalid ID"}
        app_logger.error("Invalid ID")
    return make_response(response_message, status_code)

    
@manager.route("/delete/<int:mngr_id>", methods=["DELETE"])
@verify_auth(permission_needed = ["delete_manager"])
def delete_manager(mngr_id):
    result = manager_details_query.delete_record(mngr_id)
    if result:
        status_code = 200
        response_message = {"Message":"Record deleted successfully!"}
        app_logger.info("record deleted successfully")
    else:
        status_code = 400
        response_message = {"Message":"Invalid ID"}
        app_logger.info("Invalid ID")
    return make_response(response_message, status_code)
