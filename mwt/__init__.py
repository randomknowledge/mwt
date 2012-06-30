from . import tasks
from .utils.exceptions import get_stacktrace_string
from .utils.log import logger


registered_tasks = {}
registered_notifications = {}

try:
    registered_tasks = tasks.register_plugins('tasks')
    registered_notifications = tasks.register_plugins('notifications')
except Exception, e:
    logger.log('error', "Couldn't register Plugins: %s"
            % get_stacktrace_string())
