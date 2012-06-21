from . import tasks
from mwt.utils.exceptions import get_stacktrace_string
from .utils.log import logger

registered_plugins = {}

try:
    registered_plugins = tasks.register_plugins()
except Exception, e:
    logger.log('error', "Couldn't register Plugins: %s" % get_stacktrace_string())