import time
from datetime import datetime


def string_to_timestamp(date, pattern="%d-%m-%Y"):
    return time.mktime(datetime.strptime(date, pattern).timetuple())


def string_to_datetime(date, pattern="%d-%m-%Y"):
    return datetime.strptime(date, pattern)
