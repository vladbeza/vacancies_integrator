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
    print([i for i in period_range])
    return period_range


def group_by_month_and_get_series(dates_list, period_range):

    dates = pandas.to_datetime(pandas.Series(dates_list))
    dates.index = dates.dt.to_period('m')
    dates = dates.groupby(level=0).size()
    dates = dates.reindex(period_range,
                          fill_value=0)
    return [int(d) for d in dates]


group_by_month_and_get_series(dates_for_test,
                              create_dates_range(
                                datetime(2018, 1, 1),
                                datetime(2020, 1, 1)))
