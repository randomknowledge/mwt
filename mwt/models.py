import datetime
from django.db import models
from mwt.utils import get_tz


RUN_STATUS_CHOICES = (
    ('pending', u'Pending'),
    ('running', u'Running'),
    ('success', u'Success'),
    ('fail', u'Fail'),
)

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
    url = models.URLField(null=False, blank=False)
    plugins = models.ManyToManyField('Plugin')

    def __unicode__(self):
        return self.description


class Testrun(models.Model):
    date_created = models.DateTimeField(auto_created=True, auto_now_add=True)
    date_started = models.DateTimeField(blank=True, null=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=32, choices=RUN_STATUS_CHOICES, default='pending')
    message = models.TextField(null=True, blank=True)
    test = models.ForeignKey(Test)

    def start(self):
        self.date_started = datetime.datetime.now(tz=get_tz())
        self.state = 'running'
        self.save()

    def end(self, success, message):
        self.date_finished = datetime.datetime.now(tz=get_tz())
        self.message = message
        if success:
            self.state = 'success'
        else:
            self.state = 'fail'
        self.save()

    def success(self, message=''):
        self.end(True, message)

    def fail(self, message=''):
        self.end(False, message)

    def duration(self):
        if self.state == 'pending' or self.state == 'running':
            return datetime.timedelta()
        return self.date_finished - self.date_started

    def __unicode__(self):
        return str(self.test)


class Plugin(models.Model):
    dsn = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __unicode__(self):
        return self.dsn