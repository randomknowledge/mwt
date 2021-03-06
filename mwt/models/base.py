import cgi
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.db import models
from .. import constants
from django.db.models.signals import post_save
from django.utils import simplejson
from django.utils.safestring import mark_safe
from .plugins import TaskPluginOption, NotificationPluginOption
from ..utils.time import get_tz
from ..managers import RunScheduleManager, BelongstoManager, TestrunManager, TestManager


class MWTGroup(models.Model):
    name = models.CharField(max_length=96, null=False, blank=False, unique=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, null=True, blank=True)

    class Meta:
        app_label = 'mwt'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __unicode__(self):
        return unicode(self.name)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')

    class Meta:
        app_label = 'mwt'

    def __unicode__(self):
        return unicode(self.user)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Client(models.Model):
    name = models.CharField(max_length=96, null=False, blank=False, unique=True)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, null=True, blank=True)
    groups = models.ManyToManyField(MWTGroup, null=True, blank=True)

    objects = BelongstoManager()

    class Meta:
        app_label = 'mwt'

    def __unicode__(self):
        return self.name


class Website(models.Model):
    name = models.CharField(max_length=96, null=False, blank=False)
    url = models.URLField(unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    client = models.ForeignKey(Client)
    users = models.ManyToManyField(User, null=True, blank=True)
    groups = models.ManyToManyField(MWTGroup, null=True, blank=True)

    objects = BelongstoManager()

    def belongs_to(self, user):
        return self.users.filter(pk=user.pk) or self.groups.filter(users__id=user.pk)

    class Meta:
        app_label = 'mwt'

    def __unicode__(self):
        return "%s on %s" % (self.name, self.url)


class Test(models.Model):
    website = models.ForeignKey(Website)
    description = models.CharField(max_length=255, null=False, blank=False)
    tasks = models.ManyToManyField('TaskPlugin', related_name='+')
    notifications = models.ManyToManyField('NotificationPlugin', related_name='+', null=True, blank=True)

    objects = TestManager()

    class Meta:
        app_label = 'mwt'

    def to_simple_object(self):
        me = simplejson.loads(serializers.serialize("json", Test.objects.select_related(depth=99).filter(pk=self.pk)))[0]

        fields = me.get('fields')

        def get_plugin_options(tasks, task_id):
            for t in tasks:
                if t.get('id') == task_id:
                    return t
            return None

        tasks = []
        for plugin in TaskPluginOption.objects.filter(test=self, plugin__pk__in=fields.get('tasks')).values('plugin', 'pk', 'key', 'value'):
            pid = plugin.get('plugin')
            if not pid in [t.get('id') for t in tasks]:
                tasks.append({'id': pid, 'options': []})
            get_plugin_options(tasks, pid).get('options').append({'id': plugin.get('pk'), 'key': plugin.get('key'), 'value': plugin.get('value')})


        notifications = []
        for plugin in NotificationPluginOption.objects.filter(test=self, plugin__pk__in=fields.get('notifications')).values('plugin', 'pk', 'key', 'value'):
            pid = plugin.get('plugin')
            if not pid in [t.get('id') for t in notifications]:
                notifications.append({'id': pid, 'options': []})
            get_plugin_options(notifications, pid).get('options').append({'id': plugin.get('pk'), 'key': plugin.get('key'), 'value': plugin.get('value')})

        return {
            'id': me.get('pk'),
            'description': me.get('description'),
            'website': fields.get('website'),
            'notifications': notifications,
            'schedules': [{'id': s.pk, 'repeat': s.repeat, 'paused': s.paused} for s in RunSchedule.objects.filter(test=self)],
            'tasks': tasks,
        }

    def to_json(self):
        return simplejson.dumps(self.to_simple_object(), ensure_ascii=False)

    def get_options_for_task_dsn(self, task_dsn):
        return self._plugin_opts_to_dict(
            TaskPluginOption.objects.filter(plugin=self.tasks.get(dsn=task_dsn))
        )

    def get_options_for_notification_dsn(self, notification_dsn):
        return self._plugin_opts_to_dict(
            NotificationPluginOption.objects.filter(plugin=self.notifications.get(dsn=notification_dsn))
        )

    def _plugin_opts_to_dict(self, opts):
        d = {}
        for opt in opts:
            d[str(opt.key)] = str(opt.value)
        return d

    def task_list(self):
        return [str(p.name) for p in self.tasks.all()]

    def notification_list(self):
        return [str(p.name) for p in self.notifications.all()]

    def __unicode__(self):
        return self.description


class Testrun(models.Model):
    date_created = models.DateTimeField(auto_created=True, auto_now_add=True, editable=True)
    date_started = models.DateTimeField(blank=True, null=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    state = models.CharField(
        max_length=32, choices=constants.RUN_STATUS_CHOICES, default=constants.RUN_STATUS_PENDING)
    result = models.TextField(null=True, blank=True, editable=False)
    result_successful = models.BooleanField(default=False)
    task = models.ForeignKey('TaskPlugin', related_name='+')
    schedule = models.ForeignKey('RunSchedule', related_name='+')

    objects = TestrunManager()

    class Meta:
        app_label = 'mwt'

    def start(self):
        self.date_started = datetime.datetime.now(tz=get_tz())
        self.state = constants.RUN_STATUS_RUNNING
        self.save()

    def end(self, success, result):
        self.date_finished = datetime.datetime.now(tz=get_tz())
        self.result = result
        if success:
            self.state = constants.RUN_STATUS_SUCCESS
        else:
            self.state = constants.RUN_STATUS_FAIL
        self.save()

    def success(self, result="{'success': true}"):
        self.end(True, result)

    def fail(self, result="{'success': false}"):
        self.end(False, result)

    def duration(self):
        if self.date_started is None:
            return datetime.timedelta(seconds=0)
        if self.state == constants.RUN_STATUS_PENDING or self.state == constants.RUN_STATUS_RUNNING:
            return datetime.datetime.now(tz=get_tz()) - self.date_started
        return self.date_finished - self.date_started

    def result_object(self):
        return simplejson.loads(self.result)

    def run_success(self):
        return self.result_object().get('success', False)

    def _run_other_results(self):
        r = ''
        for key, value in self.result_object().iteritems():
            if key != 'success' and key != 'message':
                r += "%s: %s\n" % (key, value)
        return r

    def other_run_results(self):
        return mark_safe("<pre>%s</pre>" % cgi.escape(self._run_other_results().decode('string_escape')))

    def run_message(self):
        return mark_safe("<pre>%s</pre>" % cgi.escape(self.result_object().get('message', '')))

    def stage_image(self, state):
        return '<img src="%smwt/admin/img/icon-%s.png" alt="%s" title="%s" style="margin-left: 10px" />'\
            % (
                getattr(settings, 'STATIC_URL', '/static/'),
                state,
                constants.RUN_STATES.get(state),
                constants.RUN_STATES.get(state)
                )

    def admin_state(self):
        return self.stage_image(self.state)
    admin_state.allow_tags = True
    admin_state.short_description = 'State'

    def admin_result(self):
        if self.result_successful:
            return self.stage_image(constants.RUN_STATUS_SUCCESS)
        else:
            return self.stage_image(constants.RUN_STATUS_FAIL)
    admin_result.allow_tags = True
    admin_result.short_description = 'Result'

    @property
    def users(self):
        u = []
        for group in self.schedule.test.website.groups.all():
            for user in group.users.all():
                if not user in u:
                    u.append(user)
        for user in self.schedule.test.website.users.all():
            if not user in u:
                u.append(user)
        return u

    def save(self, *args, **kwargs):
        success = False
        try:
            result = simplejson.loads(self.result)
            success = result.get('success', False)
        except Exception:
            pass
        self.result_successful = success
        super(Testrun, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s: %s" % (str(self.schedule), str(self.task))


class RunSchedule(models.Model):
    first_run_at = models.DateTimeField()
    repeat = models.CharField(max_length=32, choices=constants.RUN_REPEAT_CHOICES, default='no')
    test = models.ForeignKey(Test)
    paused = models.BooleanField(default=False)
    run_id = models.IntegerField(default=0, verbose_name=u'Run Counter')
    last_run = models.DateTimeField(editable=False, null=True, blank=True)

    objects = RunScheduleManager()

    class Meta:
        app_label = 'mwt'

    @property
    def description(self):
        if self.repeat == 'no':
            return "Run once on %s" % self.first_run_at
        else:
            return "Run every %s" % constants.RUN_SCHEDULES.get(self.repeat).get('description', self.repeat)

    def __unicode__(self):
        return "%s: %s" % (self.test, self.description)
