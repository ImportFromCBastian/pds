from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from src.core import auth
from src.web.handlers.auth import not_logued_required
from authlib.integrations.flask_client import OAuth
import os
import binascii
from src.web.controllers import user_provisorio


@not_logued_required
def login():
    return render_template("auth/login.html")

def login_send(): 
    email=session.get('new_user_email')
    if email:
        if not user_provisorio.find_by_email(email) and not auth.find_user_by_email(email):
            user_provisorio.create(email)
        flash("espere a que un administrador lo registre", "success")
    session.pop('new_user_email', None)
    return redirect(url_for("login"))


@not_logued_required
def authenticate():

    params = request.form
    user = auth.check_user(params["email"], params["contrasenia"])

    if not user:
        flash("email o contraseña incorrecta 😢", "error")

        return redirect(url_for("login"))
    elif user.bloqueado:
        flash("Su usuario está bloqueado 😢", "error")

        return redirect(url_for("login"))

    session["user"] = user.email
    flash("Inicio de sesion exitoso, Bienvenido🎉", "success")

    return redirect(url_for("home.landing"))

oauth = OAuth()
def configure_oauth(app):
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.init_app(app)
    oauth.register(
        name='google',
        server_metadata_url=CONF_URL,
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

def generate_nonce():
    return binascii.hexlify(os.urandom(16)).decode()

@not_logued_required
def google_login():
    """Redirige al usuario para iniciar sesión con Google"""
    redirect_uri = url_for('google_auth', _external=True)

    nonce = generate_nonce()
    session['nonce'] = nonce

    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

@not_logued_required
def google_auth():
    """Recibe el token de Google y lo valida en la sesión"""
    token = oauth.google.authorize_access_token() 

    nonce = session.pop('nonce', None)

    if not nonce:
        flash("Error: nonce no encontrado en la sesión", "error")
        return redirect(url_for("login"))

    try:
        userinfo = oauth.google.parse_id_token(token, nonce=nonce) 
        email = userinfo.get('email')

        if email:
            user = auth.find_user_by_email_not_blocked(email) 

            if user:
                session["user"] = user.email
                flash("Inicio de sesión exitoso, Bienvenido🎉", "success")
            else:
                session['new_user_email'] = email
                flash("Usuario no encontrado, ¿desea registrarse?", "warning")
                return redirect(url_for("login"))
        else:
            flash("No se pudo obtener el email de Google", "error")
            return redirect(url_for("login"))

    except Exception as e:
        flash(f"Error al validar el ID Token: {str(e)}", "error")
        return redirect(url_for("login"))

    return redirect(url_for('home.landing'))

@not_logued_required
def cancel_registration():
    session.pop('new_user_email', None)
    return redirect(url_for("login"))
