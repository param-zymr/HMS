"""User Catagories Roles Mapper Table in DB"""
from src.main import db

class UcatRoles(db.Model):
    __tablename__ = "ucat_roles"
    
    UCROLE_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    UCAT_ID = db.Column(db.Integer, db.ForeignKey('user_catagories.UCAT_UNIQ_ID', ondelete='SET NULL'))
    ROLE_ID = db.Column(db.Integer, db.ForeignKey('roles.ROLE_UNIQ_ID', ondelete='SET NULL'))

    def __repr__(self):
        return f"{self.UCROLE_UNIQ_ID} {self.UCAT_ID} - {self.ROLE_ID}"
