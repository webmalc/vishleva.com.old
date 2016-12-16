from django.utils import timezone
from django.conf import settings


class Calendar(object):
    """
    Event calendar generator
    """
    def __init__(self, begin=None, end=None):
        self.begin = begin if begin else timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.end = end if end else self.begin + timezone.timedelta(days=settings.EVENTS_CALENDAR_PERIOD)

    def _daterange(self):
        for n in range(int((self.end - self.begin).days)):
            yield self.begin + timezone.timedelta(n)

    def get_days(self):
        """
        Get calendar days
        :return: list of CalendarElements
        :rtype: CalendarElement[]
        """
        result = []
        # TODO: add events;
        for date in self._daterange():
            element = CalendarElement(date=date)
            result.append(element)
        return result


class CalendarElement(object):
    """
    Event calendar element
    """

    def __init__(self, date):
        self.date = date
