
from flask import Flask, redirect, url_for
from .config import Config
from .extensions import db, migrate
from .views.core import core_bp
from .views.client_config import config_bp
from .views.site_manage import site_bp

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(core_bp)
    app.register_blueprint(config_bp, url_prefix="/config")
    app.register_blueprint(site_bp)

    @app.route("/")
    def index():
        return redirect(url_for("core.list_clients"))

    return app
