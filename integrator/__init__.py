import logging

from celery import Celery
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from integrator.models import db, City, Language
from integrator.retrieve_info_djinni import get_new_jobs_djinni
from integrator.retrieve_info_dou import gather_new_jobs_dou
from integrator.views import blueprints

bootstrap = Bootstrap()


def create_app():
    logging.warning("Creating flask application")
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    db.create_all(app=app)
    bootstrap.init_app(app)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    with app.app_context():
        City.add_cities()
        Language.add_langs()
        gather_new_jobs_dou()
        get_new_jobs_djinni()

    return app


def make_celery(app):
    logging.warning("Making celery context")
    celery = Celery(
        app.import_name,
        backend=Config.result_backend,
        broker=Config.broker_url
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    logging.warning("Celery making done")
    return celery
