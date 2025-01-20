from datetime import datetime
from src.core.database import db
import enum

class JyAType(enum.Enum):
    hipoterapia = "Hipoterapia"
    monta_terapeutica = "Monta Terapéutica"
    deporte_ecuestre_adaptado = "Deporte Ecuestre Adaptado"
    actividades_recreativas = "Actividades Recreativas"
    equitacion = "Equitación"

class CompraDonacion(enum.Enum):
    compra = "Compra"
    donacion = "Donación"

class Sede(enum.Enum):
    CASJ = "CASJ"
    HLP = "HLP"
    otros = "Otro"

class Sexo(enum.Enum):
    M = "Macho"
    F = "Hembra"

class TipoDocumento(enum.Enum):
    ficha_general = "Ficha General"
    planificacion_entrenamiento = "Planificación de Entrenamiento"
    informe_evolucion = "Informe de Evolución"
    carga_imagenes = "Carga de Imágenes"
    registro_veterinario = "Registro Veterinario"

Caballo_Empleado = db.Table(
    "Caballo_Empleado",
    db.Column("idCaballo",db.Integer, db.ForeignKey("Caballo.id"), primary_key=True),
    db.Column("dniEmpleado",db.BigInteger(), db.ForeignKey("Empleado.dni"), primary_key=True)
) 


class DocumentoCaballo(db.Model):
    __tablename__ = "Documento_Caballo"
    id = db.Column(db.Integer, primary_key=True)
    tipo_documento = db.Column(db.Enum(TipoDocumento), nullable=False)
    id_caballo = db.Column(db.BigInteger, db.ForeignKey(
        'Caballo.id'), nullable=False)
    documento = db.Column(db.String(255), nullable=False)
    es_link = db.Column(db.Boolean, nullable=False, default=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now())

class Caballo(db.Model):
    """A horse that is part of the equestrian center"""

    __tablename__ = "Caballo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    sexo = db.Column(db.Enum(Sexo), nullable=False)
    raza = db.Column(db.String(100), nullable=False)
    pelaje = db.Column(db.String(100), nullable=False)
    compra_donacion = db.Column(db.Enum(CompraDonacion), nullable=False)
    fecha_ingreso = db.Column(db.DateTime, nullable=False)
    sede_asignada = db.Column(db.Enum(Sede), nullable=False)
    tipo_de_JyA_asignado = db.Column(db.Enum(JyAType), nullable=False)
    empleados = db.relationship("Empleado",secondary=Caballo_Empleado)
    eliminado = db.Column(db.Boolean, default=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    def __repr__(self):
        return (
            f"<Caballo id='{self.id}', "
            f"nombre='{self.nombre}', "
            f"fecha_nacimiento='{self.fecha_nacimiento}', "
            f"sexo='{self.sexo}', "
            f"raza='{self.raza}', "
            f"pelaje='{self.pelaje}', "
            f"compra_donacion='{self.compra_donacion}', "
            f"fecha_ingreso='{self.fecha_ingreso}', "
            f"sede_asignada='{self.sede_asignada}', "
            f"tipo_de_JyA_asignado='{self.tipo_de_JyA_asignado}', "
            f"empleados='{self.empleados}', "
            f"inserted_at='{self.inserted_at}', "
            f"updated_at='{self.updated_at}'>"
        )