from src.core.models import Permiso


def create_permissions():
    """
    Create permissions for the contact module.
    """
    permisson1 = Permiso.create_permission(nombre="contact_index")
    permisson2 = Permiso.create_permission(nombre="contact_show")
    permisson3 = Permiso.create_permission(nombre="contact_update")
    permisson4 = Permiso.create_permission(nombre="contact_create")
    permisson5 = Permiso.create_permission(nombre="contact_destroy")