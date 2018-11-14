import datetime
from datetime import timedelta

import pytz


def move_time_forward():
    now = datetime.datetime.now()

    now += timedelta(days=1)  # safe_dt_op
    now += datetime.timedelta(weeks=1)  # safe_dt_op

    now -= timedelta(weeks=1)  # safe_dt_op
    now -= timedelta(weeks=2)  # safe_dt_op

    now = now.replace(hour=2)
    now = now.replace(tzinfo=None)  # safe_dt_op
    now = now.replace(hour=1, tzinfo=pytz.utc)  # safe_dt_op

    print(now)
