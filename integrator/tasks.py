import celery

from integrator.retrieve_info import gather_new_jobs_dou


@celery.task()
def gather_dou_jobs_task():
    gather_new_jobs_dou()
