"""Manager Details Table in DB"""
from src.main import db

class ManagerDetails(db.Model):
    __tablename__ = "manager_details"
    
    MNGR_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    MNGR_FNAME = db.Column(db.String(250), nullable=False)
    MNGR_LNAME = db.Column(db.String(250), nullable=False)
    MNGR_YOE = db.Column(db.Integer, nullable=False)
    MNGR_CELL = db.Column(db.String(250), unique=True, nullable=False)
    MNGR_ALTR_CELL = db.Column(db.String(250))
    MNGR_EMAIL = db.Column(db.String(250), unique=True, nullable=False)
    MNGR_PASSWORD = db.Column(db.String(250), unique=True, nullable=False)
    MNGR_PASSWORD_SALT = db.Column(db.String(250), unique=True, nullable=False)
    MNGR_ROLE = db.Column(db.String(250), nullable=False)
    MNGR_GENDER = db.Column(db.String(250), nullable=False)
    MNGR_ADDRESS = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"{self.MNGR_FNAME} {self.MNGR_LNAME}"
