from src.core.database import db
from datetime import datetime
import enum


class ConditionType(enum.Enum):
    voluntario = "Voluntario"
    personal_rentado = "Personal Rentado"


class ProfessionType(enum.Enum):
    psicologo = "Psicólogo/a"
    psicomotricista = "Psicomotricista"
    medico = "Médico/a"
    kinesiologo = "Kinesiólogo/a"
    terapista_ocupacional = "Terapista Ocupacional"
    psicopedagogo = "Psicopedagogo/a"
    docente = "Docente"
    profesor = "Profesor"
    fonoaudiologo = "Fonoaudiólogo/a"
    veterinario = "Veterinario/a"
    otro = "Otro"


class PositionType(enum.Enum):
    administrativo = "Administrativo/a"
    terapeuta = "Terapeuta"
    conductor = "Conductor"
    auxiliar_pista = "Auxiliar de pista"
    herrero = "Herrero"
    veterinario = "Veterinario"
    entrenador_caballos = "Entrenador de Caballos"
    domador = "Domador"
    profesor_equitacion = "Profesor de Equitación"
    docente_capacitacion = "Docente de Capacitación"
    auxiliar_mantenimiento = "Auxiliar de mantenimiento"
    otro = "Otro"


class Empleado(db.Model):
    """
    A member of the team for the system.
    """

    __tablename__ = "Empleado"
    dni = db.Column(db.BigInteger(), nullable=False, unique=True, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    domicilio = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.BigInteger(), nullable=False)
    profesion = db.Column(db.Enum(ProfessionType), nullable=False)
    puesto_laboral = db.Column(db.Enum(PositionType), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_cese = db.Column(db.DateTime, nullable=True)
    numero_afiliado = db.Column(db.BigInteger(), unique=True)
    condicion = db.Column(db.Enum(ConditionType), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, default=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user = db.relationship("Usuario", back_populates="empleado")
    numero_emergencia = db.Column(db.BigInteger(), nullable=False)
    nombre_emergencia = db.Column(db.String(100), nullable=False)
    copia_dni = db.Column(db.String(25), nullable=True)
    titulo = db.Column(db.String(25), nullable=True)
    curriculum_vitae = db.Column(db.String(25), nullable=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    cobros = db.relationship("Cobro", back_populates="empleado")

    def __repr__(self):
        return (
            f"<Empleado dni='{self.dni}', "
            f"nombre='{self.nombre}', "
            f"apellido='{self.apellido}', "
            f"profesion='{self.profesion}', "
            f"puesto_laboral='{self.puesto_laboral}', "
            f"telefono='{self.telefono}', "
            f"domicilio='{self.domicilio}', "
            f"localidad='{self.localidad}', "
            f"fecha_inicio='{self.fecha_inicio}', "
            f"fecha_cese='{self.fecha_cese}', "
            f"numero_afiliado='{self.numero_afiliado}', "
            f"condicion='{self.condicion}', "
            f"activo='{self.activo}', "
            f"email='{self.email}', "
            f"numero_emergencia='{self.numero_emergencia}', "
            f"nombre_emergencia='{self.nombre_emergencia}'> "
        )
