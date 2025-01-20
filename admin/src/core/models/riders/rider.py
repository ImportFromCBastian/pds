from src.core.database import db
from datetime import datetime
import enum
from sqlalchemy.orm import relationship


class SituacionPrevisional(db.Model):
    __tablename__ = "Situacion_Previsional"
    id = db.Column(db.Integer, primary_key=True)
    obra_social = db.Column(db.String(100), nullable=False)
    numero_afiliado = db.Column(db.BigInteger(), nullable=False)
    tiene_curatela = db.Column(db.Boolean, nullable=False)
    observaciones = db.Column(db.String(100), nullable=True)


class InstitucionEscolar(db.Model):
    __tablename__ = "Institucion_Escolar"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.BigInteger(), nullable=False)
    grado_actual = db.Column(db.String(50), nullable=False)
    observaciones = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return (f"<InstitucionEscolar(\n"
                f"  id={self.id},\n"
                f"  nombre='{self.nombre}',\n"
                f"  direccion='{self.direccion}',\n"
                f"  telefono={self.telefono},\n"
                f"  grado_actual='{self.grado_actual}',\n"
                f"  observaciones='{self.observaciones}'\n"
                f">)")


class Sede(enum.Enum):
    CASJ = "CASJ"
    HLP = "HLP"
    otros = "Otro"


class PropuestaTrabajo(enum.Enum):
    hipoterapia = "Hipoterapia"
    monta_terapeutica = "Monta terapéutica"
    deporte_adaptado = "Deporte ecuestre adaptado"
    actividades_recreativas = "Actividades recreativas"
    equitacion = "Equitación"


class Condition(enum.Enum):
    regular = "Regular"
    de_baja = "De baja"


class TrabajoInstitucional(db.Model):
    __tablename__ = "Trabajo_Institucional"
    id = db.Column(db.Integer, primary_key=True)
    tipo_trabajo = db.Column(db.Enum(PropuestaTrabajo), nullable=False)
    condicion = db.Column(db.Enum(Condition), nullable=False)
    sede = db.Column(db.Enum(Sede), nullable=False)
    dia = db.Column(db.String(100), nullable=False)
    profesor_terapeuta_id = db.Column(db.BigInteger, db.ForeignKey(
        'Empleado.dni'), nullable=False)
    profesor_terapeuta = db.relationship(
        'Empleado', foreign_keys=[profesor_terapeuta_id])
    conductor_caballo_id = db.Column(db.BigInteger, db.ForeignKey(
        'Empleado.dni'), nullable=False)
    conductor_caballo = db.relationship(
        'Empleado', foreign_keys=[conductor_caballo_id])
    caballo_id = db.Column(db.Integer, db.ForeignKey(
        'Caballo.id'), nullable=False)
    caballo = db.relationship('Caballo', foreign_keys=[caballo_id])
    auxiliar_pista_id = db.Column(db.BigInteger, db.ForeignKey(
        'Empleado.dni'), nullable=False)
    auxiliar_pista = db.relationship(
        'Empleado', foreign_keys=[auxiliar_pista_id])

    def __repr__(self):
        return (f"<TrabajoInstitucional(\n"
                f"  id={self.id},\n"
                f"  tipo_trabajo={self.tipo_trabajo},\n"
                f"  condicion={self.condicion},\n"
                f"  sede={self.sede},\n"
                f"  dia='{self.dia}',\n"
                f"  profesor_terapeuta={self.profesor_terapeuta},\n"
                f"  conductor_caballo={self.conductor_caballo},\n"
                f"  auxiliar_pista={self.auxiliar_pista}\n"
                f">)")


class PensionType(enum.Enum):
    provincial = "Provincial"
    nacional = "Nacional"


class DiagnosisType(enum.Enum):
    ecne = "ECNE"
    lesion_post_traumatica = "Lesión post-traumática"
    mielomeningocele = "Mielomeningocele"
    esclerosis_multiples = "Esclerosis Múltiple"
    escoliosis_leve = "Escoliosis Leve"
    secuelas_acv = "Secuelas de ACV"
    discapacidad_intelectual = "Discapacidad Intelectual"
    trastorno_espectro_autista = "Trastorno del Espectro Autista"
    trastorno_aprendizaje = "Trastorno del Aprendizaje"
    tda_h = "Trastorno por Déficit de Atención/Hiperactividad"
    trastorno_comunicacion = "Trastorno de la Comunicación"
    trastorno_ansiedad = "Trastorno de Ansiedad"
    sindrome_down = "Síndrome de Down"
    retraso_madurativo = "Retraso Madurativo"
    psicosis = "Psicosis"
    trastorno_conducta = "Trastorno de Conducta"
    trastornos_animo_afectivos = "Trastornos del ánimo y afectivos"
    trastorno_alimentario = "Trastorno Alimentario"
    otro = "OTRO"


class Equitador(db.Model):
    __tablename__ = "Equitador"
    """ datos personales """
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.BigInteger(), nullable=False,
                    unique=True, primary_key=True)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    lugar_nacimiento = db.Column(db.String(100), nullable=False)
    """datos de contacto"""
    domicilio_actual = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.BigInteger(), nullable=False)
    numero_emergencia = db.Column(db.BigInteger(), nullable=False)
    nombre_emergencia = db.Column(db.String(100), nullable=False)
    becado = db.Column(db.Boolean, nullable=False)
    porcentaje_beca = db.Column(db.Integer(), nullable=True)
    observaciones = db.Column(db.String(100), nullable=True)
    """ discapacidad """
    certificado_discapacidad = db.Column(db.Boolean, nullable=False)
    diagnostico_discapacidad = db.Column(db.Enum(DiagnosisType), nullable=True)
    otro_diagnostico = db.Column(db.String(100), nullable=True, default=None)
    tipo_discapacidad = db.Column(db.String(100), nullable=False)
    """ beneficios y asignaciones """
    recibe_asignacion = db.Column(db.Boolean, nullable=False)
    tipo_asignacion = db.Column(db.String(100), nullable=True)
    recibe_pension = db.Column(db.Boolean, nullable=False)
    tipo_pension = db.Column(db.Enum(PensionType), nullable=True)
    profesionales = db.Column(db.String(100), nullable=False)
    """ inserción y modificación """
    inserted_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    borrado = db.Column(db.Boolean, nullable=False, default=False)
    """ relación con otras tablas """
    situacion_previsional_id = db.Column(
        db.Integer, db.ForeignKey('Situacion_Previsional.id'), nullable=False)
    institucion_escolar_id = db.Column(
        db.Integer, db.ForeignKey('Institucion_Escolar.id'), nullable=False)
    trabajo_institucional_id = db.Column(
        db.Integer, db.ForeignKey('Trabajo_Institucional.id'), nullable=False)
    situacion_previsional = relationship(
        SituacionPrevisional, backref="equitador", lazy="joined")
    institucion_escolar = relationship(
        InstitucionEscolar, backref="equitador", lazy="joined")
    trabajo_institucional = relationship(
        TrabajoInstitucional, backref="equitador", lazy="joined")
    cobros = db.relationship("Cobro", back_populates="equitador")

    def __repr__(self):
        return (f"<Equitador(\n"
                f"  nombre='{self.nombre}',\n"
                f"  apellido='{self.apellido}',\n"
                f"  dni={self.dni},\n"
                f"  fecha_nacimiento={self.fecha_nacimiento},\n"
                f"  lugar_nacimiento='{self.lugar_nacimiento}',\n"
                f"  domicilio_actual='{self.domicilio_actual}',\n"
                f"  telefono={self.telefono},\n"
                f"  numero_emergencia={self.numero_emergencia},\n"
                f"  nombre_emergencia='{self.nombre_emergencia}',\n"
                f"  becado={self.becado},\n"
                f"  porcentaje_beca={self.porcentaje_beca},\n"
                f"  observaciones='{self.observaciones}',\n"
                f"  certificado_discapacidad={
                    self.certificado_discapacidad},\n"
                f"  diagnostico_discapacidad='{
                    self.diagnostico_discapacidad}',\n"
                f"  tipo_discapacidad={self.tipo_discapacidad},\n"
                f"  recibe_asignacion={self.recibe_asignacion},\n"
                f"  recibe_pension={self.recibe_pension},\n"
                f"  tipo_pension={self.tipo_pension},\n"
                f"  inserted_at={self.inserted_at},\n"
                f"  updated_at={self.updated_at},\n"
                f"  situacion_previsional={self.situacion_previsional},\n"
                f"  institucion_escolar_id={self.institucion_escolar_id},\n"
                f"  profesionales='{self.profesionales}',\n"
                f"  trabajo_institucional_id={self.trabajo_institucional_id}\n"
                f">)")

    @classmethod
    def togle_pay_status(cls, dni: str):
        """Togles the rider pays status sended by his DNI, and returns the user if he exists"""
        # Primero busco al equitador
        rider = cls.query.filter_by(dni=dni).first()

        # Si existe el equitador, le cambio el estado
        if rider:
            rider.tiene_deudas = not rider.tiene_deudas
            db.session.commit()

            return rider

        else:
            return None


class NivelEscolaridad(enum.Enum):
    primario = "Primario"
    secundario = "Secundario"
    terciario = "Terciario"
    universitario = "Universitario"


class FamiliarResponsable(db.Model):
    __tablename__ = "Familiar_Responsable"
    parentesco = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.BigInteger(), nullable=False, primary_key=True)
    domicilio_actual = db.Column(db.String(255), nullable=False)
    celular_actual = db.Column(db.BigInteger(), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    nivel_escolaridad = db.Column(db.Enum(NivelEscolaridad), nullable=False)
    actividad_ocupacion = db.Column(db.String(100), nullable=False)
    # Relación con Equitador
    equitador_dni = db.Column(db.BigInteger, db.ForeignKey(
        'Equitador.dni'), nullable=False)
    equitador = relationship(
        Equitador, backref="familiares", lazy="joined")

    def __repr__(self):
        return (f"<FamiliarResponsable(\n"
                f"  parentesco='{self.parentesco}',\n"
                f"  nombre='{self.nombre}',\n"
                f"  apellido='{self.apellido}',\n"
                f"  dni={self.dni},\n"
                f"  domicilio_actual='{self.domicilio_actual}',\n"
                f"  celular_actual={self.celular_actual},\n"
                f"  email='{self.email}',\n"
                f"  nivel_escolaridad='{self.nivel_escolaridad}',\n"
                f"  actividad_ocupacion='{self.actividad_ocupacion}'\n"
                f">)")


class TipoArchivo(enum.Enum):
    entrevista = "Entrevista"
    evaluacion = "Evaluación"
    planificaciones = "Planificaciones"
    evolucion = "Evolución"
    cronica = "Crónica"
    documental = "Documental"


class ArchivosEquitador(db.Model):
    __tablename__ = "Archivos_Equitador"
    id = db.Column(db.Integer, primary_key=True)
    tipo_archivo = db.Column(db.Enum(TipoArchivo), nullable=False)
    equitador_dni = db.Column(db.BigInteger, db.ForeignKey(
        'Equitador.dni'), nullable=False)
    archivo = db.Column(db.String(255), nullable=False)
    inserted_at = db.Column(db.DateTime, default=datetime.now())
    is_link = db.Column(db.Boolean, nullable=False, default=False)
