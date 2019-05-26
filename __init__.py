from flask import Flask
from flask_bootstrap import Bootstrap
from integrator.config import Config
from integrator.models import db
from integrator.views import blueprints

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    db.create_all(app=app)
    bootstrap.init_app(app)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    return app
