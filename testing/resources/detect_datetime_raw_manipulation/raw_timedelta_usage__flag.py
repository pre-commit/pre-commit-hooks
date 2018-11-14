import datetime
from datetime import timedelta

import pytz


def move_time_forward():
    now = datetime.datetime.now()
    timezone = pytz.utc

    # 1
    now = datetime.datetime(now.year, now.month, now.day, hour=8, minute=0, tzinfo=timezone)

    # 2
    now += timedelta(days=1)
    # 3
    now += datetime.timedelta(weeks=1)
    # 4
    now = now + timedelta(seconds=1)

    # 5
    now -= datetime.timedelta(weeks=1)
    # 6
    now -= timedelta(weeks=2)
    # 7
    now = now - timedelta(seconds=1)

    now = now.replace(hour=2)
    # 8
    now = now.replace(tzinfo=None)
    # 9
    now = now.replace(hour=1, tzinfo=pytz.utc)

    # 10
    now = datetime.datetime(2018, 10, 11, 2, 3, 4, 450000, tzinfo=pytz.utc)

    print(now)
