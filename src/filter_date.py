from dateutil import parser

from datetime import datetime, timedelta, timezone


class FilterDate:
    @staticmethod
    def get_date(date):
        return parser.parse(date)

    @staticmethod
    def unix_time(date, filter_count):
        post_time = datetime.utcfromtimestamp(int(date) / 1000)

        target_time = datetime.now() - post_time

        if target_time > timedelta(filter_count):
            return False

        return post_time

    @staticmethod
    def check_data(date, filter_count):
        post_time = parser.parse(date)

        target_time = datetime.now(timezone.utc) - post_time

        if target_time > timedelta(filter_count):
            return False

        return post_time

    @staticmethod
    def get_format(date: str):

        try:
            date = parser.parse(date)
        except:
            return datetime.now().strftime('%d.%m.%Y')

        try:
            date = date.strftime('%d.%m.%Y')
        except:
            return ''

        return date
