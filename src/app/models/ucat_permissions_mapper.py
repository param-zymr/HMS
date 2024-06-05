"""User Catagories Permissions Mapper Table in DB"""
from src.main import db

class UcatPermissions(db.Model):
    __tablename__ = "ucat_permissions"
    
    UCPAR_UNIQ_ID = db.Column(db.Integer, primary_key=True)
    UCAT_ID = db.Column(db.Integer, db.ForeignKey('user_catagories.UCAT_UNIQ_ID', ondelete='SET NULL'))
    PAR_ID = db.Column(db.Integer, db.ForeignKey('permissions.PAR_UNIQ_ID', ondelete='SET NULL'))

    def __repr__(self):
        return f"{self.UCPAR_UNIQ_ID} {self.UCAT_ID} - {self.PAR_ID}"
