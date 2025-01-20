from src.core.database import db

from src.core.models.users_module.role_permission import role_permission


class Rol(db.Model):
    """Role of the user int the system"""

    __tablename__ = "Rol"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    usuarios = db.relationship("Usuario", back_populates="rol", lazy=True)
    permisos = db.relationship(
        "Permiso",
        secondary=role_permission,
        lazy="subquery",
        backref=db.backref("roles", lazy=True),
    )

    @classmethod
    def create_role(cls, **kwargs):
        """
        Add a role by sending the parameters and types below:
            id: Integer (id of the role)
            nombre: String (name of the role)

        Optionally:
            permisos: List of Permission IDs to associate with the role
            modulo: String (name of the module where that role has that permission)
        """
        from src.core.models import Permiso

        permisos = kwargs.pop("permisos", None)
        role = cls(**kwargs)

        if permisos:
            permisos_obj = Permiso.query.filter(Permiso.id.in_(permisos)).all()
            role.permisos.extend(permisos_obj)

        db.session.add(role)
        db.session.commit()

        return role

    @classmethod
    def get_roles(cls):
        """Returns all the roles in the system"""
        return cls.query.all()

    @classmethod
    def get_role_permissions_by_name(cls, role_name: str):
        """Returns all the permissions of a role"""
        role = cls.query.filter_by(nombre=role_name).first()
        return role.permisos
