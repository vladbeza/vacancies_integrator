import re

import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"}
base_url = "https://djinni.co/jobs/"
qa_automation = base_url + "?primary_keyword=QA+Automation"
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
                job_links.update(_get_links_from_page(response.content))
                next_page += 1
            else:
                break

        print("Djinni links gathered")
    else:
        raise Exception("Couldn't get links from Djinni")


    #get all data from details link

    for title, link in job_links:
        # job = Job(title=vacancy_info["title"],
        #           dou_id=vacancy_id,
        #           description=vacancy_info["description"],
        #           company=vacancy_info["company_href"],
        #           details_link=vacancy_info["details_href"],
        #           salary=vacancy_info.get("salary", None))

        djinni_id = re.search(base_url + "(.+)[\\\]", link).group(1)

        content = session.get(link)
        if content.ok:
            html = BeautifulSoup(content.content)
            details = html.find("div", {"class": "list-jobs__details"}).text





def _get_links_from_page(page_content):
    result = {}
    html = BeautifulSoup(page_content).find_all(
        "div", {"class": "list-jobs__title"}).find(
        "a", {"class": "profile"})
    for profile in html:
        result[profile.text.encode("utf-8")] = profile.get("href")
    return result
