import mwt
from mwt.models import Plugin
import os
import re
from celery.registry import tasks

def import_plugins():
    plugins = 'plugins'
    tasks = 'tasks'
    imported = []
    parentmodule = "mwt.%s.%s" % (plugins, tasks)
    basedir = os.path.dirname(__file__)
    plugindir = os.path.join(basedir, plugins, tasks)

    if os.path.isdir(plugindir):
        for file in os.listdir(plugindir):
            m = re.match(r'^(?P<module>[a-z0-9][a-z0-9_\.-]*)\.py$', file, re.I)
            if m:
                try:
                    i = __import__("%s.%s" % (parentmodule, m.group('module')), globals(), locals(), [parentmodule], -1)
                except Exception, e:
                    print e.message
                else:
                    imported.append(i)

    return imported


def register_plugins():
    registered_plugins = {}
    for plugin in import_plugins():
        try:
            mwt.logger.debug("Registering Task Plugin '%s'" % plugin.__name__)
            tasks.register(plugin.Main)
        except Exception, e:
            mwt.logger.warn("Failed to register Task Plugin '%s': %s" % (plugin, e.message))
        else:
            Plugin.objects.get_or_create(dsn=plugin.__name__)
            registered_plugins[plugin.__name__] = plugin.Main
    return registered_plugins