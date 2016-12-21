from django.utils import timezone
from django.conf import settings
from events.models import Event
import arrow


def _get_date_events(begin, end, events):
    return [e for e in events if begin <= e.begin <= end or begin < e.end <= end or (e.begin <= begin and e.end >= end)]


class Calendar(object):
    """
    Event calendar generator
    """
    def __init__(self, begin=None, end=None):
        self.begin = begin if begin else arrow.now().floor('day').to('UTC').datetime
        self.end = end if end else self.begin + timezone.timedelta(days=settings.EVENTS_CALENDAR_PERIOD)
        self.events = Event.objects.get_by_dates(begin=self.begin, end=self.end)

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
        for date in self._daterange():
            end = arrow.get(date).replace(hours=+24).datetime
            element = CalendarDay(date=date, events=_get_date_events(date, end, self.events))
            result.append(element)
        return result


class CalendarDay(object):
    """
    Event calendar element
    """

    def __init__(self, date, events=[]):
        self.date = date
        self.events = events
        self.hours = []
        for h in range(0, 24):
            hour = arrow.get(self.date).replace(hours=+h).datetime
            begin = arrow.get(hour).floor('hour').datetime
            end = arrow.get(hour).ceil('hour').datetime
            self.hours.append(CalendarHour(hour, events=_get_date_events(begin, end, self.events)))

    def get_events_by_hour(self, hour):
        for h in self.hours:
            if h.date.strftime('%H') == hour.strftime('%H'):
                return h.events
        return []


class CalendarHour(object):
    """
    Event calendar element
    """
    def __init__(self, date, events=[]):
        self.date = date
        self.events = events
