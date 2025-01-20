from src.core.models import Rol
from src.core.models import Permiso


def create_roles_permissions():
    tecnica_permissions = [
        Permiso.search_by_prefix("rider"),
        Permiso.search_by_prefix("equestrian_index"),
        Permiso.search_by_prefix("equestrian_show"),
        Permiso.search_by_prefix("charge_index"),
        Permiso.search_by_prefix("charge_show"),
        Permiso.search_by_prefix("chart_index"),
        Permiso.search_by_prefix("report_index"),
    ]
    tecnica_permissions = [
        item for sublist in tecnica_permissions for item in sublist]

    role1 = Rol.create_role(
        nombre="Tecnica",
        permisos=tecnica_permissions,
    )
    ecuestre_permissions = [
        Permiso.search_by_prefix("rider_index"),
        Permiso.search_by_prefix("rider_show"),
        Permiso.search_by_prefix("equestrian"),
    ]
    ecuestre_permissions = [
        item for sublist in ecuestre_permissions for item in sublist]

    role2 = Rol.create_role(
        nombre="Ecuestre",
        permisos=ecuestre_permissions,
    )
    role3 = Rol.create_role(
        nombre="Voluntariado",
    )

    # first find all permissions that start with a given prefix like "horses" "team" "payment"
    admin_permissions = [
        Permiso.search_by_prefix("content"),
        Permiso.search_by_prefix("team"),
        Permiso.search_by_prefix("payment"),
        Permiso.search_by_prefix("rider"),
        Permiso.search_by_prefix("equestrian_index"),
        Permiso.search_by_prefix("equestrian_show"),
        Permiso.search_by_prefix("charge"),
        Permiso.search_by_prefix("user_index"),
        Permiso.search_by_prefix("user_update"),
        Permiso.search_by_prefix("contact"),
        Permiso.search_by_prefix("chart_index"),
        Permiso.search_by_prefix("report_index"),
        Permiso.search_by_prefix("provisorio"),
    ]
    # flatten the list of lists to only have the ids
    admin_permissions = [
        item for sublist in admin_permissions for item in sublist]

    role4 = Rol.create_role(
        nombre="Administracion",
        permisos=admin_permissions,
    )
