from django.db import models
from .abstract import Plugin, PluginOption


class TaskPlugin(Plugin):
    pass


class NotificationPlugin(Plugin):
    pass


class TaskPluginOption(PluginOption):
    plugin = models.ForeignKey(TaskPlugin, related_name='+')


class NotificationPluginOption(PluginOption):
    plugin = models.ForeignKey(NotificationPlugin, related_name='+')
