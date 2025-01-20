from src.core.models import teams


# el nombre de los campos que son enums estan ligados a los atributos de las clase enums (ProfessionType, PositionType, ConditionType)


def create_employee():
    """
    Create a new team member.
    """
    employee1 = teams.team_create(
        dni=96186620,
        nombre="John",
        apellido="Doe",
        profesion="docente",
        domicilio="Calle Falsa 123",
        localidad="Springfield",
        telefono=123456789,
        puesto_laboral="herrero",
        fecha_inicio="2021-02-01",
        condicion="voluntario",
        activo=True,
        numero_afiliado=19192,
        email="generalLee12@gmail.com",
        numero_emergencia=123456789,
        nombre_emergencia="Daisy Duke",
    )

    employee2 = teams.team_create(
        dni=2,
        nombre="Jane",
        apellido="Doe",
        profesion="profesor",
        domicilio="Calle Falsa 123",
        localidad="Springfield",
        telefono=123456789,
        puesto_laboral="veterinario",
        fecha_inicio="2021-01-01",
        condicion="voluntario",
        email="starsky12@gmail.com",
        numero_afiliado=88888,
        activo=True,
        numero_emergencia=123456789,
        nombre_emergencia="Daisy Duke",
    )

    employee3 = teams.team_create(
        dni=3,
        nombre="Lucas",
        apellido="Smith",
        profesion="otro",
        domicilio="Avenida Siempre Viva 742",
        localidad="Springfield",
        telefono=987654321,
        puesto_laboral="auxiliar_pista",
        fecha_inicio="2022-05-01",
        condicion="voluntario",
        email="lucas.smith@example.com",
        numero_afiliado=99999,
        activo=True,
        numero_emergencia=987654321,
        nombre_emergencia="Maggie Smith",
    )

    employee4 = teams.team_create(
        dni=4,
        nombre="Maria",
        apellido="Garcia",
        profesion="otro",
        domicilio="Calle Verde 456",
        localidad="Springfield",
        telefono=654321789,
        puesto_laboral="terapeuta",
        fecha_inicio="2020-03-15",
        condicion="voluntario",
        email="maria.garcia@example.com",
        numero_afiliado=77777,
        activo=True,
        numero_emergencia=654321789,
        nombre_emergencia="John Doe",
    )

    employee5 = teams.team_create(
        dni=5,
        nombre="Carlos",
        apellido="López",
        profesion="otro",
        domicilio="Calle Azul 789",
        localidad="Springfield",
        telefono=321654987,
        puesto_laboral="conductor",
        fecha_inicio="2019-08-20",
        condicion="voluntario",
        email="carlos.lopez@example.com",
        numero_afiliado=66666,
        activo=True,
        numero_emergencia=321654987,
        nombre_emergencia="Anna López",
    )
