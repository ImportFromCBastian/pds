from sqlalchemy import null
from src.core.database import db
from datetime import datetime
import enum


class EstadoType(enum.Enum):
    Borrador = "Borrador"
    Publicado = "Publicado"
    Archivado = "Archivado"


class Contenido(db.Model):
    """
      Modelo de la tabla Contenido
    """
    __tablename__ = "Contenido"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    copete = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    estado = db.Column(db.Enum(EstadoType), nullable=False)
    fecha_publicacion = db.Column(db.DateTime, nullable=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, onupdate=datetime.now, nullable=True)
    autor_email = db.Column(db.String(100), db.ForeignKey(
        'Usuario.email'), nullable=False)
    autor = db.relationship("Usuario", lazy="joined")

    def __repr__(self):
        return (
            f"titulo: {self.titulo}, "
            f"copete: {self.copete}, "
            f"contenido: {self.contenido}, "
            f"estado: {self.estado}, "
            f"fecha_publicacion: {self.fecha_publicacion}, "
            f"autor_mail: {self.autor_email}, "
            f"inserted_at: {self.inserted_at}, "
            f"updated_at: {self.updated_at}"
        )
