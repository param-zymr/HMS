"""
Flask App Creation as a Function
"""
import logging
from logging.config import dictConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.app.config import app_settings

#logging config
dictConfig(app_settings.LOG_DICT_CONFIG)
app_logger = logging.getLogger('default')
app_logger.info("logger configured")

db = SQLAlchemy()
app_logger.info("db connection created")

def create_app():
    # init app
    app = Flask(__name__, template_folder="./app/templates")
    # configuration
    app.config.from_object(app_settings)
    app.json.sort_keys = False
    app.json.default = str
    app_logger.info("flask app configured")
    db.init_app(app)
    app_logger.info("db connection configured")

    with app.app_context():
        from src.app.routes.user_authorisation import user_authorisation
        from src.app.routes.manager_crud import manager
        from src.app.routes.doctor_crud import doctor
        from src.app.routes.patient_crud import patient
        from src.app.routes.receptionist_crud import receptionist
        from src.app.routes.patient_appointments_crud import patient_appointments
        from src.app.routes.patient_appointments_history import patient_appointments_history
        from src.app.routes.doctor_schedule import doctor_schedule
        from src.app.routes.doctor_appointments_list import doctor_appointments_list
        from src.app.routes.doctor_appointment_availability import doctor_appointment_availability
        #register blueprints
        app.register_blueprint(user_authorisation, url_prefix='/api/v1/user_authorisation')
        app.register_blueprint(manager, url_prefix='/api/v1/managers')
        app.register_blueprint(doctor, url_prefix='/api/v1/doctors')
        app.register_blueprint(patient, url_prefix='/api/v1/patients')
        app.register_blueprint(receptionist, url_prefix='/api/v1/receptionists')
        app.register_blueprint(patient_appointments, \
            url_prefix='/api/v1/patient_appointments')
        app.register_blueprint(patient_appointments_history, \
            url_prefix='/api/v1/patient_appointments_history')
        app.register_blueprint(doctor_schedule, url_prefix='/api/v1/doctor_schedule')
        app.register_blueprint(doctor_appointments_list, \
            url_prefix='/api/v1/doctor_appointments_list')
        app.register_blueprint(doctor_appointment_availability, \
            url_prefix='/api/v1/doctor_appointment_availability')
        db.create_all()
        app_logger.info("tables in db created")
    return app
