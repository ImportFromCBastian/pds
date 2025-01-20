from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.models import equestrian
from src.core.models import teams
from src.core.models.equestrian.Horse import JyAType, CompraDonacion, Sexo, Sede
from src.web.controllers.equestrian.handlers.search import filter_horses
from web.controllers.equestrian.handlers.validators.validator import validate_horse, validate_partial_horse
from math import ceil
from src.web.controllers.equestrian.files import file_uploader, sort_documents, get_documents, clear_filters, delete_document, link_uploader
from src.core.models.equestrian.Horse import TipoDocumento
bp = Blueprint("equestrian", __name__, url_prefix="/ecuestre")

from flask import request, render_template
from math import ceil
from src.web.handlers.auth import login_and_permission_required

@bp.get("/")
@login_and_permission_required("equestrian_index")
def index():
    """
    Shows the index of the horses with pagination and filtering.
    """
    # Get query parameters for pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    # Get filter parameters
    nombre = request.args.get('nombre', None)
    tipo_de_JyA_asignado = request.args.get('tipo_de_JyA', None)
    sort_field = request.args.get('sort_field', 'nombre')
    sort_order = request.args.get('sort_order', 'asc')

    # Get horses with filtering and pagination
    horses_data = equestrian.equestrian_index(page=page, per_page=per_page, nombre=nombre,
                                           tipo_de_JyA_asignado=tipo_de_JyA_asignado, sort_field=sort_field, sort_order=sort_order)

    return render_template(
        "equestrian/index.html",
        horses=horses_data,
        page=page,
        typeofJyA=JyAType,
        total_pages=horses_data.pages,
        total_horses=horses_data.total,
        per_page=per_page,
        nombre=nombre,
        tipo_de_JyA_asignado=tipo_de_JyA_asignado,
        sort_field=sort_field,
        sort_order=sort_order,
        errors={}
    )




@bp.get("/agregar")
@login_and_permission_required("equestrian_new")
def new():
    """
    Shows the create form for a new horse.
    """
    return render_template(
        "equestrian/new.html",
        typeofJyA=JyAType,
        type_compra_donacion=CompraDonacion,
        genre=Sexo,
        sedes=Sede,
        empleados=teams.team_index(),
        errors={},
    )

@bp.post("/agregar")
@login_and_permission_required("equestrian_new")
def create():
    """
    Create a new horse.
    """
    params = request.form
    is_valid = validate_horse(params)


    errors = {}
    if not is_valid["valid"]:
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]

        return render_template(
            "equestrian/new.html",
            type_compra_donacion=CompraDonacion,
            typeofJyA=JyAType,
            genre=Sexo,
            sedes=Sede,
            empleados=teams.team_index(),
            errors=errors,
        )
    params = params.to_dict()
    dni = params.pop("dni", None)
    employee = teams.search_by_dni(dni)
    # Crear nuevo miembro del equipo
    try:
        new_horse = equestrian.create_horse(**params)
        new_relationship = equestrian.asign_employee(new_horse, [employee])
    except Exception as e:
        # change the return to a redirect to the errors page
        return f"Error creating horse: {str(e)}", 500

    flash("Caballo creado con exito", "success")
    return redirect(url_for("equestrian.index"))

@bp.get("/detalles/<int:id>")
@login_and_permission_required("equestrian_show")
def show(id):
    """
    Shows the details of a horse.
    """

    requested_horse = equestrian.search_by_id(id)

    return render_template("equestrian/show.html", horse=requested_horse)

@bp.get("/editar/<int:id>")
@login_and_permission_required("equestrian_update")
def edit(id):
    """
    Shows the edit form for a team member.
    """
    requested_horse = equestrian.search_by_id(id)

    return render_template(
        "equestrian/edit.html",
        type_compra_donacion=CompraDonacion,
        typeofJyA=JyAType,
        genre=Sexo,
        sedes=Sede,
        empleados=teams.team_index(),
        horse=requested_horse,
        errors={},
    )

@bp.post("/editar/<int:id>")
@login_and_permission_required("equestrian_update")
def update(id):
    """
    Update a team member.
    """
    requested_horse = equestrian.search_by_id(id)

    params = request.form.to_dict()

    is_valid = validate_partial_horse(params)

    errors = {}
    if not is_valid["valid"]:
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]


        return render_template(
            "equestrian/edit.html",
            type_compra_donacion=CompraDonacion,
            typeofJyA=JyAType,
            genre=Sexo,
            sedes=Sede,
            empleados=teams.team_index(),
            horse=requested_horse,
            errors=errors,
        )

    # Actualizar miembro del equipo
    try:
        updated_horse = equestrian.update_horse(id, params)
        # Obtener la lista de DNIs de empleados desde params
        empleados_dni_list = [dni.strip() for dni in params['empleados_dni'].split(',')]

        # Llamar a la función para actualizar los empleados a cargo
        updated_relationship = equestrian.update_employees_in_charge(id, empleados_dni_list)

    except Exception as e:
        return f"Error updating horse: {str(e)}", 500

    horse = equestrian.search_by_id(id)

    flash(
        f"el caballo {horse.nombre} ha sido actualizado con éxito",
        "success",
    )
    return redirect(url_for("equestrian.index"))

@bp.post("/eliminar/<int:id>")
@login_and_permission_required("equestrian_destroy")
def delete(id):
    """
    Delete a horse.
    """

    delete_horse = equestrian.delete_horse(id)

    flash("Caballo eliminado con éxito", "success")

    return redirect(url_for("equestrian.index"))

@bp.route("/documentos/<int:id>")
@login_and_permission_required("equestrian_show")
def showFiles(id):
    """
    Mostrar archivos de los caballos.
    """
    horse = equestrian.search_by_id(id)

    nombre = request.args.get('nombre')
    tipo_documento = request.args.get('tipo_documento')

    documents = get_documents(
        horse.id, nombre=nombre, tipo=tipo_documento)
    nombre = None
    tipo_archivo = None

    order_by = request.args.get('order_by')
    if order_by:

        documents = sort_documents(documents, order_by)
    return render_template("equestrian/showFiles.html", horse=horse, documents=documents, tipo_documento=TipoDocumento)


@bp.get("/archivos/limpiarFiltros/<int:id>")
@login_and_permission_required("equestrian_show")
def clear_all_filters(id):
    clear_filters()
    return redirect(url_for('equestrian.showFiles', id=id))


@bp.post("/archivos/<int:id>")
@login_and_permission_required("equestrian_submit_files")
def submit_files(id):
    """
    Submit files for a horse.
    """

    file = request.files.get('file')
    horse = equestrian.search_by_id(id)
    tipo = request.form.get('tipo_documento')
    error = file_uploader(file, horse, tipo)


    if error:
        error_messages = []
        if "size" in error:
            error_messages.append(error["size"])
        if "type" in error:
            error_messages.append(error["type"])
        if "exists" in error:
            error_messages.append(error["exists"])
        flash("Error al subir el archivo: " +
              ", ".join(error_messages), "error")
        return redirect(url_for("equestrian.showFiles", id=id))

    else:
        flash("Documento subido con éxito", "success")
        return redirect(url_for("equestrian.showFiles", id=id))


@bp.post("/archivos/eliminar/<int:id>")
@login_and_permission_required("equestrian_destroy")
def deleteDocument(id):
    """
    Delete a document by ID.
    """
    document_id = request.form.get("document_id")
    document_nombre = request.form.get("document_nombre")
    document_es_enlace = request.form.get("document_es_enlace") == 'True'

    error = None
    if (not document_es_enlace):
        if delete_document(id, document_nombre):
            try:
                equestrian.delete_document_by_id(document_id)
            except Exception as e:
                error = f"Error eliminando documento de la base de datos: {
                    str(e)}", 500
        else:
            error = "Error al eliminar el archivo de MinIO", 500
    else:
        try:
            equestrian.delete_document_by_id(document_id)
        except Exception as e:
            error = f"Error eliminando documento de la base de datos: {
                str(e)}", 500

    if error:
        flash("Error al eliminar el archivo!", "danger")
    else:
        flash("Archivo eliminado con éxito", "success")
    return redirect(url_for("equestrian.showFiles", id=id))


@bp.post("/archivos/cargar_link/<int:id>")
@login_and_permission_required("equestrian_submit_files")
def submit_links(id):
    """
    Cargar un enlace.
    """
    link = request.form.get("link")
    tipo = request.form.get('tipo_link')
    error = None
    if not link:
        error = "El enlace no puede estar vacío."
    # Aquí puedes agregar la lógica para almacenar el enlace en tu base de datos
    if not error:
        try:
            link_uploader(link, id, tipo)
            flash("Enlace cargado con éxito", "success")
        except Exception as e:
            error = f"Error al cargar el enlace: {str(e)}"

    if error:
        flash(error, "error")

    return redirect(url_for("equestrian.showFiles", id=id))
