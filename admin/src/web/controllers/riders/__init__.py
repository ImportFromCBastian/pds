from src.web.handlers.auth import login_and_permission_required
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.models import riders
from src.core.models.teams import search_by_job_position
from src.core.models.equestrian import equestrian_index
from web.controllers.riders.validators.validator import (
    validate_rider,
    validate_partial_rider,
    validate_partial_institution,
    validate_partial_provisional_situation,
    validate_partial_work,
    validate_family_member,
    validate_work,
    validate_institution,
    validate_provisional_situation
)
from src.web.controllers.riders.files import file_uploader, sort_documents, get_documents, clear_filters, delete_file, link_uploader

from src.core.models.riders.rider import Sede, PropuestaTrabajo, Condition, PensionType, DiagnosisType, NivelEscolaridad, TipoArchivo
bp = Blueprint("riders", __name__, url_prefix="/equitadores")


@bp.get("/")
@login_and_permission_required("rider_index")
def index():
    """
    Shows the index of the riders with pagination and filtering.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    dni = request.args.get('dni', None)
    nombre = request.args.get('nombre', None)
    apellido = request.args.get('apellido', None)
    profesional = request.args.get('profesional', None)
    sort_field = request.args.get('sort_field', 'dni')
    sort_order = request.args.get('sort_order', 'asc')

    riders_data = riders.rider_index(page=page, per_page=per_page, dni=dni, nombre=nombre,
                                     apellido=apellido, profesional=profesional, sort_field=sort_field, sort_order=sort_order)

    return render_template(
        "riders/index.html",
        riders=riders_data,
        page=page,
        total_pages=riders_data.pages,
        total_riders=riders_data.total,
        per_page=per_page,
        dni=dni,
        nombre=nombre,
        apellido=apellido,
        profesional=profesional,
        sort_field=sort_field,
        sort_order=sort_order,
        errors={}
    )


@bp.get("/info/<int:dni>")
@login_and_permission_required("rider_show")
def info(dni):
    """
    Shows the details of a rider.
    """
    rider = riders.search_by_dni(dni)

    return render_template(
        "riders/info.html",
        rider=rider,
        DiagnosisType=DiagnosisType,

    )


@bp.post("/eliminar/<int:dni>")
@login_and_permission_required("rider_destroy")
def deleteRider(dni):
    """
    Delete a rider by DNI.
    """
    try:
        riders.rider_delete(dni)
    except Exception as e:
        return f"Error deleting rider: {str(e)}", 500

    flash(f"Equitador con DNI {dni} eliminado con éxito", "success")
    return redirect(url_for("riders.index"))


@bp.get("/editarInfoPersonal/<int:dni>")
@login_and_permission_required("rider_show")
def editPersonalData(dni):
    """
    Edit a rider.
    """
    rider = riders.search_by_dni(dni)
    return render_template(
        "riders/edit/editPersonalData.html",
        rider=rider,
        DiagnosisType=DiagnosisType,
        fecha_actual=datetime.today()
    )


@bp.post("/editarInfoPersonal/<int:dni>")
@login_and_permission_required("rider_update")
def updatePersonalData(dni):
    rider = riders.search_by_dni(dni)
    params = request.form.to_dict()
    tipo_discapacidad = request.form.getlist("tipo_discapacidad[]")
    params['tipo_discapacidad'] = ', '.join(tipo_discapacidad)
    if params['certificado_discapacidad'] == 'true':
        params['certificado_discapacidad'] = True
        if params['diagnostico_discapacidad'] != 'otro':
            params['otro_diagnostico'] = None
    else:
        params['certificado_discapacidad'] = False
        params['diagnostico_discapacidad'] = None
        params['otro_diagnostico'] = None
    is_valid = validate_partial_rider(params)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo actualizar. Error en el campo '{
                  field}': {error['msg']}", "error")
        return redirect(url_for("riders.editPersonalData", dni=dni))
    try:
        updated_rider = riders.rider_update(dni, params)
    except Exception as e:
        return f"Error updating rider: {str(e)}", 500

    flash(
        f"Equitador con DNI {rider.dni} actualizado con éxito", "success")
    return redirect(url_for("riders.info", dni=rider.dni))


@bp.get("/editarDatosContacto/<int:dni>")
@login_and_permission_required("rider_show")
def editContactData(dni):
    """
    Edit the contact data of a rider.
    """
    rider = riders.search_by_dni(dni)
    return render_template(
        "riders/edit/editContactData.html",
        rider=rider,

    )


@bp.post("/editarDatosContacto/<int:dni>")
@login_and_permission_required("rider_update")
def updateContactData(dni):
    rider = riders.search_by_dni(dni)
    params = request.form.to_dict()
    is_valid = validate_partial_rider(params)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo actualizar. Error en el campo '{
                  field}': {error['msg']}", "error")
        return redirect(url_for("riders.editContactData", dni=dni))
    try:
        updated_rider = riders.rider_update(dni, params)
    except Exception as e:
        return f"Error updating rider: {str(e)}", 500

    flash(
        f"Equitador con DNI {rider.dni} actualizado con éxito", "success")
    return redirect(url_for("riders.info", dni=rider.dni))


@bp.get("/editarDatosAcademicos/<int:dni>")
@login_and_permission_required("rider_show")
def editAcademicData(dni):
    """
    Edit the academic data of a rider.
    """
    rider = riders.search_by_dni(dni)
    return render_template(
        "riders/edit/editAcademicData.html",
        rider=rider,
    )


@bp.post("/editarDatosAcademicos/<int:dni>")
@login_and_permission_required("rider_update")
def updateAcademicData(dni):
    rider = riders.search_by_dni(dni)
    params = request.form.to_dict()
    if params["observaciones"] == "":
        params["observaciones"] = None
    is_valid = validate_partial_institution(params)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo actualizar. Error en el campo '{
                  field}': {error['msg']}", "error")
        return redirect(url_for("riders.editAcademicData", dni=dni))
    try:
        updated_institution = riders.academic_update(
            rider.institucion_escolar_id, params)
    except Exception as e:
        return f"Error updating rider: {str(e)}", 500

    flash(
        f"Información académica del equitador con DNI {rider.dni} actualizado con éxito", "success")
    return redirect(url_for("riders.info", dni=rider.dni))


@bp.get("/editarTrabajoInstitucion/<int:dni>")
@login_and_permission_required("rider_show")
def editInstitutionalWork(dni):
    """
    Update the institutional data of a rider.
    """
    rider = riders.search_by_dni(dni)
    Profesores = search_by_job_position("profesor_equitacion")
    Profesores.extend(search_by_job_position("terapeuta"))
    Conductores = search_by_job_position("conductor")
    Auxiliares = search_by_job_position("auxiliar_pista")
    Caballos = equestrian_index()

    return render_template(
        "riders/edit/editInstitutionalData.html",
        rider=rider,
        condition=Condition,
        sedes=Sede,
        propuesta_trabajo=PropuestaTrabajo,
        profesores=Profesores,
        conductores=Conductores,
        auxiliares=Auxiliares,
        caballos=Caballos
    )


@bp.post("/editarTrabajoInstitucion/<int:dni>")
@login_and_permission_required("rider_update")
def updateInstitutionalData(dni):
    rider = riders.search_by_dni(dni)
    params = request.form.to_dict()
    dia = request.form.getlist("dia[]")
    params['dia'] = ', '.join(dia)
    is_valid = validate_partial_work(params)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo actualizar. Error en el campo '{
                  field}': {error['msg']}", "error")
        return redirect(url_for("riders.editInstitutionalWork", dni=dni))
    try:
        updated_work = riders.institutionalWork_update(
            rider.trabajo_institucional_id, params)
    except Exception as e:
        return f"Error updating rider: {str(e)}", 500

    flash(
        f"Trabajo institucional del equitador con DNI {rider.dni} actualizado con éxito", "success")
    return redirect(url_for("riders.info", dni=rider.dni))


@bp.get("/editarSituacionPrevisional/<int:dni>")
@login_and_permission_required("rider_show")
def editProvisionalSituation(dni):
    """
    Edit the provisional situation of a rider.
    """
    rider = riders.search_by_dni(dni)

    return render_template(
        "riders/edit/editProvisionalData.html",
        rider=rider,

    )


@bp.post("/editarSituacionPrevisional/<int:dni>")
@login_and_permission_required("rider_update")
def updateProvisionalSituation(dni):
    rider = riders.search_by_dni(dni)
    params = request.form.to_dict()
    if params["tiene_curatela"] == "true":
        params["tiene_curatela"] = True
    else:
        params["tiene_curatela"] = False
    if params["observaciones"] == "":
        params["observaciones"] = None
    is_valid = validate_partial_provisional_situation(params)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo actualizar. Error en el campo '{
                  field}': {error['msg']}", "error")
        return redirect(url_for("riders.editProvisionalData", dni=dni))
    try:
        updated_situation = riders.previtionalSituation_update(
            rider.situacion_previsional_id, params)
    except Exception as e:
        return f"Error updating rider: {str(e)}", 500

    flash(
        f"Situación provisional del equitador con DNI {rider.dni} actualizado con éxito", "success")
    return redirect(url_for("riders.info", dni=rider.dni))


@bp.get("/editarInformacionAdicional/<int:dni>")
@login_and_permission_required("rider_show")
def editAditionalData(dni):
    """
    Edit the additional data of a rider.
    """
    rider = riders.search_by_dni(dni)

    return render_template(
        "riders/edit/editAditionalData.html",
        rider=rider,
        PensionType=PensionType
    )


@bp.post("/editarInformacionAdicional/<int:dni>")
@login_and_permission_required("rider_update")
def updateAditionalData(dni):
    rider = riders.search_by_dni(dni)
    params = request.form.to_dict()
    if "becado" in params:
        if params["becado"] == "true":
            params["becado"] = True
        else:
            params["becado"] = False
            params["porcentaje_beca"] = None

    if "recibe_asignacion" in params:
        if params["recibe_asignacion"] == "true":
            params["recibe_asignacion"] = True
            tipo_asignacion = request.form.getlist("tipo_asignacion[]")
            params['tipo_asignacion'] = ', '.join(tipo_asignacion)
        else:
            params["recibe_asignacion"] = False
            params["tipo_asignacion"] = None

    if "recibe_pension" in params:
        if params["recibe_pension"] == "true":
            params["recibe_pension"] = True
        else:
            params["recibe_pension"] = False
            params["tipo_pension"] = None

    is_valid = validate_partial_rider(params)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo actualizar. Error en el campo '{
                  field}': {error['msg']}", "error")
        return redirect(url_for("riders.info", dni=dni))
    try:
        updated_rider = riders.rider_update(dni, params)
    except Exception as e:
        return f"Error updating rider: {str(e)}", 500

    flash(
        f"Equitador con DNI {rider.dni} actualizado con éxito", "success")
    return redirect(url_for("riders.info", dni=rider.dni))


@bp.post("/cargarNuevoFamiliar/<int:dni>")
@login_and_permission_required("rider_new")
def createNewFamilyMember(dni):
    rider = riders.search_by_dni(dni)
    params = request.form.to_dict()
    params["equitador_dni"] = rider.dni
    is_valid = validate_family_member(params)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo actualizar. Error en el campo '{
                  field}': {error['msg']}", "error")
        return redirect(url_for("riders.info", dni=dni))
    try:
        updated_rider = riders.familiar_responsable_create(**params)
    except Exception as e:
        return f"Error updating rider: {str(e)}", 500

    flash(
        f"Equitador con DNI {rider.dni} actualizado con éxito", "success")
    return redirect(url_for("riders.info", dni=rider.dni))


@bp.get("/cargarNuevoFamiliar/<int:dni>")
@login_and_permission_required("rider_show")
def newFamilyMember(dni):
    """
    load a new family member.
    """
    rider = riders.search_by_dni(dni)
    return render_template(
        "riders/new/newFamilyMember.html",
        rider=rider,
        nivel_escolaridad=NivelEscolaridad
    )


@bp.post("/eliminar/<int:dni>/<int:riderdni>")
@login_and_permission_required("rider_destroy")
def deleteFamilyMember(dni, riderdni):
    """
    Delete a family member by DNI.
    """
    try:
        riders.familyMember_delete(dni)
    except Exception as e:
        return f"Error deleting family member: {str(e)}", 500

    flash(f"Familiar con DNI {dni} eliminado con éxito", "success")
    return redirect(url_for("riders.info", dni=riderdni))


@bp.post("/crearEquitador")
@login_and_permission_required("rider_new")
def createRider():
    """
    Create a new rider.
    """
    params = request.form.to_dict()

    tipo_discapacidad = request.form.getlist("tipo_discapacidad[]")
    params['tipo_discapacidad'] = ', '.join(tipo_discapacidad)

    params['certificado_discapacidad'] = params.get(
        'certificado_discapacidad', 'false') == 'true'
    if params['certificado_discapacidad']:
        if params['diagnostico_discapacidad'] != 'otro':
            params['otro_diagnostico'] = None
    else:
        params['diagnostico_discapacidad'] = None
        params['otro_diagnostico'] = None

    if not params.get("informacion_previsional_observaciones"):
        params["informacion_previsional_observaciones"] = None
    if not params.get("observaciones"):
        params["observaciones"] = None

    if not params.get("institucion_escolar_observaciones"):
        params["institucion_escolar_observaciones"] = None

    params['informacion_previsional_tiene_curatela'] = params.get(
        "informacion_previsional_tiene_curatela", 'false') == 'true'

    params['becado'] = params.get("becado", 'false') == 'true'
    if not params['becado']:
        params["porcentaje_beca"] = None

    params['recibe_asignacion'] = params.get(
        "recibe_asignacion", 'false') == 'true'
    if params['recibe_asignacion']:
        tipo_asignacion = request.form.getlist("tipo_asignacion[]")
        params['tipo_asignacion'] = ', '.join(tipo_asignacion)
    else:
        params["tipo_asignacion"] = None

    params['recibe_pension'] = params.get("recibe_pension", 'false') == 'true'
    if not params['recibe_pension']:
        params["tipo_pension"] = None

    dias = request.form.getlist("trabajo_institucional_dia[]")
    params['trabajo_institucional_dia'] = ', '.join(dias)

    equitador_data = {
        'dni': params['dni'],
        'nombre': params['nombre'],
        'apellido': params['apellido'],
        'tipo_discapacidad': params['tipo_discapacidad'],
        'fecha_nacimiento': params['fecha_nacimiento'],
        'lugar_nacimiento': params['lugar_nacimiento'],
        'domicilio_actual': params['domicilio_actual'],
        'telefono': params['telefono'],
        'numero_emergencia': params['numero_emergencia'],
        'nombre_emergencia': params['nombre_emergencia'],
        'becado': params['becado'],
        'porcentaje_beca': params.get('porcentaje_beca'),
        'observaciones': params.get('observaciones'),
        'certificado_discapacidad': params['certificado_discapacidad'],
        'diagnostico_discapacidad': params.get('diagnostico_discapacidad'),
        'otro_diagnostico': params.get('otro_diagnostico'),
        'recibe_asignacion': params['recibe_asignacion'],
        'tipo_asignacion': params.get('tipo_asignacion'),
        'recibe_pension': params['recibe_pension'],
        'tipo_pension': params.get('tipo_pension'),
        'profesionales': params['profesionales'],
    }
    is_valid = validate_rider(equitador_data)
    errors = {}
    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
            flash(f"No se pudo crear al jinete/amazona. Error en el campo '{
                  field}': {error['msg']}", "error")
        return redirect(url_for("riders.index"))

    trabajo_institucional_data = {
        'sede': params['trabajo_institucional_sede'],
        'tipo_trabajo': params['trabajo_institucional_tipo_trabajo'],
        'profesor_terapeuta_id': params['profesor_terapeuta_id'],
        'conductor_caballo_id': params['conductor_caballo_id'],
        'auxiliar_pista_id': params['auxiliar_pista_id'],
        'caballo_id': params['caballo_id'],
        'dia': params['trabajo_institucional_dia'],
        'condicion': params['trabajo_institucional_condicion'],
    }
    institucion_escolar_data = {
        'nombre': params['institucion_escolar_nombre'],
        'direccion': params['institucion_escolar_direccion'],
        'telefono': params['institucion_escolar_telefono'],
        'grado_actual': params['institucion_escolar_grado_actual'],
        'observaciones': params['institucion_escolar_observaciones'],
    }
    situacion_previsional_data = {
        'tiene_curatela': params['informacion_previsional_tiene_curatela'],
        'observaciones': params['informacion_previsional_observaciones'],
        'obra_social': params['informacion_previsional_obra_social'],
        'numero_afiliado': params['informacion_previsional_numero_afiliado'],
    }
    if not (
        validate_work(trabajo_institucional_data) and
        validate_institution(institucion_escolar_data) and
        validate_provisional_situation(situacion_previsional_data)
    ):
        flash("Error en la validación de datos de trabajo, institución o situación previsional", "danger")
        return redirect(url_for("riders.index", riders=riders.rider_index()))
    institucionEscolar = riders.institucion_escolar_create(
        **institucion_escolar_data)
    trabajoInstitucional = riders.trabajo_institucional_create(
        **trabajo_institucional_data)
    situacionPrevisional = riders.situacion_previsional_create(
        **situacion_previsional_data)
    equitador_data['institucion_escolar_id'] = institucionEscolar.id
    equitador_data['trabajo_institucional_id'] = trabajoInstitucional.id
    equitador_data['situacion_previsional_id'] = situacionPrevisional.id

    equitador = riders.rider_create(**equitador_data)
    flash(f"Equitador con DNI {equitador.dni} creado con éxito", "success")
    return redirect(url_for("riders.info", dni=equitador.dni))


@bp.get("/crearEquitador")
@login_and_permission_required("rider_show")
def newRider():
    Profesores = search_by_job_position("profesor_equitacion")
    Profesores.extend(search_by_job_position("terapeuta"))
    Conductores = search_by_job_position("conductor")
    Auxiliares = search_by_job_position("auxiliar_pista")
    Caballos = equestrian_index()
    return render_template(
        "riders/new/newRider.html",
        sedes=Sede,
        propuesta_trabajo=PropuestaTrabajo,
        condition=Condition,
        profesores=Profesores,
        conductores=Conductores,
        auxiliares=Auxiliares,
        DiagnosisType=DiagnosisType,
        PensionType=PensionType,
        caballos=Caballos,
        fecha_actual=datetime.today()
    )


@bp.get("/archivos/<int:dni>")
@login_and_permission_required("rider_show")
def showFiles(dni):
    """
    Mostrar archivos del jinete/amazona.
    """
    rider = riders.search_by_dni(dni)

    nombre = request.args.get('nombre')
    tipo_archivo = request.args.get('tipo_archivo')

    documents = get_documents(
        rider.dni, nombre=nombre, tipo=tipo_archivo)
    nombre = None
    tipo_archivo = None

    order_by = request.args.get('order_by')
    if order_by:

        documents = sort_documents(documents, order_by)
    return render_template("riders/showFiles.html", rider=rider, documents=documents, tipo_archivo=TipoArchivo)


@bp.get("/archivos/limpiarFiltros/<int:dni>")
@login_and_permission_required("rider_show")
def clear_all_filters(dni):
    clear_filters()
    return redirect(url_for('riders.showFiles', dni=dni))


@bp.post("/archivos/<int:dni>")
@login_and_permission_required("rider_submit_files")
def submit_files(dni):
    """
    Submit files for a rider.
    """

    file = request.files.get('file')
    rider = riders.search_by_dni(dni)
    tipo = request.form.get('tipo_archivo')
    error = file_uploader(file, rider, tipo)

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
        return redirect(url_for("riders.showFiles", dni=dni))

    else:
        flash("Archivo subido con éxito", "success")
        return redirect(url_for("riders.showFiles", dni=dni))


@bp.post("/archivos/eliminar/<int:dni>")
@login_and_permission_required("rider_destroy")
def deleteDocument(dni):
    """
    Delete a document by ID.
    """
    document_id = request.form.get("document_id")
    document_nombre = request.form.get("document_nombre")
    document_es_enlace = request.form.get("document_es_enlace") == 'True'

    error = None
    if (not document_es_enlace):
        if delete_file(dni, document_nombre):
            try:
                riders.delete_file_by_id(document_id)
            except Exception as e:
                error = f"Error eliminando documento de la base de datos: {
                    str(e)}", 500
        else:
            error = "Error al eliminar el archivo de MinIO", 500
    else:
        try:
            riders.delete_file_by_id(document_id)
        except Exception as e:
            error = f"Error eliminando documento de la base de datos: {
                str(e)}", 500

    if error:
        flash("Error al eliminar el archivo!", "danger")
    else:
        flash("Archivo eliminado con éxito", "success")
    return redirect(url_for("riders.showFiles", dni=dni))


@bp.post("/archivos/cargar_link/<int:dni>")
@login_and_permission_required("rider_submit_files")
def submit_links(dni):
    """
    Cargar un enlace.
    """
    link = request.form.get("link")
    tipo = request.form.get('tipo_link')
    error = None
    if not link:
        error = "El enlace no puede estar vacío."
    if not error:
        try:
            link_uploader(link, dni, tipo)
            flash("Enlace cargado con éxito", "success")
        except Exception as e:
            error = f"Error al cargar el enlace: {str(e)}"

    if error:
        flash(error, "error")

    return redirect(url_for("riders.showFiles", dni=dni))
