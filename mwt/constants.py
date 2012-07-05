from datetime import timedelta
from django.conf import settings
import re


DEFAULTS = {
    'mwt': {
        'url': 'http://localhost:8000',
        'name': 'localhost',
        'email_from': 'MWT Server <noreply@localhost>',
        'use_nodejs': False,
    },
    'redis': {
        'connection': {
            'db': 0,
            'host': 'localhost',
            'port': 6379,
            },
        'eager': False,
        'queue_prefix': 'mwt:'
    },
}


RUN_STATUS_PENDING = 'pending'
RUN_STATUS_RUNNING = 'running'
RUN_STATUS_SUCCESS = 'success'
RUN_STATUS_FAIL = 'fail'


REDIS_SETTINGS = getattr(settings, 'REDIS_SETTINGS', DEFAULTS.get('redis'))
MWT_SETTINGS = getattr(settings, 'MWT_SETTINGS', DEFAULTS.get('mwt'))
MWT_SETTINGS['url'] = re.sub(r'\/+$', '', MWT_SETTINGS.get('url', DEFAULTS.get('mwt').get('url')))


RUN_STATES = {
    RUN_STATUS_PENDING: u'Pending',
    RUN_STATUS_RUNNING: u'Running',
    RUN_STATUS_SUCCESS: u'Success',
    RUN_STATUS_FAIL: u'Fail',
}

RUN_STATUS_CHOICES = tuple([(key, value) for key, value in RUN_STATES.iteritems()])


RUN_SCHEDULES = {
    'no': {
        'description': u"Don't repeat",
        'delta': None,
        },
    'minute': {
        'description': u'every minute',
        'delta': timedelta(minutes=1),
        },
    'tenminute': {
        'description': u'every 10 minutes',
        'delta': timedelta(minutes=10),
        },
    'thirtyminute': {
        'description': u'every 30 minutes',
        'delta': timedelta(minutes=30),
        },
    'hour': {
        'description': u'every hour',
        'delta': timedelta(hours=1),
        },
    'sixhour': {
        'description': u'every 6 hours',
        'delta': timedelta(hours=6),
        },
    'twelvehour': {
        'description': u'every 12 hours',
        'delta': timedelta(hours=12),
        },
    'day': {
        'description': u'every day',
        'delta': timedelta(days=1),
        },
    'week': {
        'description': u'every week',
        'delta': timedelta(weeks=1),
        },
    'fourweek': {
        'description': u'every 4 weeks',
        'delta': timedelta(weeks=4),
        },
    }


RUN_REPEAT_CHOICES = tuple([(key, value.get('description')) for key, value in RUN_SCHEDULES.iteritems()])

if MWT_SETTINGS.get('use_nodejs', False):
    settings.INSTALLED_APPS += ('announce', )
    idx = 0
    try:
        idx = settings.MIDDLEWARE_CLASSES.index('django.contrib.sessions.middleware.SessionMiddleware')
    except Exception:
        pass
    c = list(settings.MIDDLEWARE_CLASSES)
    c.insert(idx, 'announce.middleware.AnnounceCookieMiddleware')
    settings.MIDDLEWARE_CLASSES = tuple(c)