"""Permissions Table in DB"""
from src.main import db

class Permissions(db.Model):
    __tablename__ = "permissions"
    
    PAR_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    PERMISSION = db.Column(db.String, nullable=False)

    #Relationships
    PAR_ROLES = db.relationship('RolePermissions', backref='permissions')
    PAR_USERCATS = db.relationship('UcatPermissions', backref='permissions')

    def __repr__(self):
        return f"{self.PAR_UNIQ_ID} {self.PERMISSION}"
