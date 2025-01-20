from src.core.models.contact_module.contact import PortalQuery
from src.core.models.contact_module.contact import QueryState
from datetime import datetime


def create_portal_querys():
    """Seeds de Database with a few portal querys"""
    portal_query_1 = PortalQuery.create_query(
        titulo="Consulta de Nombres Caballos",
        email="williams@gmail.com",
        descripcion="Hay algun caballo llamado Colapa?",
        estado=QueryState.Creada,
        created_at="2024-11-15",
        closed_at="2024-11-15",
    )
    return portal_query_1.get("portal_query")


def create_portal_querys_2():
    """Seeds de Database with a few portal querys"""
    portal_query_1 = PortalQuery.create_query(
        titulo="Consulta de Nombres Caballos",
        email="dukeBoys@gmail.com",
        descripcion="Hay algun caballo llamado General Lee?",
        estado=QueryState.Creada,
        created_at="2024-11-7",
        closed_at="2024-11-15",
    )
    return portal_query_1.get("portal_query")
