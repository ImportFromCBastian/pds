from src.core.database import db


class Permiso(db.Model):
    """A permission that let's a user have a determined interaction in the system"""

    __tablename__ = "Permiso"
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    nombre = db.Column(db.String, nullable=False)

    @classmethod
    def create_permission(cls, **kwargs):
        """
        Add a permission by sending the parameters and types below:
            id: Integer (id of the permission)
            nombre: String (name of the permission)
        """
        permission = cls(**kwargs)
        db.session.add(permission)
        db.session.commit()

        return permission

    @classmethod
    def search_by_prefix(cls, prefix):
        """
        Search a permission by a prefix and return a list of ids
        """
        # Fetch ids and unpack the single value tuple
        return [
            result[0]
            for result in cls.query.with_entities(cls.id)
            .filter(cls.nombre.like(f"{prefix}%"))
            .all()
        ]
