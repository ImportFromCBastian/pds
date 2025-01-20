from src.core.models import Permiso


def create_permissions():
    """
    Create permissions for the riders module.
    """
    permisson1 = Permiso.create_permission(nombre="equestrian_index")
    permisson2 = Permiso.create_permission(nombre="equestrian_new")
    permisson3 = Permiso.create_permission(nombre="equestrian_submit_files")
    permisson4 = Permiso.create_permission(nombre="equestrian_update")
    permisson5 = Permiso.create_permission(nombre="equestrian_show")
    permisson6 = Permiso.create_permission(nombre="equestrian_destroy")