from django.db import models
import re
from .. import helper


class Plugin(models.Model):
    dsn = models.CharField(max_length=255, null=False, blank=False, unique=True)
    name = models.CharField(max_length=120, blank=True, default='')
    author = models.CharField(max_length=120, blank=True, default='')
    description = models.TextField(blank=True)
    versionfield = models.CharField(max_length=12, null=True, default=None)
    params = models.TextField(null=True, blank=True, editable=False)

    class Meta:
        abstract = True
        app_label = 'mwt'

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
    test = models.ForeignKey('Test', related_name='+')
    key = models.CharField(max_length=64, null=False, blank=False)
    value = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        abstract = True
        app_label = 'mwt'

    def __unicode__(self):
        return "%s => %s" % (self.key, self.value)

    def as_dict(self):
        d = {}
        d[str(self.key)] = str(self.value)
        return d