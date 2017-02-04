import datetime


def convert_utc_datetime(date):
	return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")