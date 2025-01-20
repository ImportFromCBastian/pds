from src.core.seeds.team_seeds import create_employee
from src.core.seeds.user_seeds import create_users
from src.core.seeds.payment_seeds import create_payments
from src.core.seeds.rider_seeds import create_riders
from src.core.seeds.charge_seeds import create_charges
from src.core.seeds.equestrian_seed import create_horses
from src.core.seeds.permission import create_all_permission
from src.core.seeds.role_seeds import create_roles_permissions
from src.core.seeds.content_seeds import create_contents
from src.core.seeds.contact_seeds import create_portal_querys, create_portal_querys_2
# To poblate the local database


def seed_db():
    """
    Grows the database with some data.
    """
    print("Seeding the database🌱")

    # Añado permisos
    create_all_permission()

    # Añado roles con permisos
    create_roles_permissions()

    # Añado usuarios
    create_users()

    # Añado empleados
    create_employee()

    # Añado pagos
    create_payments()

    # Añado caballos
    create_horses()

    # Añado jinetes
    create_riders()

    # Añado cobros
    create_charges()

    # Añado contenidos
    create_contents()
    
    # Añado consultas del portal
    create_portal_querys()
    create_portal_querys_2()

    print("Database grown🌳")
