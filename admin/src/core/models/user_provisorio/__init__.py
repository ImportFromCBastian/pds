from src.core.models.user_provisorio.user_provisorio import UserProvisorio
from src.core.database import commit_db, delete_from_db

def user_provisorios_index():
    """
    List all the provisory users.
    """
    return UserProvisorio.query.all()

def user_provisorio_find_by_email(email):
    """
    Find a provisory user by email.
    """
    return UserProvisorio.query.filter_by(email=email).first()

def user_provisorio_create(email):
    """
    Create a new provisory user.
    """
    user = UserProvisorio(email=email)
    commit_db(user)
    return user

def user_provisorio_delete(email):
    """
    Delete a provisory user by email.
    """
    user = UserProvisorio.query.filter_by(email=email).first()
    delete_from_db(user)
    return user
