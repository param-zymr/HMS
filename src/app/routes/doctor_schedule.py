"""App Patient Functionality Router """
from flask import Blueprint, request, make_response
from src.app.database.doctor_queries.schedule import doctor_schedule_query
from src.app.utils.authorisation.access_control import verify_auth
from src.main import app_logger

doctor_schedule = Blueprint('doctor_schedule', __name__)

@doctor_schedule.route("/", methods=["GET"])
@verify_auth(permission_needed = ["get_doctor_schedule"])
def get_doctor_schedules():
    all_schedule = doctor_schedule_query.get_records()
    response_json=[]
    if all_schedule:
        for row in all_schedule:
            schedule_data={
                "ID":row.SHIFT_UNIQ_ID,
                "Doctor ID":row.SHIFT_DOC_ID,
                "Shift Date":row.SHIFT_DATE.strftime('%d/%m/%Y'),
                "Shift Type":row.SHIFT_TYPE,
                "Shift Start Time":row.SHIFT_START_TIME.strftime('%H:%M'),
                "Shift End Time":row.SHIFT_END_TIME.strftime('%H:%M'),
                "Is Doctor Available":row.SHIFT_IS_AVAILABLE
            }
            response_json.append(schedule_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("no records found") 
    return make_response({"Message":"No records found"}, 200)
    

@doctor_schedule.route("/<int:shift_id>", methods=["GET"])
@verify_auth(permission_needed = ["get_doctor_schedule","get_doctor_schedule_by_id"])
def get_doctor_schedule(shift_id):
    all_schedule = doctor_schedule_query.get_records_by_id(shift_id)
    response_json=[]
    if all_schedule:
        schedule_data={
            "ID":all_schedule.SHIFT_UNIQ_ID,
            "Doctor ID":all_schedule.SHIFT_DOC_ID,
            "Shift Date":all_schedule.SHIFT_DATE.strftime('%d/%m/%Y'),
            "Shift Type":all_schedule.SHIFT_TYPE,
            "Shift Start Time":all_schedule.SHIFT_START_TIME.strftime('%H:%M'),
            "Shift End Time":all_schedule.SHIFT_END_TIME.strftime('%H:%M'),
            "Is Doctor Available":all_schedule.SHIFT_IS_AVAILABLE
        }
        response_json.append(schedule_data)
        app_logger.info("records fetched successfully")
        return make_response(response_json, 200)
    app_logger.info("invalid ID")
    return make_response({"Message":"Invalid ID"}, 404)


@doctor_schedule.route("/add", methods=["POST"])
@verify_auth(permission_needed = ["create_doctor_schedule"])
def create_doctor_schedule():
    data = request.json
    check_data = doctor_schedule_query.check_data(data)
    validate_shift_data = doctor_schedule_query.validate_shift_data(data)
    check_foreign_keys = doctor_schedule_query.check_foreign_keys(data)
    if check_data:
        status_code = 400
        response_message = {"Message":"Shift already exists"}
        app_logger.error("shift already exists")
    else:
        if validate_shift_data and check_foreign_keys:
            doctor_schedule_query.create_record(data)
            status_code = 200
            response_message = {"Message":"Record created successfully!"}
            app_logger.info("record created successfully")
        else:
            status_code = 400
            response_message = {"Message":"Schedule data is not valid"}
            app_logger.error("Invalid schedule data")
    return make_response(response_message, status_code)
    
    
@doctor_schedule.route("/update/<int:shift_id>", methods=["PUT"])
@verify_auth(permission_needed = ["update_doctor_schedule"])
def update_doctor_schedule(shift_id):
    new_data = request.json
    schedule_data_temp = doctor_schedule_query.get_records_by_id(shift_id)
    if schedule_data_temp:
        schedule_data = schedule_data_temp.__dict__
        schedule_data.update(new_data)
        check_data = doctor_schedule_query.check_data_by_id(schedule_data, shift_id)
        validate_shift_data = doctor_schedule_query.validate_shift_data(schedule_data)
        check_foreign_keys = doctor_schedule_query.check_foreign_keys(schedule_data)
        if check_data:
            status_code = 400
            response_message = {"Message":"Shift already exists"}
            app_logger.error("Shift already exists")
        else:
            if validate_shift_data and check_foreign_keys:
                doctor_schedule_query.update_record(shift_id, new_data)
                status_code = 200
                response_message = {"Message":"Record updated successfully!"}
                app_logger.info("record updated successfully")
            else:
                status_code = 400
                response_message = {"Message":"Schedule data is not valid"}
                app_logger.error("Invalid schedule data")
    else:
        status_code = 404
        response_message = {"Message":"Invalid ID"}
        app_logger.error("Invalid ID")
    return make_response(response_message, status_code)


@doctor_schedule.route("/delete/<int:shift_id>", methods=["DELETE"])
@verify_auth(permission_needed = ["delete_doctor_schedule"])
def delete_doctor_schedule(shift_id):
    result = doctor_schedule_query.delete_record(shift_id)
    if result:
        status_code = 200
        response_message = {"Message":"Record deleted successfully!"}
        app_logger.info("record deleted successfully")
    else:
        status_code = 400
        response_message = {"Message":"Invalid ID"}
        app_logger.info("Invalid ID")
    return make_response(response_message, status_code)
