from src.core.database import db

class UserProvisorio(db.Model):
    """Usuario provisorio del sistema"""
    __tablename__ = "User_Provisorio"
    email = db.Column(db.String, nullable=False,primary_key=True)

    def repr(self):
        return f"<UserProvisorio {self.email}>"


