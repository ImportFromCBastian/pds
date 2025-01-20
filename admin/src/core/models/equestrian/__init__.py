from src.core.database import commit_db,delete_from_db
from src.core.models.equestrian.Horse import Caballo,DocumentoCaballo
from src.core.models import teams
from src.core.models.equestrian.handler.update_horse import update as uphorse
from sqlalchemy import String, cast

def equestrian_index_paginated(page: int):
    """
    List the horses paginated, ordered by name descendently. Receives the page to paginated
    Returns the horses and the cant of pages
    """
    horses = Caballo.query.order_by(
        Caballo.nombre.desc()).paginate(page=page, per_page=15)
    return {"horses": horses.items, "pages":horses.pages}


def equestrian_index(page=1, per_page=5, nombre=None, tipo_de_JyA_asignado=None, sort_field='', sort_order='asc'):
    """
    List all the horses that are not marked as deleted (eliminado = false) with pagination and filtering.
    """
    query = Caballo.query.filter_by(eliminado=False)

    # Apply filters
    if nombre:
        query = query.filter(Caballo.nombre.ilike(f"%{nombre}%"))
    if tipo_de_JyA_asignado:
        query = query.filter(cast(Caballo.tipo_de_JyA_asignado, String).ilike(f"%{tipo_de_JyA_asignado}%"))

    # Sort results
    if sort_field and sort_order:
        if sort_order == 'asc':
            query = query.order_by(getattr(Caballo, sort_field).asc())
        else:
            query = query.order_by(getattr(Caballo, sort_field).desc())

    # Pagination
    horses = query.paginate(page=page, per_page=per_page, error_out=False)
    return horses

def create_horse(**kwargs):
    """
    Create a new horse.
    """
    horse = Caballo(**kwargs)
    commit_db(horse)
    return horse

def asign_employee(horse, employee):
    """
    Create a new relation.
    """
    horse.empleados = employee
    commit_db(horse)
    return horse

def search_by_id(id: int):
    """
    Search a horse by id where 'eliminado' is false.
    """
    horse = Caballo.query.filter_by(id=id, eliminado=False).first()
    return horse

def update_horse(id: int, params):
    """
    Update horse.
    """
    horse = search_by_id(id)
    uphorse(horse, params)
    commit_db(horse)
    return horse

def update_employees_in_charge(id: int, params):
    """
    Update employees in charge.
    """
    horse = search_by_id(id)
    # Extraer los DNIs actuales de los empleados
    current_dnis = {employee.dni for employee in horse.empleados}
    
    # Convertir los parámetros a un conjunto de DNIs para facilitar la comparación
    new_dnis = set(params)

    # Identificar DNIs a eliminar (los que están en current_dnis pero no en new_dnis)
    dnis_to_remove = current_dnis - new_dnis
    for dni in dnis_to_remove:
        employee = next((emp for emp in horse.empleados if emp.dni == dni), None)
        if employee:
            horse.empleados.remove(employee)

    # Identificar DNIs a agregar (los que están en new_dnis pero no en current_dnis)
    dnis_to_add = new_dnis - current_dnis
    for dni in dnis_to_add:
        employee = teams.search_by_dni(dni)  # Asegúrate de que esto devuelva el empleado correcto
        if employee:
            horse.empleados.append(employee)

    commit_db(horse)
    return horse


def delete_horse(id: int):
    """
    Delete a horse.
    """
    horse = search_by_id(id)
    horse.eliminado = True
    commit_db(horse)
    return horse

def upload_file(file_name: str, id: int, tipoDocumento: str, es_link: bool = False):
    """
    Uploads a file by creating a new entry in DocumentoCaballo.
    """
    nuevo_archivo = DocumentoCaballo(
        tipo_documento=tipoDocumento,
        id_caballo=id,
        documento=f"{file_name}",
        es_link=es_link)

    commit_db(nuevo_archivo)
    return nuevo_archivo


def get_documents_by_id_horse(id: int):
    """
    Devuelve todos los archivos asociados a un caballo por su id.
    """
    documentos = DocumentoCaballo.query.filter_by(
        id_caballo=id).all()
    files = []

    # Crear una lista de documentos con su tipo y nombre
    for documento in documentos:
        file_data = {
            'nombre': documento.documento,
            'tipo_documento': documento.tipo_documento,
            'fecha': documento.inserted_at,
            'id': documento.id, 
            'es_link': documento.es_link
        }
        files.append(file_data)
    return files


def delete_document_by_id(file_id: int):
    """
    elimina un archivo por su ID.
    """
    archivo = DocumentoCaballo.query.filter_by(id=file_id).first()
    if archivo:
        try:
            delete_from_db(archivo)
            return archivo
        except Exception as e:
            raise Exception(f"Error deleting file: {str(e)}")
    else:
        raise ValueError("File not found.")

