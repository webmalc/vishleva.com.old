from django import template

register = template.Library()


@register.filter()
def calendar_get_events_by_hour(calendar, hour):
    return calendar.get_events_by_hour(hour)

