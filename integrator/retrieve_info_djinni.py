# coding=utf-8
import re

import requests
from bs4 import BeautifulSoup

from config import location_translations
from integrator.models import Job, City, db, Language
from integrator.utils import add_languages_used

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}
base_url = "https://djinni.co"
jobs_url = base_url + "/jobs/"
qa_automation = jobs_url + "?primary_keyword=QA+Automation"
session = requests.Session()
session.headers = headers


def get_new_jobs_djinni():

    #get vacancies list

    print("Get jobs titles and links")
    home_html = session.get(qa_automation)
    if home_html.ok:
        job_links = _get_links_from_page(home_html.content)
        next_page = 2

        while True:
            link = qa_automation + "&page={}".format(next_page)
            print("Get Djinni page {}".format(next_page))
            response = session.get(link)
            if response.ok:
                new_jobs = _get_links_from_page(response.content)
                print("new jobs {}".format(new_jobs))
                if not new_jobs:
                    break
                job_links.update(new_jobs)
                next_page += 1
            else:
                break

        print("Djinni links gathered")
    else:
        raise Exception("Couldn't get links from Djinni")


    #get all data from details link

    jobs_count = 0
    print("Gathered jobs - {}".format(len(job_links)))
    for link, title in job_links.items():

        djinni_id = re.search(jobs_url + "(.+)[/]", link).group(1)
        job_request = Job.query.filter_by(djinni_id=djinni_id).first()

        if not job_request:

            content = session.get(link)
            if content.ok:
                html = BeautifulSoup(content.content)
                details = html.find("div", {"class": "list-jobs__details"}).text
                cities = []
                for city, variants in location_translations.items():
                    for v in variants:
                        if v in details.lower():
                            cities.append(city)
                            break

                description = html.find_all(
                    "div", {"class": "profile-page-section"})[1].text.strip()

                try:
                    company = html.find_all(
                        "div", {"class": "profile-page-section"})[2].find(
                        "a").get("href")
                except Exception:
                    company = ""

                job = Job(title=title,
                          djinni_id=djinni_id,
                          description=description,
                          company=company,
                          details_link=link,
                          is_automation=True)

                if not cities:
                    another = City.query.filter_by(name="Другой").first()
                    job.cities.append(another)

                for city in cities:
                    if city in ("Удаленно", "Remote", "Віддалена робота"):
                            job.remote = True
                            continue
                    c = City.query.filter_by(name=city).one_or_none()
                    if c:
                        job.cities.append(c)

                langs = Language.query.all()
                add_languages_used(langs, job)

                print("Add to db djinni {}".format(djinni_id))
                db.session.add(job)
                db.session.commit()
                jobs_count += 1

    djinni_vacancies = Job.query.filter(Job.djinni_id != None,
                                         Job.active == True).all()
    for job in djinni_vacancies:
        if job.details_link not in job_links.keys():
            print("Deactivate vacancy '{}'".format(job.title))
            job.active = False
            db.session.add(job)
            db.session.commit()
    print("finish gathering from djinni. Added: {}".format(jobs_count))


def _get_links_from_page(page_content):
    result = {}
    jobs_list = BeautifulSoup(page_content).find_all(
        "div", {"class": "list-jobs__title"})

    on_page = 0
    for job_title in jobs_list:
        on_page += 1
        profile = job_title.find("a", {"class": "profile"})
        result[base_url + profile.get("href")] = profile.text
    print("on page - {}".format(on_page))
    return result
