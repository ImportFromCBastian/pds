from src.core.models import Permiso


def create_permissions():
    """
    Create permissions for the user module.
    """
    permission1 = Permiso.create_permission(nombre="user_index")
    permission2 = Permiso.create_permission(nombre="user_new")
    permission3 = Permiso.create_permission(nombre="user_destroy")
    permission4 = Permiso.create_permission(nombre="user_update")
    permission5 = Permiso.create_permission(nombre="user_show")
