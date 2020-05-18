# -*- coding:utf-8 -*-
import re
import json

from datetime import datetime
from flask import render_template, Blueprint, current_app, request, abort, jsonify
from flask_sqlalchemy import get_debug_queries

from integrator.forms import FilterJobsForm, SkillsForm
from integrator.models import Job, Language, db, City
from integrator.utils import create_dates_range, group_by_month_and_get_series
from config import CITIES, languages

jobs = Blueprint('jobs', __name__)


@jobs.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


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

        active_vacancies_query = active_vacancies_query.filter_by(
            is_automation=is_automation)
        
        if is_remote:
            active_vacancies_query = active_vacancies_query.filter_by(
                remote=is_remote)

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
            active_vacancies_query = active_vacancies_query.join(
                Job.cities).filter_by(id=int(city))

        if language != "Any":
            active_vacancies_query = active_vacancies_query.join(
                Job.languages).filter_by(id=int(language))

        active_vacancies = active_vacancies_query.all()

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

@jobs.route("/api/v1.0/create", methods=['POST'])
def api_create_job():
    if not request.json:
        response = jsonify({'error': 'bad request. No data provided. Request {}'.format(request)})
        response.status_code = 400
        print("API response is {}".format(response))
        return response

    print("Creating job with data {}".format(request.json))

    job = Job(title=request.json["title"],
              djinni_id=request.json.get("djinni_id", None),
              description=request.json["description"],
              company=request.json["company"],
              details_link=request.json["details_link"],
              is_automation=request.json["is_automation"],
              dou_id=request.json.get("dou_id", None),
              salary=request.json["salary"],
              active=request.json["active"],
              remote=request.json["remote"]
              )

    if request.json.get("cities") is not None:
        for city_name in request.json.get("cities"):
            city = City.query.filter_by(name=city_name).first()
            job.cities.append(city)
    
    if request.json.get("languages") is not None:
        for lang_name in request.json.get("languages"):
            lang = Language.query.filter_by(name=lang_name).first()
            job.languages.append(lang)

    db.session.add(job)
    db.session.commit()

    response = jsonify({'message': 'succeed'})
    response.status_code = 201
    print("API response is {}".format(response))
    return response


@jobs.route("/history/graphics", methods=['GET'])
def more_graphics():
    city = request.args.get('city')
    if city is not None:
        all_jobs = Job.query.join(Job.cities).filter_by(name=city).all()
    else:
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
    # languages = Language.query.all()
    for l in languages:
        jobs_query = Job.query.join(Job.languages).filter_by(name=l)
        if city is not None:
            jobs_query = jobs_query.join(Job.cities).filter_by(name=city)
        jobs = jobs_query.all()
        series_for_lang = group_by_month_and_get_series(
                [j.created for j in jobs], dates_range)
        language_series.append({"name": l, "data": series_for_lang})

    return render_template("graphics.html",
                           cities=CITIES,
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
        full_desc = "{} {}".format(job.title.lower(),
                                   job.description.lower())
        for skill in skills:
            if "/" in skill:
                skills_list = skill.split("/")
            else:
                skills_list = [skill, ]

            for skill_name in skills_list:
                if skill_name.isalpha():
                    skill_re = r'\b{}\b'.format(skill_name)
                else:
                    skill_re = r' {}'.format(skill_name)
                if re.search(skill_re, full_desc) is not None:
                    result[skill]["count"] += 1
                    result[skill]["jobs"].append(
                        {"title": job.title,
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

