from src.web.controllers.auth import login as control_login
from src.web.controllers.auth import authenticate as control_authenticate
from src.web.controllers.auth import google_login as control_google_login
from src.web.controllers.auth import google_auth as control_google_auth
from src.web.controllers.auth import login_send as control_login_send
from src.web.controllers.auth import cancel_registration as control_login_cancel_send
from web.controllers.home import bp as home_bp
from src.web.controllers.users_module import bp as users_module_bp
from src.web.controllers.teams import bp as teams_bp
from src.web.controllers.payments import bp as payments_bp
from src.web.controllers.charges_module import bp as charges_module_bp
from src.web.controllers.riders import bp as riders_bp
from src.web.controllers.equestrian import bp as equestrian_bp
from src.web.controllers.charts import bp as charts_bp
from src.web.controllers.reports import bp as reports_bp
from src.web.controllers.content import bp as content_bp
from src.web.api.content import bp as content_api
from src.web.controllers.contact_module import bp as contact_module_bp
from src.web.api.contact_module import bp as contact_module_api_bp
from src.web.controllers.user_provisorio import bp as user_provisorio_bp


def register(app):

    @app.route("/")
    def login():
        return control_login()

    @app.route("/authenticate", methods=["POST"])
    def authenticate():
        return control_authenticate()
    
    @app.route("/send")
    def login_send():
        return control_login_send()
    
    @app.route("/login-google")
    def google_login():
        return control_google_login()
    
    @app.route("/login/callback")
    def google_auth():
        return control_google_auth()
    
    @app.route("/cancel-registration")
    def cancel_registration():
        return control_login_cancel_send()

    app.register_blueprint(home_bp)
    app.register_blueprint(users_module_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(charges_module_bp)
    app.register_blueprint(riders_bp)
    app.register_blueprint(equestrian_bp)
    app.register_blueprint(charts_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(content_api)
    app.register_blueprint(contact_module_bp)
    app.register_blueprint(contact_module_api_bp)
    app.register_blueprint(user_provisorio_bp)
