from flask import jsonify
from datetime import datetime
from flask import Blueprint, request
from src.core.models.content import content_index_api, get_by_id
from src.web.schemas.article import ArticleSchema, DetailedArticleSchema

bp = Blueprint("content_api", __name__, url_prefix="/api/articles")


def parse_date(date_str):
    """ Helper function to parse date from string """
    if date_str:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None
    return None


def error_response(message):
    """
    Helper function to return a standardized 400 error response.
    """
    response = jsonify({"error": message})
    response.status_code = 400
    return response


@bp.get("/")
def index():
    """
    Lists content in the system.
    """
    author = request.args.get('author', type=str)
    published_from = request.args.get('published_from', type=str)
    published_to = request.args.get('published_to', type=str)
    published_from = parse_date(published_from)
    published_to = parse_date(published_to)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    if published_from and published_to and published_from > published_to:
        return error_response("Desde no puede ser mayor que hasta.")

    if page < 1 or per_page < 1:
        return error_response("Los parámetros de paginación deben ser mayores o iguales a 1.")

    content_data = content_index_api(
        author=author,
        published_from=published_from,
        published_to=published_to,
        page=page,
        per_page=per_page
    )

    data = ArticleSchema(many=True).dump(content_data['items'])
    response = {
        "data": data,
        "total": content_data['total'],
        "page": page,
        "per_page": per_page,
    }
    return response, 200


@bp.get("/<int:article_id>")
def get_article(article_id):
    """
    Get details of a single article.
    """

    article = get_by_id(article_id)

    if not article:
        return {"error": "Articulo no encontrado"}, 400

    data = DetailedArticleSchema().dump(article)

    return {"data": data}, 200
