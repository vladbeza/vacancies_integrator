# -*- coding:utf-8 -*-
import re

from flask import render_template, Blueprint
from integrator.forms import FilterJobsForm
from integrator.models import Job

jobs = Blueprint('jobs', __name__)


def render_jobs(active):
    form = FilterJobsForm()

    active_vacancies_query = Job.query.filter_by(active=active)

    if form.validate_on_submit():
        city = form.city.data
        language = form.language.data
        is_automation = form.automation_only.data
        is_remote = form.remote_only.data
        known_salary = form.known_salary.data
        salary_more_than = form.salary_more.data

        if is_remote:
            active_vacancies_query = active_vacancies_query.filter_by(
                remote=True)

        if known_salary or salary_more_than:
            active_vacancies_query = active_vacancies_query.filter(
                Job.salary != None)

        if city != "Any":
            active_vacancies = active_vacancies_query.join(
                Job.cities).filter_by(id=int(city))
        else:
            active_vacancies = active_vacancies_query.all()

        active_vacancies = filter_automation(active_vacancies, is_automation)

        if language != "Any":
            active_vacancies = filter_language(active_vacancies, language)

        if salary_more_than:
            active_vacancies = filter_by_salary(active_vacancies,
                                                salary_more_than)

    else:
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


def filter_by_salary(jobs_list, expected_salary):
    result = []
    for job in jobs_list:
        salary = re.findall("([0-9]+)", job.salary)
        if salary:
            salary = max([int(s) for s in salary])
            if salary >= expected_salary:
                result.append(job)
    return result


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
        langs = [r"\bjavascript\b", r"\bjs\b"]
    else:
        langs = [r"\b{}\b".format(language.lower())]

    return [job for job in jobs_list if
            any(re.search(l, job.title.decode("utf-8").lower()) for l in langs)
            or any(re.search(l,
                      job.description.lower()) for l in langs)]
