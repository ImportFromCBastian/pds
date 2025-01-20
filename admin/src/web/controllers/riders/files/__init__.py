import datetime
from src.core.models import teams
from src.web.controllers.teams.handlers.files.constant import File_Names
from flask import current_app
from os import fstat
from src.core.models import riders


def file_uploader(file, rider, tipo):
    """
    Uploads a single file for a rider.
    """
    errors = {}

    if file and file.filename:
        uploaded_file = file
        extension = uploaded_file.filename.split(".")[-1]
        if (not objectExists(rider.dni, uploaded_file.filename)):
            if is_file_size_exceeding_limit(uploaded_file):
                errors["size"] = "Archivo demasiado grande ( > 5 MB)"

            if not file_type_checker(extension):
                errors["type"] = "Tipo de archivo no soportado. Los tipos soportados son: pdf, jpg, doc, jpeg, xls, png"
            if errors:
                return errors
            client = current_app.storage.client
            size = fstat(uploaded_file.fileno()).st_size

            client.put_object(
                current_app.config["MINIO_BUCKET_NAME"],
                f"{rider.dni}/{uploaded_file.filename}",
                uploaded_file,
                size,
                content_type=uploaded_file.content_type,
            )
            riders.upload_file(uploaded_file.filename,
                               rider.dni, tipo)
        else:
            errors["exists"] = "Ya existe un archivo con ese nombre"
    if errors:
        return errors
    return None


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


def get_url(dni: int, file_type: str, download=True) -> str:
    """
    Returns the URL of the object storage.
    """
    client = current_app.storage.client
    files = riders.get_files_by_dni(dni)

    file_found = next(
        (file for file in files if file['tipo_archivo'] == file_type), None)

    if not file_found:
        return None

    try:
        client.stat_object(
            current_app.config["MINIO_BUCKET_NAME"], f"{
                dni}/{file_found['nombre']}"
        )
    except Exception as e:
        return None

    expires_at_midnight = get_time_until_midnight()

    if download:
        return client.presigned_get_object(
            current_app.config["MINIO_BUCKET_NAME"],
            f"{dni}/{file_found['nombre']}",
            expires=expires_at_midnight,
            response_headers={
                "response-content-disposition": f'attachment; filename="{file_found["nombre"]}"'
            },
        )
    return client.presigned_get_object(
        current_app.config["MINIO_BUCKET_NAME"],
        f"{dni}/{file_found['nombre']}",
        expires=expires_at_midnight,
    )


def objectExists(dni: int, file_name: str) -> bool:
    client = current_app.storage.client
    try:
        client.stat_object(
            current_app.config["MINIO_BUCKET_NAME"], f"{
                dni}/{file_name}"
        )
    except Exception as e:
        return False
    return True


def get_documents(dni: int, nombre=None, tipo=None, order_by=None):
    """
    Genera los enlaces para descargar y previsualizar todos los archivos de un rider,
    aplicando filtros por nombre, tipo y ordenamiento si se proporcionan.
    """
    links = []
    files = riders.get_files_by_dni(dni)
    if files is None:
        return links

    for file_data in files:
        file_name = file_data['nombre']
        file_type = file_data['tipo_archivo']
        file_id = file_data['id']
        file_is_link = file_data['is_link']
        if (objectExists(dni, file_name) or file_is_link):
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
                preview_url = get_url(dni, file_type, False)
                download_url = get_url(dni, file_type, True)
                if preview_url and download_url:
                    new_link["preview"] = preview_url
                    new_link["link"] = download_url
            links.append(new_link)

    if order_by:
        links = sort_documents(links, order_by)
    return links


def sort_documents(documents, order_by):
    if order_by == "nombre-asc":
        return sorted(documents, key=lambda x: x['nombre'].lower())
    elif order_by == "nombre-desc":
        return sorted(documents, key=lambda x: x['nombre'].lower(), reverse=True)
    elif order_by == "fecha-asc":
        return sorted(documents, key=lambda x: x['fecha'])
    elif order_by == "fecha-desc":
        return sorted(documents, key=lambda x: x['fecha'], reverse=True)

    return documents


def clear_filters():
    """
    Esta función restablece los valores de los filtros (nombre y tipo) para que se 
    puedan realizar nuevas búsquedas sin filtros.
    """
    global nombre, tipo
    nombre = None
    tipo = None


def delete_file(dni: int, file_name: str):
    """
    Elimina un archivo de MinIO por el DNI del rider y el nombre del archivo.
    """
    client = current_app.storage.client
    try:
        client.remove_object(
            current_app.config["MINIO_BUCKET_NAME"],
            f"{dni}/{file_name}"
        )
        return True
    except Exception as e:
        return False


def link_uploader(link: str, dni, tipo):
    """
    Carga un enlace para un rider.
    """
    if not link.startswith("http://") and not link.startswith("https://"):
        return {"error": "El enlace debe comenzar con 'http://' o 'https://'."}

    try:
        riders.upload_file(link, dni, tipo, es_link=True)
        return None
    except Exception as e:
        return {"error": f"Error al cargar el enlace: {str(e)}"}
