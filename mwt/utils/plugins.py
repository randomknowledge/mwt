from .. import tasks
from .exceptions import get_stacktrace_string
from .log import logger


def update_plugins(update_db=False, force=False):
    tasks.registered_tasks = {}
    tasks.registered_notifications = {}

    try:
        tasks.registered_tasks = tasks.register_plugins('tasks', update_db=update_db, force=force)
        tasks.registered_notifications = tasks.register_plugins('notifications', update_db=update_db, force=force)
    except Exception:
        logger.log('error', "Couldn't register Plugins: %s"
        % get_stacktrace_string())
