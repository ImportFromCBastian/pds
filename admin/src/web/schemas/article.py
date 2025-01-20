from marshmallow import Schema, fields


class ArticleSchema(Schema):
    id = fields.Int(required=True)
    titulo = fields.Str(required=True)
    copete = fields.Str(required=True)
    fecha_publicacion = fields.DateTime(required=True)
    autor = fields.Str(required=True, attribute="autor.alias")


class DetailedArticleSchema(Schema):
    id = fields.Int(required=True)
    titulo = fields.Str(required=True)
    copete = fields.Str(required=True)
    fecha_publicacion = fields.DateTime(required=True)
    autor = fields.Str(required=True, attribute="autor.alias")
    contenido = fields.Str(required=True)


detaild_article_schema = DetailedArticleSchema()
articles_schema = ArticleSchema(many=True)
