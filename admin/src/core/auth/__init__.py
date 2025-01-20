from src.core.database import db
from src.core.bcrypt import bcrypt
from src.core.models.users_module.user import Usuario


def list_users():
    users = Usuario.query.all()

    return users


def create_user(**kwargs):
    user = Usuario(**kwargs)

    db.session.add(user)
    db.session.commit()

    return user


def find_user_by_email(email):
    user = Usuario.query.filter_by(borrado=False).filter_by(email=email).first()
    return user

def find_user_by_email_not_blocked(email):
    user = Usuario.query.filter_by(borrado=False).filter_by(bloqueado=False).filter_by(email=email).first()
    return user


def check_user(email, contrasenia):
    user = find_user_by_email(email)

    # if user and user.contrasenia == contrasenia: #esto es temporal, hasta que se guarden las contraseñas encriptadas, por ahora se guardan en texto plano, cuando se guarden encriptadas se descomenta la linea de arriba y se borra esta
    if user and bcrypt.check_password_hash(user.contrasenia, contrasenia):
        return user

    return None
