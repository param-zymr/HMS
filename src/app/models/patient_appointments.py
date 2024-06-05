"""Patient Appointments Table in DB"""
from src.main import db

class PatientAppointments(db.Model):
    __tablename__ = "patient_appointments"
    
    APNT_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    APNT_PAT_ID = db.Column(db.Integer, db.ForeignKey('patient_details.PAT_UNIQ_ID', \
        ondelete="CASCADE"), nullable=False)
    APNT_DOC_ID = db.Column(db.Integer, db.ForeignKey('doctor_details.DOC_UNIQ_ID', \
        ondelete="CASCADE"), nullable=False)
    APNT_REC_ID = db.Column(db.Integer, db.ForeignKey('receptionist_details.REC_UNIQ_ID', \
        ondelete='SET NULL'))
    APNT_TITLE = db.Column(db.String(250), nullable=False)
    APNT_DETAILS = db.Column(db.Text, nullable=False)
    APNT_DATE = db.Column(db.Date, nullable=False)
    APNT_START_TIME = db.Column(db.Time, nullable=False)
    APNT_END_TIME = db.Column(db.Time, nullable=False)
    APNT_REG_DATE = db.Column(db.Date, nullable=False)
    APNT_REG_TIME = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"{self.APNT_DATE} {self.APNT_TITLE}"
    