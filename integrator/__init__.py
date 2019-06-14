from celery import Celery
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
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


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend="redis://127.0.0.1:6379",
        broker="redis://127.0.0.1:6379"
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

