from src.core.database import db
from datetime import datetime
from sqlalchemy.orm import joinedload


class Usuario(db.Model):
    """An user of the system with a role"""

    __tablename__ = "Usuario"
    email = db.Column(db.String(100), nullable=False,
                      unique=True, primary_key=True)
    contrasenia = db.Column(db.String, nullable=False)
    alias = db.Column(db.String(100), nullable=False)
    bloqueado = db.Column(db.Boolean, nullable=True, default=False)
    borrado = db.Column(db.Boolean, nullable=True, default=False)
    creado_en = db.Column(db.DateTime, default=datetime.now())
    modificado_en = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now()
    )
    system_admin = db.Column(db.Boolean, nullable=True, default=False)
    dni_empleado = db.Column(
        db.BigInteger(), db.ForeignKey("Empleado.dni"), nullable=True
    )
    empleado = db.relationship("Empleado", back_populates="user")
    rol_id = db.Column(db.Integer, db.ForeignKey("Rol.id"), nullable=False)
    rol = db.relationship("Rol", back_populates="usuarios")

    @classmethod
    def is_system_admin(cls, user_email: str) -> bool:
        """Return 'True' if the email sent is from a system admin, 'False' otherwhise"""
        usuario = (
            cls.query.filter_by(borrado=False).filter(
                cls.email == user_email).first()
        )
        if usuario:
            return usuario.system_admin
        return False

    @classmethod
    def get_user(cls, email: str):
        """Search the user for the email sended"""
        return cls.query.filter_by(borrado=False).filter(cls.email == email).first()

    @classmethod
    def create_user(cls, **kwargs):
        """
        Add a user by sending the parameters and types below:
            email: String
            contrasenia: String
            alias: String
            rol_id: Integer (id of the user role)
        Optionaly, send the following if you want to set any of the attributes below (by default, they are False):
            system_admin: Boolean (is an admin)
            bloqueado: Boolean
        Finally, returns the user
        """
        user = cls(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, **kwargs):
        """Updates the user with the given data"""
        changed = {}
        for attribute, value in kwargs.items():
            match attribute:
                case "alias":
                    if value != "" and value != self.alias:
                        self.alias = value
                        changed[attribute] = value
                case "rol_id":
                    self.rol_id = value
                    changed[attribute] = value
        db.session.commit()

        return changed

    @classmethod
    def delete_user(cls, email: str) -> bool:
        """Deletes the user sended by email, and returns if it was deleted or not"""
        user = cls.get_user(email)

        if user:
            user.borrado = True
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def togle_status(cls, email: str):
        """Togles the user status sended by email, and returns the user if he exists"""
        user = cls.get_user(email)

        if user:
            user.bloqueado = not user.bloqueado
            db.session.commit()

            return user

        else:
            return None

    @classmethod
    def has_permission(cls, email: str, permission: str) -> bool:
        """Returns true if the user sended by email has the pèrmission sended, false otherwise"""
        from src.core.models import Rol

        user = (
            cls.query.filter_by(borrado=False)
            .filter_by(email=email)
            .options(joinedload(cls.rol).joinedload(Rol.permisos))
            .first()
        )

        if user:
            for permiso in user.rol.permisos:
                if permiso.nombre == permission:
                    return True

        return False

    @classmethod
    def get_user_rol_by_email(cls, email: str):
        """Returns the user role by email"""
        user = cls.query.filter_by(email=email).first()
        if user:
            return user.rol.nombre
        return None
