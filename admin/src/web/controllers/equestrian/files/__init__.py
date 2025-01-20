import datetime
from src.core.models import teams
from src.web.controllers.teams.handlers.files.constant import File_Names
from flask import current_app
from os import fstat
from src.core.models import equestrian


def file_uploader(file, horse, tipo):
    """
    Uploads a single file for a horse.
    """
    errors = {}
    if file and file.filename:
        uploaded_file = file
        extension = uploaded_file.filename.split(".")[-1]

        # Check file size limit
        if is_file_size_exceeding_limit(uploaded_file):
            errors["size"] = "Archivo demasiado grande ( > 5 MB)"

        # Check file type
        if not file_type_checker(extension):
            errors["type"] = "Tipo de archivo no soportado"
        
        # Check if the file already exists
        files = equestrian.get_documents_by_id_horse(horse.id)
        for file_data in files:
            if file_data['nombre'] == uploaded_file.filename:
                errors["exists"] = "Ya haz subido un archivo con ese nombre"

        # Check if there are any errors
        if errors:
            return errors

        client = current_app.storage.client
        size = fstat(uploaded_file.fileno()).st_size
        pepe=0
        # Store the file with the original name
        client.put_object(
            current_app.config["MINIO_BUCKET_NAME"],
            f"{horse.id}/{uploaded_file.filename}",  # Use original filename
            uploaded_file,
            size,
            content_type=uploaded_file.content_type,
        )

        # Assuming `upload_file` method takes the original filename
        equestrian.upload_file(uploaded_file.filename,
                           horse.id, tipo)

    return None  # No errors, return None


def file_type_checker(file_type) -> bool:
    """
    Checks if the given file type is supported.
    """

    return file_type in ["pdf", "jpg", "doc", "jpeg", "xls", "png"]


def is_file_size_exceeding_limit(file) -> bool:
    """
    Checks if the uploaded file size exceeds a reasonable limit (5 MB).
    """

    return fstat(file.fileno()).st_size > 5 * 1024 * 1024


def get_time_until_midnight() -> datetime.timedelta:
    """
    Calculate the time remaining until the next midnight.
    """
    now = datetime.datetime.now()
    next_midnight = datetime.datetime.combine(
        now + datetime.timedelta(days=1), datetime.time.min
    )
    return next_midnight - now


def get_url(id: int, file_type: str, download=True) -> str:
    """
    Returns the URL of the object storage.
    """
    client = current_app.storage.client
    files = equestrian.get_documents_by_id_horse(id)

    file_found = next(
        (file for file in files if file['tipo_documento'] == file_type), None)

    if not file_found:
        return None

    try:
        client.stat_object(
            current_app.config["MINIO_BUCKET_NAME"], f"{
                id}/{file_found['nombre']}"
        )
    except Exception as e:
        return None

    expires_at_midnight = get_time_until_midnight()

    if download:
        return client.presigned_get_object(
            current_app.config["MINIO_BUCKET_NAME"],
            f"{id}/{file_found['nombre']}",
            expires=expires_at_midnight,
            response_headers={
                "response-content-disposition": f'attachment; filename="{file_found["nombre"]}"'
            },
        )
    return client.presigned_get_object(
        current_app.config["MINIO_BUCKET_NAME"],
        f"{id}/{file_found['nombre']}",
        expires=expires_at_midnight,
    )


# Función para obtener documentos filtrados y luego ordenarlos
def get_documents(id: int, nombre=None, tipo=None, order_by=None):
    """
    Genera los enlaces para descargar y previsualizar todos los archivos de un caballo,
    aplicando filtros por nombre, tipo y ordenamiento si se proporcionan.
    """
    links = []
    files = equestrian.get_documents_by_id_horse(id)

    if files is None:
        return links
    for file_data in files:
        file_name = file_data['nombre']
        file_type = file_data['tipo_documento']
        file_id = file_data['id']
        file_is_link = file_data['es_link']

        if nombre and nombre.lower() not in file_name.lower():
            continue
        if tipo is not None and file_type.name != tipo.strip():
            continue

        new_link = {
            "id": file_id,
            "nombre": file_name,
            "tipo": file_type,
            "fecha": file_data['fecha'].strftime("%Y-%m-%d"),
            "es_enlace": file_is_link
        }

        if not file_is_link:
            preview_url = get_url(id, file_type, False)
            download_url = get_url(id, file_type, True)
            if preview_url and download_url:
                new_link["preview"] = preview_url
                new_link["link"] = download_url

        links.append(new_link)

    # Si hay una ordenación especificada, aplicarla
    if order_by:
        links = sort_documents(links, order_by)
    return links


# Función para ordenar documentos según el criterio dado
def sort_documents(documents, order_by):
    if order_by == "nombre-asc":
        return sorted(documents, key=lambda x: x['nombre'].lower())
    elif order_by == "nombre-desc":
        return sorted(documents, key=lambda x: x['nombre'].lower(), reverse=True)
    elif order_by == "fecha-asc":
        return sorted(documents, key=lambda x: x['fecha'])
    elif order_by == "fecha-desc":
        return sorted(documents, key=lambda x: x['fecha'], reverse=True)

    return documents  # Si no se especifica orden, devolver sin cambio


# Función para limpiar los filtros y resetear la búsqueda
def clear_filters():
    """
    Esta función restablece los valores de los filtros (nombre y tipo) para que se 
    puedan realizar nuevas búsquedas sin filtros.
    """
    global nombre, tipo
    nombre = None
    tipo = None


def delete_document(id: int, file_name: str):
    """
    Elimina un archivo de MinIO por el id del caballo y el nombre del archivo.
    """
    client = current_app.storage.client
    try:
        # Intenta eliminar el archivo especificado
        client.remove_object(
            current_app.config["MINIO_BUCKET_NAME"],
            f"{id}/{file_name}"
        )
        return True
    except Exception as e:
        return False


def link_uploader(link: str, id, tipo):
    """
    Carga un enlace para un caballo.
    """
    if not link.startswith("http://") and not link.startswith("https://"):
        return {"error": "El enlace debe comenzar con 'http://' o 'https://'."}

    try:
        equestrian.upload_file(link, id, tipo, es_link=True)
        return None  # No hay errores
    except Exception as e:
        return {"error": f"Error al cargar el enlace: {str(e)}"}
