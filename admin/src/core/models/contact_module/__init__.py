from src.core.models.contact_module.contact import PortalQuery
from src.core.models.contact_module.contact import QueryState


def query_index(
    page: int = 1,
    per_page: int = 5,
    sort_order: str = "desc",
    query_state: str = None,
):
    """ Returns the querys maded by the portal ordered by date of created in descendent form by default.
        Optionally, can be ordered in ascendent form (sending in sort_order, "asc"), and filtered by 
        it's state. Receives the page and items for page to paginate (page 1 and 5 items by default)"""
    
    queries = PortalQuery.query.filter_by(borrado=False)
    
    if query_state in QueryState:
        queries = queries.filter(PortalQuery.estado == query_state)
    
    if sort_order == "asc":
        queries = queries.order_by(PortalQuery.created_at.asc())
    else:
        queries = queries.order_by(PortalQuery.created_at.desc())
        
    queries_paginated = queries.paginate(page=page, per_page=per_page)
    
    return queries_paginated