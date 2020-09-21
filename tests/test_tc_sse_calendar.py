import datetime

import pandas as pd
import pytz

import pandas_market_calendars as mcal
from pandas_market_calendars.holidays_cn import all_holidays

sse_calendar = mcal.get_calendar('XSHG')


def test_time_zone():
    assert sse_calendar.tz == pytz.timezone('Asia/Shanghai')
    assert sse_calendar.name == 'XSHG'


def test_all_holidays():
    trading_days = sse_calendar.valid_days(pd.Timestamp('2004-01-01'), pd.Timestamp('2020-12-31'))
    for session_label in all_holidays:
        assert session_label not in trading_days


def test_sse_closes_at_lunch():
    sse_schedule = sse_calendar.schedule(
        start_date=datetime.datetime(2015, 1, 14, tzinfo=pytz.timezone('Asia/Shanghai')),
        end_date=datetime.datetime(2015, 1, 16, tzinfo=pytz.timezone('Asia/Shanghai'))
    )

    assert sse_calendar.open_at_time(
        schedule=sse_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 11, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
    )

    assert not sse_calendar.open_at_time(
        schedule=sse_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 12, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
    )
