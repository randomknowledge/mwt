from . import tasks
import logging
from django.utils import log

logger  = logging.getLogger()

if not logger.handlers:
    logger.addHandler(log.NullHandler())

registered_plugins = {}

try:
    registered_plugins = tasks.register_plugins()
except Exception, e:
    logger.fatal("Couldn't register Plugins: %s" % e.message)