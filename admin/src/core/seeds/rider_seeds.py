from src.core.models import riders
from src.core.database import db
from src.core.models import teams
from src.core.models import equestrian


def create_riders():
    # Create and add Situacion_Previsional instances
    situacion1 = riders.situacion_previsional_create(
        obra_social="Obra Social A",
        numero_afiliado=123456,
        tiene_curatela=False,
    )
    situacion2 = riders.situacion_previsional_create(
        obra_social="Obra Social B",
        numero_afiliado=654321,
        tiene_curatela=True,
        observaciones="Requiere seguimiento"
    )

    # Create and add InstitucionEscolar instances
    institucion1 = riders.institucion_escolar_create(
        nombre="Instituto Educativo A",
        direccion="Calle Falsa 123",
        telefono=1234567890,
        grado_actual="Primero",
        observaciones="Ninguna"
    )
    institucion2 = riders.institucion_escolar_create(
        nombre="Instituto Educativo B",
        direccion="Avenida Siempre Viva 456",
        telefono=9876543210,
        grado_actual="Segundo",
        observaciones="Falta documentación"
    )

    # Create and add TrabajoInstitucional instances
    terapeuta1 = teams.search_by_dni(4)
    conductor1 = teams.search_by_dni(3)
    auxiliar1 = teams.search_by_dni(5)
    caballo1 = equestrian.search_by_id(1)
    trabajo1 = riders.trabajo_institucional_create(
        tipo_trabajo="hipoterapia",
        condicion="regular",
        sede="CASJ",
        dia="Lunes",
        profesor_terapeuta_id=4,
        profesor_terapeuta=terapeuta1,
        conductor_caballo_id=3,
        conductor_caballo=conductor1,
        auxiliar_pista_id=5,
        auxiliar_pista=auxiliar1,
        caballo_id=1,
        caballo=caballo1

    )
    terapeuta2 = teams.search_by_dni(4)
    conductor2 = teams.search_by_dni(3)
    auxiliar2 = teams.search_by_dni(5)
    caballo2 = equestrian.search_by_id(2)
    trabajo2 = riders.trabajo_institucional_create(
        tipo_trabajo="deporte_adaptado",
        condicion="de_baja",
        sede="HLP",
        dia="Miércoles",
        profesor_terapeuta_id=4,
        profesor_terapeuta=terapeuta2,
        conductor_caballo_id=3,
        conductor_caballo=conductor2,
        auxiliar_pista_id=5,
        auxiliar_pista=auxiliar2,
        caballo_id=2,
        caballo=caballo2
    )

    # Create and add Equitador instances
    equitador1 = riders.rider_create(
        nombre="Juan",
        apellido="Pérez",
        dni=12345678,
        fecha_nacimiento="2011-05-01",
        lugar_nacimiento="Ciudad A",
        domicilio_actual="Calle Falsa 123",
        telefono=1234567890,
        numero_emergencia=9876543210,
        nombre_emergencia="María Pérez",
        becado=True,
        porcentaje_beca=100,
        observaciones="Ninguna",
        certificado_discapacidad=True,
        diagnostico_discapacidad="otro",
        otro_diagnostico="Trastorno físico",
        tipo_discapacidad="Motora",
        recibe_asignacion=True,
        tipo_asignacion="Asignación universal por hijo con discapacidad, Asignación universal por hijo",
        recibe_pension=True,
        tipo_pension="provincial",
        situacion_previsional_id=1,
        situacion_previsional=situacion1,
        institucion_escolar_id=1,
        institucion_escolar=institucion1,
        profesionales="Maria Garcia",
        trabajo_institucional=trabajo1,
        trabajo_institucional_id=1
    )

    equitador2 = riders.rider_create(
        nombre="Ana",
        apellido="Gómez",
        dni=87654321,
        fecha_nacimiento="2013-08-15",
        lugar_nacimiento="Ciudad B",
        domicilio_actual="Avenida Siempre Viva 456",
        telefono=2345678901,
        numero_emergencia=1098765432,
        nombre_emergencia="José Gómez",
        becado=False,
        porcentaje_beca=None,
        observaciones="En tratamiento",
        certificado_discapacidad=True,
        diagnostico_discapacidad="trastorno_alimentario",
        tipo_discapacidad="Motora, Sensorial",
        recibe_asignacion=False,
        tipo_asignacion=None,
        recibe_pension=False,
        tipo_pension=None,
        situacion_previsional_id=2,
        situacion_previsional=situacion2,
        institucion_escolar=institucion2,
        institucion_escolar_id=2,
        profesionales="Carlos López",
        trabajo_institucional=trabajo2,
        trabajo_institucional_id=2
    )
    familiarResponsable1 = riders.familiar_responsable_create(
        parentesco="Madre",
        nombre="Ana",
        apellido="Pérez",
        dni=123,
        domicilio_actual="Calle Falsa 123",
        celular_actual=987654321,
        email="ana.perez@example.com",
        nivel_escolaridad="terciario",
        actividad_ocupacion="Enfermera",
        equitador_dni=12345678,
        equitador=equitador1
    ),
    familiarResponsable2 = riders.familiar_responsable_create(
        parentesco="Padre",
        nombre="Juan",
        apellido="Gómez",
        dni=456,
        domicilio_actual="Avenida Siempre Viva 456",
        celular_actual=123456789,
        email="juan.gomez@example.com",
        nivel_escolaridad="universitario",
        actividad_ocupacion="Ingeniero",
        equitador_dni=87654321,
        equitador=equitador2
    ),
    familiarResponsable3 = riders.familiar_responsable_create(
        parentesco="Hermano",
        nombre="Luis",
        apellido="Fernández",
        dni=789,
        domicilio_actual="Calle Verde 789",
        celular_actual=987123456,
        email="luis.fernandez@example.com",
        nivel_escolaridad="secundario",
        actividad_ocupacion="Estudiante",
        equitador_dni=87654321,
        equitador=equitador2
    )
