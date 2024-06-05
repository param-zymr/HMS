"""Receptionist Details Table in DB"""
from src.main import db

class ReceptionistDetails(db.Model):
    __tablename__ = "receptionist_details"
    
    REC_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    REC_FNAME = db.Column(db.String(250), nullable=False)
    REC_LNAME = db.Column(db.String(250), nullable=False)
    REC_EMAIL = db.Column(db.String(250), unique=True, nullable=False)
    REC_PASSWORD = db.Column(db.String(250), unique=True, nullable=False)
    REC_PASSWORD_SALT = db.Column(db.String(250), unique=True, nullable=False)
    REC_ROLE = db.Column(db.String(250), nullable=False)
    REC_CELL = db.Column(db.String(250), unique=True, nullable=False)
    REC_ALTR_CELL = db.Column(db.String(250))
    REC_GENDER = db.Column(db.String(250), nullable=False)
    REC_ADDRESS = db.Column(db.Text, nullable=False)
    REC_CITY = db.Column(db.String(250), nullable=False)
    REC_STATE = db.Column(db.String(250), nullable=False)
    Is_Admin = db.Column(db.Boolean, nullable=False)
    
    #Relationships
    REC_APPOINTMENT_DETAILS = db.relationship('PatientAppointments', \
        backref='receptionist_details')

    def __repr__(self):
        return f"{self.REC_FNAME} {self.REC_LNAME}"
