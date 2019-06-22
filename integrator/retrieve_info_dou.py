# -*- coding:utf-8 -*-

import re

from integrator.models import db, Job, City
import requests
from bs4 import BeautifulSoup

all_jobs_list = "https://jobs.dou.ua/vacancies/?category={category}"
all_jobs_city = "https://jobs.dou.ua/vacancies/?city={city}&category={category}"

xhr_jobs_list = "https://jobs.dou.ua/vacancies/xhr-load/?category={category}"
xhr_jobs_city = "https://jobs.dou.ua/vacancies/xhr-load/?city={city}&category={category}"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}
session = requests.Session()
session.headers = headers


def gather_new_jobs_dou():
    print("gather_new_jobs")
    all_vacancies_on_dou = get_vacancies()
    print("all_vacancies_on_dou got")
    for vacancy_id, vacancy_info in all_vacancies_on_dou.items():
        job_request = Job.query.filter_by(dou_id=vacancy_id).first()
        if not job_request:
            get_descriptions(vacancy_info)
            job = Job(title=vacancy_info["title"],
                      dou_id=vacancy_id,
                      description=vacancy_info["description"],
                      company=vacancy_info["company_href"],
                      details_link=vacancy_info["details_href"],
                      salary=vacancy_info.get("salary", None))

            cities = vacancy_info.get("cities", None)
            another = City.query.filter_by(name="Другой").first()
            if cities is not None:
                for city in cities:
                    if city in ("Удаленно", "Remote"):
                        job.remote = True
                        continue
                    c = City.query.filter_by(name=city).one_or_none()
                    if c:
                        job.cities.append(c)
                    else:
                        job.cities.append(another)
            else:
                job.cities.append(another)

            db.session.add(job)
            db.session.commit()

    dou_vacancies = Job.query.filter(Job.dou_id is not None, Job.active is True).all()
    for dou_job in dou_vacancies:
        if dou_job.dou_id not in all_vacancies_on_dou.keys():
            dou_job.active = False
            db.session.add(dou_job)

    db.session.commit()
    print("finish gathering from dou")


def get_vacancies(for_city=None, category="QA"):
    print("get vacancies")

    vacancies = {}

    if for_city is not None:
        referer_url = all_jobs_city.format(category=category, city=for_city)
        xhr_url = xhr_jobs_city.format(category=category, city=for_city)
    else:
        referer_url = all_jobs_list.format(category=category)
        xhr_url = xhr_jobs_list.format(category=category)

    home_html = session.get(referer_url)
    if 'csrftoken' in session.cookies:
        csrftoken = session.cookies['csrftoken']
    else:
        csrftoken = session.cookies['csrf']

    try:
        vacancies_header_text = BeautifulSoup(home_html.content).find(
            "div", {"class": "b-vacancies-head"}).find("h1").text
        vacancies_count = int(re.match("[0-9]+", vacancies_header_text).group())
    except:
        vacancies_count = 40

    current_vacancies_counter = 0

    while current_vacancies_counter <= vacancies_count:

        data = session.post(xhr_url,
                            data={"csrfmiddlewaretoken": csrftoken, "count": current_vacancies_counter},
                            headers=headers.update({"Referer": referer_url}))

        json_data = data.json()

        html_data = json_data["html"]

        structured_data = BeautifulSoup(html_data)

        vacancies_list = structured_data.find_all("div", {"class": "vacancy"})

        for vacancy in vacancies_list:
            identifier = vacancy.get("_id")
            if identifier not in vacancies.keys():
                vacancy_data = {}
                data = vacancy.find("a", {"class": "vt"})

                vacancy_data["title"] = data.text.replace("\xa0", " ").encode("utf-8")
                vacancy_data["details_href"] = data.get("href")
                try:
                    vacancy_data["cities"] = [city.strip().capitalize() for city in
                                          vacancy.find("span", {"class": "cities"}).text.split(",")]
                except AttributeError:
                    pass
                vacancy_data["company_href"] = vacancy.find("a", {"class": "company"}).get("href")
                vacancies[identifier] = vacancy_data

        current_vacancies_counter += 40

    return vacancies


def get_descriptions(vacancy):
    print("get description for {}".format(vacancy))
    details_page = session.get(vacancy["details_href"]).content
    details_html = BeautifulSoup(details_page)
    descriptions = details_html.find_all("div", {"class": "text b-typo vacancy-section"})
    # vacancy["description"] = "\n".join([desc.text.replace("\xa0", " ") for desc in descriptions])
    vacancy["description"] = descriptions[0].text.replace("\xa0", " ")
    salary = details_html.find("span", {"class": "salary"})
    if salary is not None:
        vacancy["salary"] = salary.text.replace("\xa0", " ")
