from src.core.models import Permiso


def create_permissions():
    """
    Create permissions for the payment module.
    """
    permisson1 = Permiso.create_permission(nombre="payment_index")
    permisson2 = Permiso.create_permission(nombre="payment_new")
    permisson4 = Permiso.create_permission(nombre="payment_update")
