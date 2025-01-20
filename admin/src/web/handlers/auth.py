from functools import wraps
from flask import session
from flask import redirect, render_template
from flask import url_for
from flask import abort
from src.core.models.users_module.user import Usuario


def is_authenticated(session):
    return session.get("user") is not None


def is_system_admin(session):
    """Checks if the user in the session is a system admin"""
    return Usuario.is_system_admin(session.get("user"))


def check_permission(session, permission: str):
    """Checks if the user in the session has the permission sended"""
    return Usuario.has_permission(session.get("user"), permission)


def not_logued_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if is_authenticated(session):
            return redirect(url_for("home.landing"))
        return f(*args, **kwargs)

    return wrapper


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated(session):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper


def get_logged_in_user():
    """Retorna el usuario logueado actualmente"""
    user_data = session.get("user")
    if user_data:
        return user_data
    return None


def login_and_permission_required(permission=None):
    """Combines login_required, is_system_admin and check_permission logic"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # First, check if the user is authenticated
            if not is_authenticated(session):
                return redirect(url_for("login"))

            # Then, check if the user is a system admin or has the required permission
            if is_system_admin(session):
                return f(*args, **kwargs)

            if permission:
                if not check_permission(session, permission):
                    return abort(401)
            else:
                return redirect(url_for("home.landing"))

            return f(*args, **kwargs)

        return wrapper

    return decorator
