"""Doctor Schedules Table in DB"""
from src.main import db

class DoctorSchedule(db.Model):
    __tablename__ = "doctor_schedule"
    
    SHIFT_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    SHIFT_DOC_ID = db.Column(
        db.Integer, db.ForeignKey('doctor_details.DOC_UNIQ_ID', \
            ondelete="CASCADE"), nullable=False)
    SHIFT_DATE = db.Column(db.Date, nullable=False)
    SHIFT_TYPE = db.Column(db.String(250), nullable=False)
    SHIFT_START_TIME = db.Column(db.Time, nullable=False)
    SHIFT_END_TIME = db.Column(db.Time, nullable=False)
    SHIFT_IS_AVAILABLE = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"{self.SHIFT_UNIQ_ID} {self.SHIFT_DOC_ID}"
