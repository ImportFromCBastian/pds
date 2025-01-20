
from sqlalchemy import func
from sqlalchemy import String, cast
from sqlalchemy.orm import joinedload, aliased
from src.core.models.riders.rider import Equitador, SituacionPrevisional, FamiliarResponsable, InstitucionEscolar, TrabajoInstitucional, ArchivosEquitador
from src.core.database import commit_db, delete_from_db
from src.core.models.teams.employee import Empleado
from src.core.models.equestrian.Horse import Caballo
from src.core.models.riders.handlers.update import update_rider, update_academic, update_previtional_situation, update_work
from sqlalchemy.orm import joinedload
from src.core.models.charges_module.charge import Cobro
from datetime import datetime
from sqlalchemy import and_


def riders_index():
    """
    List all the riders.
    """
    riders = Equitador.query.all()
    return riders


def rider_index(page=1, per_page=5, dni=None, nombre=None, apellido=None, profesional=None, sort_field='dni', sort_order='asc'):
    """
    List all the riders that are not marked as deleted with pagination and filtering.
    """
    query = Equitador.query.filter_by(borrado=False)

    if dni:
        query = query.filter(cast(Equitador.dni, String).ilike(f"%{dni}%"))
    if nombre:
        query = query.filter(Equitador.nombre.ilike(f"%{nombre}%"))
    if apellido:
        query = query.filter(Equitador.apellido.ilike(f"%{apellido}%"))
    if profesional:
        query = query.filter(Equitador.profesionales.ilike(f"%{profesional}%"))

    if sort_field and sort_order:
        if sort_order == 'asc':
            query = query.order_by(getattr(Equitador, sort_field).asc())
        else:
            query = query.order_by(getattr(Equitador, sort_field).desc())

    riders = query.paginate(page=page, per_page=per_page, error_out=False)
    return riders


def rider_create(**kwargs):
    """
    Create a new rider.
    """
    new_rider = Equitador(**kwargs)
    commit_db(new_rider)
    return new_rider


def familiar_responsable_create(**kwargs):
    """
    Create a new responsable family.
    """
    new_familiar_responsable = FamiliarResponsable(**kwargs)
    commit_db(new_familiar_responsable)
    return new_familiar_responsable


def institucion_escolar_create(**kwargs):
    """
    Create a new school institution.
    """
    new_institucion_escolar = InstitucionEscolar(**kwargs)
    commit_db(new_institucion_escolar)
    return new_institucion_escolar


def trabajo_institucional_create(**kwargs):
    """
    Create a new institutional work.
    """
    new_trabajo_institucional = TrabajoInstitucional(**kwargs)
    commit_db(new_trabajo_institucional)
    return new_trabajo_institucional


def situacion_previsional_create(**kwargs):
    """
    Create a new previsional situation.
    """
    new_situacion_previsional = SituacionPrevisional(**kwargs)
    commit_db(new_situacion_previsional)
    return new_situacion_previsional


def exists_rider(dni: int) -> bool:
    """
    Check if a rider with the given DNI exists.
    :return: True if the rider exists, False otherwise.
    """
    rider = Equitador.query.filter_by(dni=dni).first()
    return rider is not None


def search_by_dni(dni: int):
    """
    Search a rider by DNI and return all related data.
    """
    Empleado_profesor = aliased(Empleado)
    Empleado_conductor = aliased(Empleado)
    Empleado_auxiliar = aliased(Empleado)
    rider = (
        Equitador.query
        .options(
            joinedload(Equitador.situacion_previsional),
            joinedload(Equitador.institucion_escolar),
            joinedload(Equitador.trabajo_institucional),
            joinedload(Equitador.familiares),
        )
        .join(TrabajoInstitucional, Equitador.trabajo_institucional_id == TrabajoInstitucional.id)
        .join(Empleado_profesor, Empleado_profesor.dni == TrabajoInstitucional.profesor_terapeuta_id)
        .join(Empleado_conductor, Empleado_conductor.dni == TrabajoInstitucional.conductor_caballo_id)
        .join(Empleado_auxiliar, Empleado_auxiliar.dni == TrabajoInstitucional.auxiliar_pista_id)
        .join(Caballo, Caballo.id == TrabajoInstitucional.caballo_id)
        .filter(Equitador.dni == dni)
        .first()
    )
    return rider


def rider_update(dni: int, params):
    """
    Update a rider.
    """
    rider = search_by_dni(dni)

    update_rider(rider, params)
    commit_db(rider)
    return rider


def search_institution_by_id(institution_id: int):
    """
    Search an institution by ID.
    """
    institution = InstitucionEscolar.query.filter_by(id=institution_id).first()
    return institution


def academic_update(academic_id: int, params):
    """
    Update an institution.
    """
    academic = search_institution_by_id(academic_id)
    update_academic(academic, params)
    commit_db(academic)
    return academic


def search_previtional_situation_by_id(previtional_situation_id: int):
    """
    Search a previtionalSituation by ID.
    """
    previtionalSituation = SituacionPrevisional.query.filter_by(
        id=previtional_situation_id).first()
    return previtionalSituation


def previtionalSituation_update(previtional_situation_id: int, params):
    """
    Update a previtionalSituation
    """
    previtionalSituation = search_previtional_situation_by_id(
        previtional_situation_id)
    update_previtional_situation(previtionalSituation, params)
    commit_db(previtionalSituation)
    return previtionalSituation


def search_work_by_id(work_id: int):
    """
    Search a work by ID.
    """
    work = TrabajoInstitucional.query.filter_by(id=work_id).first()
    return work


def institutionalWork_update(work_id: int, params):
    """
    Update a work
    """
    work = search_work_by_id(work_id)
    update_work(work, params)
    commit_db(work)
    return work


def familyMember_delete(dni_familiar: int):
    """
    Delete a family member.
    """
    family_member = FamiliarResponsable.query.filter_by(
        dni=dni_familiar).first()
    if family_member:
        try:
            delete_from_db(family_member)
            return family_member
        except Exception as e:
            raise Exception(f"Error deleting family member: {str(e)}")
    else:
        raise ValueError("Family member not found.")


def upload_file(file_name: str, dni: int, tipoArchivo: str, es_link: bool = False):
    """
    Uploads a file by creating a new entry in ArchivosEquitador.
    """
    nuevo_archivo = ArchivosEquitador(
        tipo_archivo=tipoArchivo,
        equitador_dni=dni,
        archivo=f"{file_name}",
        is_link=es_link)

    commit_db(nuevo_archivo)

    return nuevo_archivo


def get_files_by_dni(dni: int):
    """
    Devuelve todos los archivos asociados a un rider por su DNI, incluyendo su tipo.
    """
    archivos = ArchivosEquitador.query.filter_by(
        equitador_dni=dni).all()
    files = []

    for archivo in archivos:
        file_data = {
            'nombre': archivo.archivo,
            'tipo_archivo': archivo.tipo_archivo,
            'fecha': archivo.inserted_at,
            'id': archivo.id,
            'is_link': archivo.is_link
        }
        files.append(file_data)

    return files


def delete_file_by_id(file_id: int):
    """
    elimina un archivo por su ID.
    """
    archivo = ArchivosEquitador.query.filter_by(id=file_id).first()
    if archivo:
        try:
            delete_from_db(archivo)
            return archivo
        except Exception as e:
            raise Exception(f"Error deleting file: {str(e)}")
    else:
        raise ValueError("File not found.")


def rider_delete(dni: int):
    """
    Delete a rider by DNI.
    """
    rider = Equitador.query.filter_by(dni=dni).first()
    if rider:
        try:
            rider.borrado = True
            commit_db(rider)
            return rider
        except Exception as e:
            raise Exception(f"Error deleting rider: {str(e)}")
    else:
        raise ValueError("Rider not found.")


def rider_charges(initial_year, final_year):
    """
    Return all riders (Equitador) with their associated charges (cobros),
    grouped by the monto (charge amount) within the specified year range.
    """

    initial_date = datetime(initial_year, 1, 1)
    final_date = datetime(final_year, 12, 31)

    riders = (
        Equitador.query
        .filter(Equitador.borrado == False)
        .join(Cobro, and_(Cobro.dni_equitador == Equitador.dni, Cobro.borrado == False))
        .filter(Cobro.fecha_pago.between(initial_date, final_date))
        .with_entities(Equitador.dni, Equitador.nombre, func.sum(Cobro.monto).label('total_monto'))
        .group_by(Equitador.dni, Equitador.nombre)
        .all()
    )
    return riders
