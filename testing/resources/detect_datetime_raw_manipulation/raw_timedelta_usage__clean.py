import datetime
from datetime import timedelta


def dummy_func(inp):
    print(inp)


def move_time_forward():
    now = datetime.datetime.now()

    # Check commented out lines
    # now += timedelta(days=1)
    # now += datetime.timedelta(weeks=1)
    #
    # now -= timedelta(weeks=1)
    # now -= timedelta(weeks=2)
    #
    # now = now.replace(hour=2)
    # now = now.replace(tzinfo=None)
    # now = now.replace(hour=1, tzinfo=pytz.utc)

    # Test regular usage of timedelta & datetime
    dummy_func(timedelta(days=1))
    dummy_func(datetime.datetime(2018, 10, 11, 2, 3, 4, 450000))

    print(now)
