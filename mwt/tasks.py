import sys
from .models.plugins import TaskPlugin, NotificationPlugin
from . import helper
from .utils.exceptions import get_stacktrace_string
from .plugins.tasks import BaseTaskPlugin
from .plugins.notifications import BaseNotificationPlugin
from .utils.log import logger
import os
import re


def import_plugins(type):
    s_plugins = 'plugins'
    s_tasks = type
    imported = []
    parentmodule = "mwt.%s.%s" % (s_plugins, s_tasks)
    basedir = os.path.dirname(__file__)
    plugindir = os.path.join(basedir, s_plugins, s_tasks)

    if os.path.isdir(plugindir):
        for file in os.listdir(plugindir):
            m = re.match(r'^(?P<module>[a-z0-9][a-z0-9_\.-]*)\.py$', file, re.I)
            if m:
                mod = m.group('module')
                try:
                    dsn = "%s.%s" % (parentmodule, mod)
                    i = __import__(dsn, globals(), locals(), [parentmodule], -1)
                except Exception:
                    logger.error("Failed to import Plugin %s: %s" %
                            (mod, get_stacktrace_string()))
                else:
                    if (type == 'tasks' and hasattr(i, 'Main') and issubclass(i.Main, BaseTaskPlugin))\
                    or (type == 'notifications' and hasattr(i, 'Main') and issubclass(i.Main, BaseNotificationPlugin)):
                        imported.append(i)
                    else:
                        logger.error("Plugin '%s' doesn't extend "
                                "'BaseTaskPlugin/BaseNotificationPlugin' or doesn't have "
                                "a 'Main' class!" % mod)
                        try:
                            del sys.modules[dsn]
                            del i
                        except Exception:
                            pass

    return imported


def register_plugins(type):
    registered_plugins = {}
    for plugin in import_plugins(type):
        logger.log('debug', "Registering Plugin '%s'" % plugin.__name__)
        if type == 'tasks':
            p, created = TaskPlugin.objects.get_or_create(dsn=plugin.__name__)
        else:
            p, created = NotificationPlugin.objects.get_or_create(dsn=plugin.__name__)

        if created or p.versionnumber < helper.versionnumber(plugin.__version__):
            p.name = str(plugin.__pluginname__)
            p.author = str(plugin.__author__)
            p.description = str(plugin.__description__)
            p.versionfield = str(plugin.__version__)
            p.params = ','.join(plugin.__params__ or [])
            p.save()
        else:
            logger.log('debug', "Plugin '%s' with higher or same Version "
                                "already exists. Not creating Plugin object "
                                "in DB." % p.__unicode__())
        registered_plugins[plugin.__name__] = plugin.Main()
    return registered_plugins
