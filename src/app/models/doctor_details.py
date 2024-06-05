"""Doctor Details Table in DB"""
from src.main import db

class DoctorDetails(db.Model):
    __tablename__ = "doctor_details"
    
    DOC_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    DOC_FNAME = db.Column(db.String(250), nullable=False)
    DOC_LNAME = db.Column(db.String(250), nullable=False)
    DOC_LICENCE_NUMBER = db.Column(db.String(250), unique=True, nullable=False)
    DOC_YOE = db.Column(db.Integer, nullable=False)
    DOC_CELL = db.Column(db.String(250), unique=True, nullable=False)
    DOC_ALTR_CELL = db.Column(db.String(250))
    DOC_EMAIL = db.Column(db.String(250), unique=True, nullable=False)
    DOC_PASSWORD = db.Column(db.String(250), unique=True, nullable=False)
    DOC_PASSWORD_SALT = db.Column(db.String(250), unique=True, nullable=False)
    DOC_ROLE = db.Column(db.String(250), nullable=False)
    DOC_SPECIALITY = db.Column(db.String(250), nullable=False)
    DOC_GENDER = db.Column(db.String(250), nullable=False)
    DOC_ADDRESS = db.Column(db.Text, nullable=False)
    
    #Relationships
    DOC_PATIENT_DETAILS = db.relationship('PatientDetails', backref='doctor_details')
    DOC_APPOINTMENT_DETAILS = db.relationship('PatientAppointments', \
        backref='doctor_details', cascade="all, delete")
    DOC_SCHEDULE = db.relationship('DoctorSchedule', \
        backref='doctor_details', cascade="all, delete")

    def __repr__(self):
        return f"{self.DOC_FNAME} {self.DOC_LNAME}"
