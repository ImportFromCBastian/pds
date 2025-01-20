from src.core.models import Usuario
from src.core.models import Rol
from src.core.models import Permiso
from src.core.bcrypt import bcrypt


def create_users():
    """
    Create a seed of new users.
    """

    user1 = Usuario.create_user(
        email="starsky@gmail.com",
        contrasenia=bcrypt.generate_password_hash("Torino537").decode("utf-8"),
        alias="Red Tomato",
        rol_id=2,
        system_admin=False,
    )
    user2 = Usuario.create_user(
        email="generalLee@gmail.com",
        contrasenia=bcrypt.generate_password_hash(
            "Charger320").decode("utf-8"),
        alias="DukeBoys",
        rol_id=1,
        system_admin=True,
        bloqueado=True,
    )
    user3 = Usuario.create_user(
        email="KITT2000@gmail.com",
        contrasenia=bcrypt.generate_password_hash(
            "Firebird1982").decode("utf-8"),
        alias="KITT",
        rol_id=4,
        bloqueado=False,
        system_admin=True,
    )
    user4 = Usuario.create_user(
        email="pepe@gmail.com",
        contrasenia=bcrypt.generate_password_hash("Olivia123").decode("utf-8"),
        alias="pepe",
        rol_id=1,
        system_admin=False,
        bloqueado=False,
    )
    user5 = Usuario.create_user(
        email="aaaa@gmail.com",
        contrasenia=bcrypt.generate_password_hash("Valorant").decode("utf-8"),
        alias="chichon",
        rol_id=4,
        system_admin=False,
        bloqueado=False,
    )
    user6 = Usuario.create_user(
        email="ornitorrinco@gmail.com",
        contrasenia=bcrypt.generate_password_hash("Perri").decode("utf-8"),
        alias="agenteP",
        rol_id=2,
        system_admin=False,
        bloqueado=False,
    )
    user7 = Usuario.create_user(
        email="josemartinezosti@gmail.com",
        contrasenia=bcrypt.generate_password_hash(
            "Contraseña").decode("utf-8"),
        alias="Jose",
        rol_id=1,
        system_admin=True,
        bloqueado=False,
    )
