# -*- coding:utf-8 -*-
import re

from flask import render_template, Blueprint
from integrator.config import languages
from integrator.forms import FilterJobsForm
from integrator.models import Job, City
from integrator.tasks import gather_jobs_task

jobs = Blueprint('jobs', __name__)

def render_jobs(active):
    form = FilterJobsForm()

    active_vacancies_query = Job.query.filter_by(active=active)

    if form.validate_on_submit():
        city = form.city.data
        language = form.language.data
        is_automation = form.automation_only.data
        is_remote = form.remote_only.data

        if is_remote:
            active_vacancies_query = active_vacancies_query.filter_by(
                remote=True)

        if city != "Any":
            active_vacancies = active_vacancies_query.join(
                Job.cities).filter_by(id=int(city))
        else:
            active_vacancies = active_vacancies_query.all()

        active_vacancies = filter_automation(active_vacancies, is_automation)

        if language != "Any":
            active_vacancies = filter_language(active_vacancies, language)

    else:
        # gather_jobs_task.delay()
        active_vacancies = active_vacancies_query.all()
        form.city.data = "Any"
        form.language.data = "Any"

    return render_template('index.html', jobs=active_vacancies, form=form)


@jobs.route("/", methods=['GET', 'POST'])
def index():
    return render_jobs(True)


@jobs.route("/history", methods=['GET', 'POST'])
def history():
    return render_jobs(False)


def filter_automation(jobs_list, automation):
    key_words = [r"\bautomation\b",
                 r"\bin test\b",
                 r"\bавтоматизация\b",
                 r"\bавтоматизиронный\b"]
    if automation:
        return [job for job in jobs_list if
                any(re.search(word, job.title.decode("utf-8").lower())
                    is not None for word in key_words)]

    return jobs_list


def filter_language(jobs_list, language):
    if language == "JavaScript":
        langs = ["JavaScript", "js"]
    else:
        langs = [language]
    return [job for job in jobs_list if any(l.lower() in
            job.title.decode("utf-8").lower() for l in langs)
            or any(l.lower() in job.description.lower() for l in langs)]
