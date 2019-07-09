# -*- coding:utf-8 -*-
import re

from datetime import datetime
from flask import render_template, Blueprint

from config import languages
from integrator.forms import FilterJobsForm, SkillsForm
from integrator.models import Job
from integrator.utils import create_dates_range, group_by_month_and_get_series

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
        use_dou = form.use_dou_stats.data
        use_djinni = form.use_djinni.data

        if is_remote:
            active_vacancies_query = active_vacancies_query.filter_by(
                remote=True)

        if not use_dou:
            active_vacancies_query = active_vacancies_query.filter_by(
                dou_id=None)

        if not use_djinni:
            active_vacancies_query = active_vacancies_query.filter_by(
                djinni_id=None)

        if known_salary or salary_more_than:
            active_vacancies_query = active_vacancies_query.filter(
                Job.salary != None)

        if city != "Any":
            active_vacancies = active_vacancies_query.join(
                Job.cities).filter_by(id=int(city)).all()
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


@jobs.route("/history/graphics", methods=['GET'])
def more_graphics():
    all_jobs = Job.query.all()

    min_job_date, max_job_date = min(all_jobs, key=lambda x: x.created),\
                         max(all_jobs, key=lambda x: x.created)

    dates_range = create_dates_range(min_job_date.created,
                                     max_job_date.created)
    months_categories = [month.strftime("%b %y") for month in dates_range]

    dates = [j.created for j in all_jobs]
    series_data = group_by_month_and_get_series(dates, dates_range)
    common_series = [{"name": "jobs",
                      "data": series_data}]

    language_series = []
    for l in languages:
        if l != "Any":
            jobs = filter_language(all_jobs, l)
            series_for_lang = group_by_month_and_get_series(
                [j.created for j in jobs], dates_range)
            language_series.append({"name": l, "data": series_for_lang})

    return render_template("graphics.html",
                           month_categories=months_categories,
                           common_series=common_series,
                           language_series=language_series)


@jobs.route("/needed_skills", methods=['GET', 'POST'])
def most_needed_skills():
    form = SkillsForm()
    if form.validate_on_submit():
        skills_set = form.skills_list.data
        start_date = form.from_date.data
        end_date = form.to_date.data

        vacancies_query = Job.query.filter(
            Job.created >= start_date).filter(Job.created <= end_date).all()
        skills_info = filter_by_skills_required(vacancies_query, skills_set)
        skills_categories = sorted(skills_info.keys())

        month_categories,\
        month_skills_series = prepare_data_for_skills_timeseries(
            skills_info, start_date, end_date
        )

        return render_template('skills.html',
                               skills_info=skills_info,
                               form=form,
                               scroll="skills",
                               skills_categories=skills_categories,
                               skills_count_series=prepare_data_for_skills_histogram(
                                   skills_categories,
                                   skills_info),
                               month_categories=month_categories,
                               month_skills_series=month_skills_series)
    else:
        return render_template('skills.html',
                               skills_info={},
                               form=form,
                               scroll=None)


def prepare_data_for_skills_timeseries(skills_info,
                                       start_date,
                                       end_date):
    dates_range = create_dates_range(start_date, end_date)
    categories = [month.strftime("%b %y") for month in dates_range]

    series = []
    for skill, skill_data in skills_info.items():
        dates = [datetime.strptime(j["date"], "%x") for j in skill_data["jobs"]]
        series_data = group_by_month_and_get_series(dates, dates_range)
        series.append({"name": skill,
                       "data": series_data})
    return categories, series


def prepare_data_for_skills_histogram(categories, skills_info):
    data = []
    for skill in categories:
        data.append({"name": skill,
                     "y": skills_info[skill]["count"]})
    series = [{"data": data}]
    return series


def filter_by_skills_required(jobs_list, skills):
    result = {}
    for skill in skills:
        result[skill] = {"count": 0, "jobs": []}

    for job in jobs_list:
        full_desc = "{} {}".format(job.title.decode("utf-8").lower(),
                                   job.description.lower())
        for skill in skills:
            if "/" in skill:
                skills_list = skill.split("/")
            else:
                skills_list = [skill, ]

            for skill_name in skills_list:
                skill_re = r'\b{}\b'.format(skill_name)
                if re.search(skill_re, full_desc) is not None:
                    result[skill]["count"] += 1
                    result[skill]["jobs"].append(
                        {"title": job.title.decode("utf-8"),
                         "details_link": job.details_link,
                         "date": job.created.strftime("%x")})
                    break

    return result


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
