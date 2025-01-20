from src.web.handlers.auth import login_and_permission_required, get_logged_in_user
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.models import content
from src.web.controllers.content.validators.validator import validate_content, validate_partial_content
bp = Blueprint("content", __name__, url_prefix="/contenido")


@bp.get("/")
@login_and_permission_required("content_index")
def index():
    """
    lists content in the system.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    content_data = content.content_index(page=page, per_page=per_page)
    return render_template(
        "content/index.html",
        content=content_data,
        page=page,
        per_page=per_page,
        errors={}
    )


@bp.get("/detalles/<int:id>")
@login_and_permission_required("content_show")
def details(id):
    """
    Shows the whole content.
    """
    content_data = content.search_by_id(id)

    return render_template(
        "content/details.html",
        content=content_data,
    )


@bp.get("/crear")
@login_and_permission_required("content_new")
def new():
    """
    Create a new content.
    """
    return render_template("content/create.html")


@bp.post("/crear")
@login_and_permission_required("content_new")
def createContent():
    params = request.form.to_dict()
    params["autor_email"] = get_logged_in_user()
    if params["estado"] == "Publicado":
        params["fecha_publicacion"] = datetime.now()
    is_valid = validate_content(params)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo crear. Error en el campo '{
                  field}': {error['msg']}", "error")
            return redirect(url_for("content.index"))
    try:
        new_content = content.create_content(**params)
    except Exception as e:
        return f"Error creating content: {str(e)}", 500

    flash(
        f"Contenido con titulo {new_content.titulo} creado con éxito", "success")
    return redirect(url_for("content.details", id=new_content.id))


@bp.get("/actualizar/<int:id>")
@login_and_permission_required("content_update")
def edit(id):
    """
    Update a content.
    """
    content_data = content.search_by_id(id)
    return render_template("content/edit.html", content=content_data)


def clean_text(text):
    """Función para limpiar texto"""
    return ' '.join(text.strip().replace('\n', ' ').split())


@bp.post("/actualizar/<int:id>")
@login_and_permission_required("content_update")
def editContent(id):
    content_data = content.search_by_id(id)
    params = request.form.to_dict()
    if params["estado"] == "Publicado":
        if content_data.estado.value != "Publicado":
            params["fecha_publicacion"] = datetime.now()
    if (
        clean_text(params.get("estado", "")) == clean_text(content_data.estado.value) and
        clean_text(params.get("titulo", "")) == clean_text(content_data.titulo) and
        clean_text(params.get("copete", "")) == clean_text(content_data.copete) and
        clean_text(params.get("contenido", "")) == clean_text(
            content_data.contenido)
    ):
        return redirect(url_for("content.details", id=id))

    is_valid = validate_partial_content(params)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo actualizar. Error en el campo '{
                  field}': {error['msg']}", "error")

        return redirect(url_for("content.edit", id=id))
    try:
        updated_content = content.update_content(id, params)

    except Exception as e:
        print("Error updating content:", e)
        return f"Error updating content: {str(e)}", 500

    flash(f"Contenido con titulo {
          updated_content.titulo} actualizado con éxito", "success")
    return redirect(url_for("content.details", id=updated_content.id))


@bp.post("/eliminar/<int:id>")
@login_and_permission_required("content_delete")
def deleteContent(id):
    """
    Delete a content.
    """
    content_data = content.search_by_id(id)
    try:
        content.delete_content(id)
    except Exception as e:
        return f"Error deleting content: {str(e)}", 500

    flash(f"Contenido con título {
          content_data.titulo} eliminado con éxito", "success")
    return redirect(url_for("content.index"))
