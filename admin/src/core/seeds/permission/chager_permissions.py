from src.core.models import Permiso


def create_permissions():
    """
    Create permissions for the chager module.
    """
    permission1 = Permiso.create_permission(nombre="charge_index")
    permission2 = Permiso.create_permission(nombre="charge_create")
    permission3 = Permiso.create_permission(nombre="charge_destroy")
    permission4 = Permiso.create_permission(nombre="charge_update")
    permission5 = Permiso.create_permission(nombre="charge_show")
