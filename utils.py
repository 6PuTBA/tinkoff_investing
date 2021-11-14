from pycbrf.toolbox import ExchangeRates
import datetime

def date_now():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


def get_usd_course():
    return ExchangeRates(date_now())["USD"].value