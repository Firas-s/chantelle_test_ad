from datetime import datetime, timezone
import pytz
import time

def get_ingestion():
    now = datetime.now(pytz.timezone('UTC'))
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_timestamp(stamp):
    if stamp is None:
        return None
    now = datetime.fromtimestamp(stamp, pytz.timezone('UTC'))
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_now(delta):
    ts = time.time()
    return round(ts)-delta*60

def get_date(date):
    return round(datetime.strptime(date, '%Y-%m-%d').timestamp())