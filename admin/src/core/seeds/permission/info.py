from src.core.models import Permiso


def create_graph_report_permissions():
    """Create a graph permission and report permission."""
    charts = Permiso.create_permission(nombre="chart_index")
    reports = Permiso.create_permission(nombre="report_index")
