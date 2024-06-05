"""Role Permissions Mapper Table in DB"""
from src.main import db

class RolePermissions(db.Model):
    __tablename__ = "role_permissions"
    
    RPAR_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    ROLE_ID = db.Column(db.Integer, db.ForeignKey('roles.ROLE_UNIQ_ID', ondelete='SET NULL'))
    PAR_ID = db.Column(db.Integer, db.ForeignKey('permissions.PAR_UNIQ_ID', ondelete='SET NULL'))

    def __repr__(self):
        return f"{self.RPAR_UNIQ_ID} {self.ROLE_ID} - {self.PAR_ID}"
