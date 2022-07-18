from datetime import datetime, timedelta
import pytz


def int_round(num):
    num = float(num)
    num = int(num + (0.5 if num > 0 else -0.5))
    return num


def get_time_zones():
    utc_offset = timedelta(hours=5)
    print({tz.zone for tz in map(pytz.timezone, pytz.all_timezones_set)
           if datetime.now(pytz.utc).astimezone(tz).utcoffset() == utc_offset})
