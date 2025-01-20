from src.core.models import equestrian
from src.core.models import teams

def create_horses():
    """
    Create a new horse.
    """

    horse1 = equestrian.create_horse(
        nombre="John",
        fecha_nacimiento="2020-01-01",
        sexo="M",
        raza="Arabe",
        pelaje="Blanco",
        compra_donacion="donacion",
        fecha_ingreso="2022-07-01",
        sede_asignada="CASJ",
        tipo_de_JyA_asignado="equitacion"
    )
    horse2 = equestrian.create_horse(
        nombre="Jane",
        fecha_nacimiento="2012-01-01",
        sexo="F",
        raza="Arabe",
        pelaje="Blanco",
        compra_donacion="compra",
        fecha_ingreso="2021-04-01",
        sede_asignada="CASJ",
        tipo_de_JyA_asignado="hipoterapia"
    )
    employee1 = teams.search_by_dni(96186620)
    equestrian.asign_employee(
        horse1,[employee1]
    )
    equestrian.asign_employee(
        horse2,[employee1]
    )