"""Patient Details Table in DB"""
from src.main import db

class PatientDetails(db.Model):
    __tablename__ = "patient_details"
    
    PAT_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    PAT_FNAME = db.Column(db.String(250), nullable=False)
    PAT_LNAME = db.Column(db.String(250), nullable=False)
    PAT_MNAME = db.Column(db.String(250), nullable=False)
    PAT_ADHAR = db.Column(db.String(250), unique=True, nullable=False)
    PAT_DOB = db.Column(db.Date, nullable=False)
    PAT_GENDER = db.Column(db.String(250), nullable=False)
    PAT_CELL = db.Column(db.String(250), unique=True, nullable=False)
    PAT_ALTR_CELL = db.Column(db.String(250))
    PAT_EMAIL = db.Column(db.String(250), unique=True, nullable=False)
    PAT_PASSWORD = db.Column(db.String(250), unique=True, nullable=False)
    PAT_PASSWORD_SALT = db.Column(db.String(250), unique=True, nullable=False)
    PAT_ROLE = db.Column(db.String(250), nullable=False)
    PAT_ADDRESS = db.Column(db.Text, nullable=False)
    PAT_CITY = db.Column(db.String(250), nullable=False)
    PAT_STATE = db.Column(db.String(250), nullable=False)
    PAT_ZIP = db.Column(db.String(250), nullable=False)
    PAT_COUNTRY = db.Column(db.String(250), nullable=False)
    PAT_FAMILY_DOC = db.Column(db.String(250))
    PAT_FAMILY_DOC_CELL = db.Column(db.String(250))
    PAT_DOC_ASSIGNED = db.Column(
        db.Integer, db.ForeignKey('doctor_details.DOC_UNIQ_ID', ondelete='SET NULL'))
    
    #Relationships
    PAT_APPOINTMENT_DETAILS = db.relationship('PatientAppointments', \
        backref='patient_details', cascade="all, delete")

    def __repr__(self):
        return f"{self.PAT_FNAME} {self.PAT_LNAME}"
