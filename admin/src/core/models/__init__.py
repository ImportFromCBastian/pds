from src.core.database import db
from src.core.models.users_module.user import Usuario
from src.core.models.users_module.role import Rol
from src.core.models.users_module.permission import Permiso
from sqlalchemy.orm import joinedload


def get_users_filtered(
        page: int = 1, 
        per_page: int = 5, 
        sort_column: str = "creado_en", 
        sort_order: str = "desc", 
        email: str = None, 
        rol_id: int = None, 
        bloqueado: bool = None
    ):
    """Returns users filtered by email, role, and status, ordered by a given column and order (paginated in 15 users).
    Receives the page to render, the sorting column and order, and optional filters (email, role, and status)."""

    users = Usuario.query.filter_by(
        borrado=False).options(joinedload(Usuario.rol))

    if email:
        users = users.filter(Usuario.email.like(f"%{email}%"))

    if rol_id:
        users = users.filter(Usuario.rol_id == rol_id)

    if bloqueado is not None:
        users = users.filter(Usuario.bloqueado == bloqueado)

    column_mapping = {
        "creado_en": Usuario.creado_en,
        "email": Usuario.email,
    }

    order_by_column = column_mapping.get(sort_column, Usuario.creado_en)

    if sort_order == "desc":
        users = users.order_by(order_by_column.desc())
    else:
        users = users.order_by(order_by_column.asc())

    paginated_users = users.paginate(page=page, per_page=per_page)

    return paginated_users
