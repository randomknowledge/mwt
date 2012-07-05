from django.db import models
from django.db.models.query_utils import Q
from . import constants
from .utils.time import get_tznow


class RunScheduleManager(models.Manager):
    def pending(self):
        qset = self.get_query_set().filter(paused=False)
        query = Q()
        for repeat, data in constants.RUN_SCHEDULES.iteritems():
            subquery = Q(repeat=repeat)

            if repeat == 'no':
                subquery = subquery & Q(last_run=None) & Q(first_run_at__lte=get_tznow())
            else:
                subquery = subquery & Q(first_run_at__lte=get_tznow())\
                            & (
                                Q(last_run=None)
                                |
                                Q(last_run__lt=get_tznow('UTC') - constants.RUN_SCHEDULES.get(repeat).get('delta'))
                            )

            query = query | subquery
        return qset.filter(query)


class BelongstoManager(models.Manager):
    def for_user(self, user):
        return self.get_query_set().filter(Q(users__id=user.pk) | Q(groups__users__id=user.pk))


class TestrunManager(models.Manager):
    def for_user(self, user):
        return self.get_query_set().filter(Q(schedule__test__website__users__id=user.pk) | Q(schedule__test__website__groups__users__id=user.pk))
