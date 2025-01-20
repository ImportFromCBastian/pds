from marshmallow import Schema, fields, ValidationError, post_load
from datetime import datetime

def withoutSpaces(value: str):
    if not value.strip():
        raise ValidationError("No se puede ingresar un texto vacío")


class PortalQuerySchema(Schema):
    """Schema of a portal query to load from or send data to the portal"""
    titulo = fields.Str(required=True, validate=withoutSpaces)
    email = fields.Email(required=True)
    descripcion = fields.Str(required=True, validate=withoutSpaces)
    estado = fields.Str(dump_only=True)
    created_at = fields.Str(dump_only=True)
    closed_at = fields.Str(dump_only=True)

    @post_load
    def add_defaults(self, data, **kwargs):
        """Add default values for fields that are not loaded"""
        data["estado"] = "Creada"
        data["created_at"] = datetime.now().strftime("%Y-%m-%d")
        data["closed_at"] = datetime.now().strftime("%Y-%m-%d")
        return data


create_portal_query_schema = PortalQuerySchema(only=("titulo", "email", "descripcion"))
return_portal_query_schema = PortalQuerySchema()