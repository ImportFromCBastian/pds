from src.core.models.contact_module.contact import PortalQuery
from src.core.models.contact_module.contact import QueryState
from src.core.models.contact_module import query_index
from flask import render_template, request, redirect, url_for, flash, Blueprint
from src.web.handlers.auth import login_and_permission_required
from src.web.controllers.contact_module.handlers.validators.validator import validate_portal_query, validate_partial_portal_query


bp = Blueprint("modulo_contacto", __name__, url_prefix="/modulo_contacto")


@bp.get("/listado")
@login_and_permission_required("contact_index")
def listado():
    """ Shows the queries maded in the portal """

    sort_order = request.args.get("sort_order", "desc")
    page = request.args.get('page_receive', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    query_state = request.args.get("query_state", None)

    queries = query_index(
        page=page,
        per_page=per_page,
        sort_order=sort_order,
        query_state=query_state
    )

    return render_template("contact_module/index.html", queries=queries, query_states=QueryState)


@bp.get("/modificar_consulta/<id>")
@login_and_permission_required("contact_update")
def modificar_consulta(id: int):
    """Shows the portal query to update it"""
    query = PortalQuery.get_query(id)
    if query:
        return render_template("contact_module/index_update.html", query=query, query_states=QueryState)
    
    flash("No se encontro la consulta", "error")
    return redirect(url_for("modulo_contacto.listado"))


@bp.post("/actualizar_consulta/<id>")
@login_and_permission_required("contact_update")
def actualizar_consulta(id: int):
    """Updates a portal query"""
    query = PortalQuery.get_query(id)
    
    if query:
        data = request.form.to_dict()
        is_valid = validate_partial_portal_query(data)

        if not is_valid["valid"]:
            for error in is_valid["errors"]:
                flash(f'{error["msg"]}', "error")
        
        else:
            state = request.form.get("query_state", None)
            comentary = request.form.get("query_coment", None)
            
            info = query.update_query(state, comentary)
            
            for message in info:
                flash(f'{message}', "info")
            
    else:  
        flash("No se encontro la consulta")
        
    return redirect(url_for("modulo_contacto.listado"))
    

@bp.post("/eliminar_consulta/<id>")
@login_and_permission_required("contact_destroy")
def eliminar_consulta(id: int):
    """Deletes the portal query by the id sended"""
    query = PortalQuery.get_query(id)
    if query:
        query.delete_query(id)
        flash("Se ha eliminado la consulta", "info")
    else:
        flash("No se ha eliminado la consulta", "error")

    return redirect(url_for("modulo_contacto.listado"))


@bp.get("/mostrar_consulta/<id>")
@login_and_permission_required("contact_show")
def mostrar_consulta(id: int):
    """Shows the portal query by the id sended"""
    query = PortalQuery.get_query(id)
    
    if query:
        return render_template("contact_module/index_show.html", query=query)
    
    else:
        flash("No se ha encontrado la consulta", "error")
        
    return redirect(url_for("modulo_contacto.listado"))


