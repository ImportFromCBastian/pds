from src.core.models import Permiso


def create_permissions():
    """
    Create permissions for the content module.
    """
    permisson1 = Permiso.create_permission(nombre="content_index")
    permisson2 = Permiso.create_permission(nombre="content_new")
    permisson3 = Permiso.create_permission(nombre="content_update")
    permisson4 = Permiso.create_permission(nombre="content_show")
    permisson5 = Permiso.create_permission(nombre="content_destroy")
