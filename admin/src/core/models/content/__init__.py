from sqlalchemy import asc, desc
from sqlalchemy.orm import joinedload
from src.core.database import commit_db, delete_from_db
from src.core.models.content.content import Contenido
from src.core.models.users_module.user import Usuario


def content_index(page=1, per_page=5):
    """
    List all content.
    """
    content = Contenido.query.paginate(
        page=page, per_page=per_page, error_out=False)
    return content


def content_index_api(author=None, published_from=None, published_to=None, page=1, per_page=5):
    """
    List all content, filtered by author alias and/or publication dates.
    """
    query = Contenido.query.filter_by(estado='Publicado')

    if author:
        query = query.join(Usuario).filter(Usuario.alias.ilike(f"%{author}%"))

    if published_from:
        published_from = published_from.replace(
            hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(Contenido.fecha_publicacion >= published_from)

    if published_to:
        published_to = published_to.replace(
            hour=23, minute=59, second=59, microsecond=999999)
        query = query.filter(Contenido.fecha_publicacion <= published_to)
    query = query.order_by(desc(Contenido.fecha_publicacion))
    total = query.count()
    content_data = query.paginate(
        page=page, per_page=per_page, error_out=False)

    return {"items": content_data.items, "total": total}


def get_by_id(content_id):
    """
    Get a content by id.
    """
    content = Contenido.query.filter_by(id=content_id).first()
    return content


def create_content(**kwargs):
    """
    Create a new content.
    """
    new_content = Contenido(**kwargs)
    commit_db(new_content)
    return new_content


def search_by_id(content_id):
    """
    Search a content by id.
    """
    contenido = Contenido.query.filter_by(id=content_id).first()
    return contenido


def update_content(content_id, params):
    """
    Update a content.
    """
    content = search_by_id(content_id)
    for key, value in params.items():
        if value not in [None, ""]:
            setattr(content, key, value)
    commit_db(content)
    return content


def delete_content(content_id):
    """
    Delete a content.
    """
    content = search_by_id(content_id)
    if content:
        try:
            delete_from_db(content)
            return True
        except Exception as e:
            raise Exception("Error deleting content")
    else:
        raise Exception("Content not found")
