from flask import Blueprint
from src.core.models import teams
from src.core.models.teams.employee import ProfessionType
from src.core.models.teams.employee import PositionType
from src.core.models.teams.employee import ConditionType
from flask import Blueprint, render_template, request, flash, redirect, url_for
from web.controllers.teams.handlers.validators.validator import (
    validate_user,
    validate_partial_user,
)
from web.controllers.teams.handlers.search import filter_team_members
from src.web.controllers.teams.handlers.files import file_uploader
from src.web.controllers.teams.handlers.files.get_links import get as get_documents
from src.web.handlers.auth import login_and_permission_required

bp = Blueprint("teams", __name__, url_prefix="/equipo")


@bp.get("/")
@login_and_permission_required("team_index")
def index():
    """
    Shows the index of the teams
    """
    args = request.args.to_dict()

    page = int(args.get("page", 1))
    per_page = int(args.get("per_page") if args.get("per_page") else 5)

    sort_field = args.get("sort_field", "fecha_inicio")
    sort_order = args.get("sort_order", "desc")

    if args:
        filtered_result = filter_team_members(
            teams.team_index(), args, page=page, per_page=per_page
        )
        team = filtered_result["members"]
        pagination = filtered_result["pagination"]

        if not team:
            return render_template(
                "teams/index.html",
                team=team,
                positions=PositionType,
                empty=True,
                args=args,
                pagination=pagination,
            )

        if sort_field:
            team.sort(
                key=lambda x: (
                    getattr(x, sort_field).value
                    if isinstance(getattr(x, sort_field), PositionType)
                    else getattr(x, sort_field)
                ),
                reverse=(sort_order == "desc"),
            )

        return render_template(
            "teams/index.html",
            team=team,
            positions=PositionType,
            args=args,
            pagination=pagination,
        )

    else:
        filtered_result = filter_team_members(
            teams.team_index(),
            {"sort_field": sort_field, "sort_order": sort_order},
            page=page,
            per_page=per_page,
        )
        team = filtered_result["members"]
        pagination = filtered_result["pagination"]

        return render_template(
            "teams/index.html",
            team=team,
            positions=PositionType,
            args={"sort_order": "desc", "sort_field": "fecha_inicio"},
            pagination=pagination,
        )


@bp.get("/detalles/<int:dni>")
@login_and_permission_required("team_update")
def show(dni):
    """
    Shows the details of a team member.
    """

    team_member = teams.search_by_dni(dni)

    documents = get_documents(dni)

    return render_template("teams/show.html", member=team_member, documents=documents)


@bp.post("/detalles/<int:dni>")
@login_and_permission_required("team_submit_files")
def submit_files(dni):
    """
    Submit files for a team member.
    """
    files = request.files

    team_member = teams.search_by_dni(dni)

    error = file_uploader(files, team_member)

    documents = get_documents(dni)

    if error:
        return render_template(
            "teams/show.html",
            member=team_member,
            documents=documents,
            errors=error,
        )

    return render_template(
        "teams/show.html",
        member=team_member,
        documents=documents,
        success="Archivo subido con éxito",
    )


@bp.get("/agregar")
@login_and_permission_required("team_new")
def new():
    """
    Shows the create form for a new team member.
    """

    return render_template(
        "teams/new.html",
        professions=ProfessionType,
        positions=PositionType,
        conditions=ConditionType,
        errors={},
    )


@bp.post("/agregar")
@login_and_permission_required("team_new")
def create():
    """
    Create a new team member.
    """
    params = request.form

    is_valid = validate_user(params)
    errors = {}
    if not is_valid["valid"]:
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]

        return render_template(
            "teams/new.html",
            professions=ProfessionType,
            positions=PositionType,
            conditions=ConditionType,
            errors=errors,
        )

    params = params.to_dict()
    params["activo"] = True if params.get("activo") == "on" else False

    new_team_member = teams.team_create(**params)

    flash("Miembro creado con éxito", "success")
    return redirect(url_for("teams.index"))


@bp.get("/editar/<int:dni>")
@login_and_permission_required("team_edit")
def edit(dni):
    """
    Shows the edit form for a team member.
    """
    team_member = teams.search_by_dni(dni)

    return render_template(
        "teams/edit.html",
        member=team_member,
        professions=ProfessionType,
        positions=PositionType,
        conditions=ConditionType,
    )


@bp.post("/editar/<int:dni>")
@login_and_permission_required("team_update")
def update(dni):
    """
    Update a team member.
    """
    team_member = teams.search_by_dni(dni)

    params = request.form.to_dict()

    params["numero_emergencia"] = (
        int(params.get("numero_emergencia")) if params.get(
            "numero_emergencia") else 0
    )
    params["activo"] = True if params.get("activo") == "on" else False
    is_valid = validate_partial_user(params)
    errors = {}
    if not is_valid["valid"]:
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]

        return render_template(
            "teams/edit.html",
            member=team_member,
            professions=ProfessionType,
            positions=PositionType,
            conditions=ConditionType,
            errors=errors,
        )

    updated_team_member = teams.team_update(dni, params)

    team = teams.team_index()

    flash(
        f"Miembro del equipo con email {
            team_member.email} actualizado con éxito",
        "success",
    )
    return redirect(url_for("teams.index"))
