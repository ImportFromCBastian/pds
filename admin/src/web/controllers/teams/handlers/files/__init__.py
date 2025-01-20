from flask import current_app
from os import fstat
from src.web.controllers.teams.handlers.files.constant import (
    File_Names,
    File_Types,
    MAX_FILE_SIZE,
)
from src.core.models import teams


def file_uploader(files, team_member):
    """
    Uploads the files to the object storage.
    """
    errors = {"copia_dni": [], "curriculum_vitae": [], "titulo": []}
    for expected_file_name in File_Names:
        if expected_file_name in files and files[expected_file_name].filename:
            uploaded_file = files[expected_file_name]

            extension = uploaded_file.filename.split(".")[-1]

            if is_file_size_exceeding_limit(uploaded_file):
                errors[expected_file_name].append(
                    "Archivo demasiado grande ( > 5 MB)")

            if not file_type_checker(extension):
                errors[expected_file_name].append(
                    "Tipo de archivo no soportado (solo se soporta png, jpg y pdf)"
                )

            if check_error_dictionary(errors):
                continue

            client = current_app.storage.client
            size = fstat(uploaded_file.fileno()).st_size

            client.put_object(
                current_app.config["MINIO_BUCKET_NAME"],
                f"{team_member.dni}/{expected_file_name}.{extension}",
                uploaded_file,
                size,
                content_type=uploaded_file.content_type,
            )

            teams.upload_file(expected_file_name, extension, team_member.dni)

    if check_error_dictionary(errors):
        return errors


def file_type_checker(file_type) -> bool:
    """
    Checks if the given file type is supported.
    """

    return file_type in File_Types


def is_file_size_exceeding_limit(file) -> bool:
    """
    Checks if the uploaded file size exceeds a reasonable limit (5 MB).
    """

    return fstat(file.fileno()).st_size > MAX_FILE_SIZE


def check_error_dictionary(errors):
    """
    Checks if the error dictionary is empty.
    """

    for key in errors:
        if errors[key]:
            return True

    return False
