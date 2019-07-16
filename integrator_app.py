# -*- coding:utf-8 -*-
import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from integrator import create_app, make_celery
from integrator.models import db, City, Job, Language
from integrator.retrieve_info_djinni import get_new_jobs_djinni
from integrator.retrieve_info_dou import gather_new_jobs_dou
from flask_migrate import Migrate, upgrade
from integrator.scripts import remove_duplicates

app = create_app()
migrate = Migrate(app, db)
celery = make_celery(app)


@celery.task
def gather_dou_jobs_task():
    gather_new_jobs_dou()


@celery.task
def gather_djinni_jobs_task():
    get_new_jobs_djinni()


@celery.task
def remove_duplicates_task():
    remove_duplicates()


celery.conf.beat_schedule = {
    "gather_dou_jobs_task": {
        "task": "integrator_app.gather_dou_jobs_task",
        "schedule": 3600
    },
    "remove_duplicates_task": {
            "task": "integrator_app.remove_duplicates_task",
            "schedule": 1800
    },
    "gather_djinni_task": {
            "task": "integrator_app.gather_djinni_jobs_task",
            "schedule": 3600
    }
}


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, City=City, Language=Language, Job=Job)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

    City.add_cities()
    Language.add_langs()

    # with app.app_context():
    #     jobs = db.session.query(Job).all()
    #     if not jobs:
    #         gather_new_jobs_dou()
    #         get_new_jobs_djinni()
