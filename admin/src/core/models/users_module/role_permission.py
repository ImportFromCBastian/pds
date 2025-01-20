from src.core.database import db

role_permission = db.Table(
    "Rol-Permiso",
    db.Column("rol_id", db.Integer, db.ForeignKey("Rol.id"), primary_key=True),
    db.Column("permiso_id", db.Integer, db.ForeignKey("Permiso.id"), primary_key=True),
)
"""Intermediate table between Rol and Permiso"""
