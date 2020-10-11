import pandas as pd

import pandas_market_calendars as mcal

cfe = mcal.get_calendar("XCBF")


def test_2016_holidays():
    # new years: jan 1
    # mlk: jan 18
    # presidents: feb 15
    # good friday: mar 25 (not a holiday because new years is on a friday!)
    # mem day: may 30
    # independence day: july 4
    # labor day: sep 5
    # thanksgiving day: nov 24
    # christmas (observed): dec 26
    # new years (observed): jan 2 2017
    good_dates = cfe.valid_days('2016-01-01', '2016-12-31')
    for day in ["2016-01-01", "2016-01-18", "2016-02-15",
                "2016-05-30", "2016-07-04", "2016-09-05", "2016-11-24",
                "2016-12-26", "2017-01-02"]:
        assert pd.Timestamp(day, tz='UTC') not in good_dates


def test_2016_early_closes():
    # only early close is day after thanksgiving: nov 25
    schedule = cfe.schedule('2016-01-01', '2016-12-31')

    dt = pd.Timestamp("2016-11-25", tz='UTC')
    assert dt in cfe.early_closes(schedule).index

    market_close = schedule.loc[dt].market_close
    market_close = market_close.tz_convert(cfe.tz)
    assert market_close.hour == 12
    assert market_close.minute == 15


def test_open_time_tz():
    assert cfe.open_time.tzinfo == cfe.tz


def test_close_time_tz():
    assert cfe.close_time.tzinfo == cfe.tz
