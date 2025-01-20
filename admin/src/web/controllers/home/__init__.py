from flask import render_template, flash, redirect, url_for, session, Blueprint
from src.web.handlers.auth import login_required
from src.core.models.users_module.user import Usuario
from src.core.models.users_module.role import Rol
from src.web.controllers.home.handler import convert_role_naming

bp = Blueprint("home", __name__, url_prefix="/home")


@bp.get("/")
@login_required
def landing():
    user = session.get("user")
    role = Usuario.get_user_rol_by_email(user)
    db_user = Usuario.get_user(user)
    name = db_user.alias
    system_admin = db_user.system_admin
    permissions = Rol.get_role_permissions_by_name(role)
    translated_permissions = convert_role_naming(permissions)
    return render_template(
        "landing.html",
        role=role,
        name=name,
        permissions=translated_permissions,
        system_admin=system_admin,
    )


@bp.get("/logout")
@login_required
def logout():
    if session.get("user"):
        session.pop(
            "user", None
        )
        session.clear()

        flash("Sesion cerrada exitosamente ✨", "info")
    else:
        flash("No hay ninguna sesion activa 👺", "error")

    return redirect(url_for("login"))
