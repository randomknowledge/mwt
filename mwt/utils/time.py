from django.conf import settings
import pytz

def get_tz(tzstring=None):
    if not tzstring:
        tzstring = getattr(settings, 'TIME_ZONE', 'UTC')
    return pytz.timezone(tzstring)
