from src.core.models.contact_module.contact import PortalQuery
from src.core.models.contact_module.contact import QueryState
from src.core.models.contact_module import query_index
from flask import render_template, request, redirect, url_for, flash, Blueprint, jsonify
from src.web.handlers.auth import login_and_permission_required
from src.web.schemas.contact_module import create_portal_query_schema, return_portal_query_schema
from datetime import datetime
import os
from dotenv import load_dotenv
import requests


bp = Blueprint("contact_module_api", __name__, url_prefix="/api/messages")


@bp.post("/")
def load_portal_query():
    """Loads in the system a portal query if its fields are correct"""
    partial_query = request.get_json()

    recaptcha_response = partial_query.pop("recaptcha", None)
    if not verify_recaptcha(recaptcha_response):
        return jsonify({"recaptcha": "Verificación de reCAPTCHA fallida"}), 400
    
    errors = create_portal_query_schema.validate(partial_query)
    if errors:
        return jsonify(errors), 400

    kwargs = create_portal_query_schema.load(partial_query)
    query = PortalQuery.create_query(**kwargs)
    
    if query["info"] == {}:
        return jsonify(return_portal_query_schema.dump(query["portal_query"])), 201
    else:
        return jsonify(query["info"]), 400
    
    
def verify_recaptcha(recaptcha_response):
    """Verifies the token of reCAPTCHA received from the portal"""
    load_dotenv()
    secret_key = os.environ.get("CAPTCHA_SECRET_KEY")
    recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": secret_key,
        "response": recaptcha_response,
    }
    response = requests.post(recaptcha_url, data=payload)
    result = response.json()
    return result.get("success", False)