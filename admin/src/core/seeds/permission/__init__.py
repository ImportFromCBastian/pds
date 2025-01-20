from src.core.seeds.permission import (
    chager_permissions,
    team_permissions,
    user_permissions,
    payment_permissions,
    riders_permissions,
    equestrian_permissions,
    content_permissions,
    contact_permissions,
    info,
    content_permissions,
    provisorio_permissions
)

# first add a new file that contains all the permissions
# then import it here


def create_all_permission():
    """
    Creates all permissions available for the application.
    """
    # Create permissions
    chager_permissions.create_permissions()
    team_permissions.create_permissions()
    user_permissions.create_permissions()
    payment_permissions.create_permissions()
    riders_permissions.create_permissions()
    equestrian_permissions.create_permissions()
    content_permissions.create_permissions()
    contact_permissions.create_permissions()
    info.create_graph_report_permissions()
    provisorio_permissions.create_permissions()
