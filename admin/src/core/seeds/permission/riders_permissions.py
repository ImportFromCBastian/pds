from src.core.models import Permiso


def create_permissions():
    """
    Create permissions for the riders module.
    """
    permisson1 = Permiso.create_permission(nombre="rider_index")
    permisson2 = Permiso.create_permission(nombre="rider_new")
    permisson3 = Permiso.create_permission(nombre="rider_submit_files")
    permisson4 = Permiso.create_permission(nombre="rider_update")
    permisson5 = Permiso.create_permission(nombre="rider_show")
    permisson6 = Permiso.create_permission(nombre="rider_destroy")
