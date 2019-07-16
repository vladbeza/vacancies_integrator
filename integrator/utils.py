import re

import pandas
from datetime import datetime


dates_for_test = [datetime(2019, 4, 12), datetime(2019, 5, 6),
                  datetime(2019, 4, 14), datetime(2019, 12, 12)]


def create_dates_range(min_date, max_date):
    ranges_dates = pandas.to_datetime(pandas.Series([min_date, max_date]))
    ranges_dates.index = ranges_dates.dt.to_period('m')
    period_range = pandas.period_range(ranges_dates.index.min(),
                                       ranges_dates.index.max(),
                                       freq='m')
    return period_range


def group_by_month_and_get_series(dates_list, period_range):

    dates = pandas.to_datetime(pandas.Series(dates_list))
    dates.index = dates.dt.to_period('m')
    dates = dates.groupby(level=0).size()
    dates = dates.reindex(period_range,
                          fill_value=0)
    return [int(d) for d in dates]


def add_automation(job_instance):
    key_words = [r"\bautomation\b",
                 r"\bin test\b",
                 r"\bавтоматизация\b",
                 r"\bавтоматизиронный\b"]
    if any(re.search(word, job_instance.title.decode("utf-8").lower())
                    is not None for word in key_words):
        job_instance.is_automation = True


def add_languages_used(languages, job_instance):
    full_desc = "{} {}".format(
        job_instance.title.lower(),
        job_instance.description.lower())

    for lang in languages:
        if lang.name == "JavaScript":
            langs = [r"\bjavascript\b", r"\bjs\b"]
        elif lang.name == "C#":
            langs = [r"\bc#\b", r"\b[.]net\b"]
        else:
            langs = [r"\b{}\b".format(lang.name.lower())]

        if any(re.search(l, full_desc) for l in langs):
            job_instance.languages.append(lang)
