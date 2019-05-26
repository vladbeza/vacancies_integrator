from celery import Celery
from integrator.retrieve_info import gather_new_jobs_dou
from integrator.models import db

celery = Celery(__name__,
                backend="redis://localhost:6379",
                broker="redis://localhost:6379")

_APP = None


@celery.task
def gather_jobs_task():
    global _APP
    # lazy init
    if _APP is None:
        from integrator import create_app
        app = create_app()
        db.init_app(app)
    else:
        app = _APP

    with app.app_context():
        gather_new_jobs_dou()


celery.conf.beat_schedule = {
    "gather_jobs_task": {
        "task": "gather_jobs_task",
        "schedule": 3600
    }
}
