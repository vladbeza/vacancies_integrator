# -*- coding:utf-8 -*-

from integrator import create_app, make_celery
from integrator.models import db, City, Job
from integrator.retrieve_info import gather_new_jobs_dou
from flask_migrate import Migrate
from integrator.scripts import remove_duplicates

CITIES = ["Харьков", "Киев", "Одесса", "Львов", "Другой"]

app = create_app()
migrate = Migrate(app, db)

with app.app_context():
    for c in CITIES:
        city = db.session.query(City).filter(City.name == c).first()
        if city is None:
            city = City(name=c)
            db.session.add(city)
            db.session.commit()

    jobs = db.session.query(Job).all()
    if not jobs:
        gather_new_jobs_dou()


celery = make_celery(app)


@celery.task
def gather_dou_jobs_task():
    gather_new_jobs_dou()


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
        }
}

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, City=City)
