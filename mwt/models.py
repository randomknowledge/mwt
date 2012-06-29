import re
import datetime
from django.db import models
from django.conf import settings
from . import helper, constants
from .utils.time import get_tz


class Client(models.Model):
    name = models.CharField(max_length=96, null=False, blank=False, unique=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Website(models.Model):
    name = models.CharField(max_length=96, null=False, blank=False)
    url = models.URLField(unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    client = models.ForeignKey(Client)

    def __unicode__(self):
        return "%s on %s" % (self.name, self.url)


class Test(models.Model):
    website = models.ForeignKey(Website)
    description = models.CharField(max_length=255, null=False, blank=False)
    plugins = models.ManyToManyField('Plugin')

    def get_options_for_plugin(self, plugin):
        return self._plugin_opts_to_dict(
                PluginOption.objects.filter(test=self, plugin=plugin)
        )

    def get_options_for_plugin_dsn(self, plugin_dsn):
        return self._plugin_opts_to_dict(
                PluginOption.objects.filter(test=self, plugin__dsn=plugin_dsn)
        )

    def _plugin_opts_to_dict(self, opts):
        d = {}
        for opt in opts:
            d[str(opt.key)] = str(opt.value)
        return d

    def plugin_list(self):
        return [str(p.name) for p in Plugin.objects.filter(test=self)]

    def __unicode__(self):
        return self.description


class Testrun(models.Model):
    date_created = models.DateTimeField(auto_created=True, auto_now_add=True, editable=True)
    date_started = models.DateTimeField(blank=True, null=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    state = models.CharField(
            max_length=32, choices=constants.RUN_STATUS_CHOICES, default=constants.RUN_STATUS_PENDING)
    message = models.TextField(null=True, blank=True)
    plugin = models.ForeignKey('Plugin', related_name='+')
    schedule = models.ForeignKey('RunSchedule', related_name='+')

    def start(self):
        self.date_started = datetime.datetime.now(tz=get_tz())
        self.state = constants.RUN_STATUS_RUNNING
        self.save()

    def end(self, success, message):
        self.date_finished = datetime.datetime.now(tz=get_tz())
        self.message = message
        if success:
            self.state = constants.RUN_STATUS_SUCCESS
        else:
            self.state = constants.RUN_STATUS_FAIL
        self.save()

    def success(self, message=''):
        self.end(True, message)

    def fail(self, message=''):
        self.end(False, message)

    def duration(self):
        if self.date_started is None:
            return datetime.timedelta(seconds=0)
        if self.state == constants.RUN_STATUS_PENDING or self.state == constants.RUN_STATUS_RUNNING:
            return datetime.datetime.now(tz=get_tz()) - self.date_started
        return self.date_finished - self.date_started

    def admin_state(self):
        return '<img src="%smwt/admin/img/icon-%s.png" alt="%s" title="%s" style="margin-left: 10px" />'\
            % (
                getattr(settings, 'STATIC_URL', '/static/'),
                self.state,
                constants.RUN_STATES.get(self.state),
                constants.RUN_STATES.get(self.state)
        )
    admin_state.allow_tags = True
    admin_state.short_description = 'State'

    def __unicode__(self):
        return "%s: %s" % (str(self.schedule), str(self.plugin))


class Plugin(models.Model):
    dsn = models.CharField(max_length=255, null=False, blank=False, unique=True)
    name = models.CharField(max_length=120, blank=True, default='')
    author = models.CharField(max_length=120, blank=True, default='')
    description = models.TextField(blank=True)
    versionfield = models.CharField(max_length=12, null=True, default=None)
    params = models.TextField(null=True, blank=True, editable=False)

    def __unicode__(self):
        return "%s (%s) Version %s" % (
                getattr(self, 'name', self.dsn),
                getattr(self, 'name', self.dsn),
                self.versionstring
        )

    def save(self, *args, **kwargs):
        self.versionfield = re.sub(r'[^\d,]', '', str(self.versionfield))
        super(Plugin, self).save(*args, **kwargs)

    @property
    def version(self):
        return helper.version(str(self.versionfield))

    @property
    def versionstring(self):
        return helper.versionstring(str(self.versionfield))

    @property
    def versionnumber(self):
        return helper.versionnumber(str(self.versionfield))


class PluginOption(models.Model):
    plugin = models.ForeignKey(Plugin, related_name='plugin')
    test = models.ForeignKey(Test, related_name='test')
    key = models.CharField(max_length=64, null=False, blank=False)
    value = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return "%s => %s" % (self.key, self.value)

    def as_dict(self):
        d = {}
        d[str(self.key)] = str(self.value)
        return d


class RunSchedule(models.Model):
    datetime = models.DateTimeField()
    repeat = models.CharField(max_length=32, choices=constants.RUN_REPEAT_CHOICES, default='no')
    test = models.ForeignKey(Test)
    paused = models.BooleanField(default=False)

    def __unicode__(self):
        if self.repeat == 'no':
            add = "Run once on %s" % self.datetime
        else:
            add = "Run every %s" % constants.RUN_SCHEDULES.get(self.repeat).get('description', self.repeat)

        return "%s: %s" % (self.test, add)