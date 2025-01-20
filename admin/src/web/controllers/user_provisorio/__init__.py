from src.core.models import user_provisorio 
from flask import Blueprint
from flask import render_template, request,flash, redirect, url_for
from src.core.bcrypt import bcrypt
from src.core.models import Rol
from src.core.models import Usuario
from src.web.controllers.users_module.handlers.validators.validator import validate_user
import string
import random

bp = Blueprint("provisorio", __name__, url_prefix="/provisorio")

@bp.get("/")
def index():
    """
    List all the provisory users.
    """
    users=user_provisorio.user_provisorios_index()
    return render_template("provisorio/index.html", users=users)

@bp.get("/find")
def find_by_email(email):
    """
    Find a provisory user by email.
    """
    return user_provisorio.user_provisorio_find_by_email(email)

@bp.post("/crearProvisorio")
def create(email):
    """
    Create a new provisory user.
    """
    user = user_provisorio.user_provisorio_create(email)
    return user

@bp.post("/borrarProvisorio/<email>")
def delete(email):
    """
    Delete a provisory user by email.
    """
    user_provisorio.user_provisorio_delete(email)
    users=user_provisorio.user_provisorios_index()
    return render_template("provisorio/index.html", users=users) 

@bp.get("/crearUsuario/<email>")
def new_usuario(email):
    """
    Create a provisory user by email.
    """
    return render_template("provisorio/create.html", email=email, roles=Rol.get_roles(), random_password=generar_contraseña_aleatoria())

@bp.post("/crearUsuario")
def crear_usuario():
    """
    Create a provisory user by email.
    """
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
            user_provisorio.user_provisorio_delete(data.get("email"))
            flash(
                f"Se creó al usuario con email {data.get("email")}", "success"
            )
    else:
        for error in is_valid["errors"]:
            flash(f'{error["msg"]}', "error")
    
    return redirect(url_for("provisorio.index"))


def generar_contraseña_aleatoria(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(longitud))
