"""Roles Table in DB"""
from src.main import db

class Roles(db.Model):
    __tablename__ = "roles"
    
    ROLE_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    ROLE = db.Column(db.String(250), nullable=False)

    #Relationships
    ROLE_USERCATS = db.relationship('UcatRoles', backref='roles')
    ROLE_PERMISSIONS = db.relationship('RolePermissions', backref='roles')

    def __repr__(self):
        return f"{self.ROLE_UNIQ_ID} {self.ROLE}"
