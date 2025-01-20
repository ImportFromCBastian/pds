from flask import render_template, request, redirect, url_for, flash, Blueprint
from src.web.handlers.auth import login_and_permission_required
from src.core.models import get_users_filtered
from src.core.models import Rol
from src.core.models import Usuario
from src.core.bcrypt import bcrypt
from src.web.controllers.users_module.handlers.validators.validator import validate_partial_user, validate_user


bp = Blueprint("modulo_usuarios", __name__, url_prefix="/modulo_usuarios")


@bp.route("/listado", methods=["GET", "POST"])
@login_and_permission_required("user_index")
def listado():
    """Shows all the users in pages"""

    sort_column = request.args.get("sort_column", "creado_en")
    sort_order = request.args.get("sort_order", "desc")

    email = request.args.get("email", None)
    rol_id = request.args.get("role", None)
    bloqueado = request.args.get("bloqueado", None)
    page = request.args.get('page_receive', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    users = get_users_filtered(
        page, per_page, sort_column, sort_order, email, rol_id, bloqueado
    )

    roles = Rol.get_roles()

    return render_template(
        "users_module/index.html",
        page=page,
        per_page=per_page,
        users=users,
        roles=roles,
        current_sort_column=sort_column,
        current_sort_order=sort_order,
    )


@bp.route("/actualizar_usuario/<email>", methods=["GET", "POST"])
@login_and_permission_required("user_update")
def actualizar_usuario(email: str):
    """Modifies the info of the user sended"""
    user = Usuario.get_user(email)
    roles = Rol.get_roles()

    if request.method == "GET":
        return render_template("users_module/index_update.html", user=user, roles=roles)

    elif request.method == "POST":
        data = request.form.to_dict()
        
        is_valid = validate_partial_user(data)
        
        if is_valid["valid"]:
            changed = user.update_user(**data)
            if changed == {}:
                flash(
                    f"No se han actualizado los datos del usuario con email {email}", "info"
                )
            else:
                flash(f"Se actualizaron los datos del usuario con email {email}", "info")
        else:
            for error in is_valid["errors"]:
                flash(f'{error["msg"]}', "error")
        
        return redirect(url_for("modulo_usuarios.listado"))


@bp.route("/mostrar_usuario/<email>", methods=["GET", "POST"])
@login_and_permission_required("user_show")
def mostrar_usuario(email: str):
    """Shows the info of the user sended"""
    user = Usuario.get_user(email)
    roles = Rol.get_roles()

    return render_template("users_module/index_show.html", user=user, roles=roles)


@bp.route("/crear_usuario", methods=["GET", "POST"])
@login_and_permission_required()
def crear_usuario():
    """Creates a new user with the data charged"""
    roles = Rol.get_roles()

    if request.method == "GET":
        return render_template("users_module/create_user.html", roles=roles)
    elif request.method == "POST":
        data = request.form.to_dict()
        
        is_valid = validate_user(data)
        print(is_valid["errors"])
        if is_valid["valid"]:
            created_user = Usuario.create_user(
                email=data.get("email"),
                contrasenia=bcrypt.generate_password_hash(data.get("password")).decode("utf-8"),
                alias=data.get("alias"),
                rol_id=data.get("rol_id"),
                system_admin=(data.get("system_admin") == "True"),
                bloqueado=(data.get("bloqueado") == "False"),
            )

            if created_user:
                flash(
                    f"Se creó al usuario con email {data.get("email")}", "success"
                )
        else:
            for error in is_valid["errors"]:
                flash(f'{error["msg"]}', "error")

        return redirect(url_for("modulo_usuarios.listado"))


@bp.route("/eliminar_usuario/<email>", methods=["GET", "POST"])
@login_and_permission_required()
def eliminar_usuario(email: str):
    """Deletes a user permanently"""
    if Usuario.delete_user(email):
        flash(f"Se elimino al usuario con email {email}", "info")
    else:
        flash(f"No se pudo eliminar al usuario con email {email}", "error")
    return redirect(url_for( "modulo_usuarios.listado"))


@bp.route("/cambiar_estado_usuario/<email>", methods=["GET", "POST"])
@login_and_permission_required()
def cambiar_estado_usuario(email: str):
    """Togles the user status"""
    if Usuario.togle_status(email):
        if Usuario.bloqueado:
            flash(f"Se bloqueó al usuario con email {email}", "info")
        else:
            flash(f"Se desbloqueó al usuario con email {email}", "info")
    else:
        flash(f"No se pudo cambiar el estado al usuario con email {email}", "error")
    return redirect(url_for("modulo_usuarios.listado"))
