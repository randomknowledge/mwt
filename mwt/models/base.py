import cgi
import datetime
from django.conf import settings
from django.db import models
from .. import constants
from django.utils import simplejson
from django.utils.safestring import mark_safe
from .plugins import TaskPluginOption, NotificationPluginOption
from ..utils.time import get_tz
from ..managers import RunScheduleManager


class Client(models.Model):
    name = models.CharField(max_length=96, null=False, blank=False, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        app_label = 'mwt'

    def __unicode__(self):
        return self.name


class Website(models.Model):
    name = models.CharField(max_length=96, null=False, blank=False)
    url = models.URLField(unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    client = models.ForeignKey(Client)

    class Meta:
        app_label = 'mwt'

    def __unicode__(self):
        return "%s on %s" % (self.name, self.url)


class Test(models.Model):
    website = models.ForeignKey(Website)
    description = models.CharField(max_length=255, null=False, blank=False)
    tasks = models.ManyToManyField('TaskPlugin', related_name='+')
    notifications = models.ManyToManyField('NotificationPlugin', related_name='+', null=True, blank=True)

    class Meta:
        app_label = 'mwt'

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
    task = models.ForeignKey('TaskPlugin', related_name='+')
    schedule = models.ForeignKey('RunSchedule', related_name='+')

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
        success = False
        try:
            result = simplejson.loads(self.result)
            success = result.get('success', False)
        except Exception:
            pass

        if success:
            return self.stage_image(constants.RUN_STATUS_SUCCESS)
        else:
            return self.stage_image(constants.RUN_STATUS_FAIL)
    admin_result.allow_tags = True
    admin_result.short_description = 'Result'

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
