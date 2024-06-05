"""User Catagories Table in DB"""
from src.main import db

class UserCatagories(db.Model):
    __tablename__ = "user_catagories"
    
    UCAT_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    USER_CATAGORY = db.Column(db.String(250), nullable=False)

    #Relationships
    UCAT_ROLES = db.relationship('UcatRoles', backref='user_catagories')
    UCAT_PERMISSIONS = db.relationship('UcatPermissions', backref='user_catagories')

    def __repr__(self):
        return f"{self.UCAT_UNIQ_ID} {self.USER_CATAGORY}"
