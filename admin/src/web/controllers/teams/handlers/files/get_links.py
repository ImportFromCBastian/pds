from flask import current_app
from src.web.controllers.teams.handlers.files.constant import File_Names
from src.core.models import teams
import datetime


def get_time_until_midnight() -> datetime.timedelta:
    """
    Calculate the time remaining until the next midnight.
    """
    now = datetime.datetime.now()
    # Calculate next midnight
    next_midnight = datetime.datetime.combine(
        now + datetime.timedelta(days=1), datetime.time.min
    )
    # Calculate the time difference between now and next midnight
    return next_midnight - now


def get_url(dni: int, type: str, download=True) -> str:
    """
    Returns the URL of the object storage.
    """

    client = current_app.storage.client
    files = teams.get_files_by_dni(dni)

    try:
        client.stat_object(
            current_app.config["MINIO_BUCKET_NAME"], f"{dni}/{files[type]}"
        )
    except:
        return

    expires_at_midnight = get_time_until_midnight()

    if download:
        return client.presigned_get_object(
            current_app.config["MINIO_BUCKET_NAME"],
            f"{dni}/{files[type]}",
            expires=expires_at_midnight,
            response_headers={
                "response-content-disposition": f'attachment; filename="{files[type]}"'
            },
        )
    return client.presigned_get_object(
        current_app.config["MINIO_BUCKET_NAME"],
        f"{dni}/{files[type]}",
        expires=expires_at_midnight,
    )


def get(dni: int):
    """
    Returns all the links for the files of a team member.
    """
    links = []
    for file_name in File_Names:
        new_link = {
            "link": get_url(dni, file_name),
            "preview": get_url(dni, file_name, False),
        }
        if None not in new_link.values():
            links.append(new_link)

    return links
