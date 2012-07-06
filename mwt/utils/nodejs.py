from .log import logger
from .exceptions import get_stacktrace_string
from .. import constants

try:
    from announce import AnnounceClient
except Exception:
    pass


def send_nodejs_notification(user_id, data):
    if not constants.MWT_SETTINGS.get('use_nodejs', False):
        return

    try:
        announce_client = AnnounceClient()
        announce_client.emit(
            user_id,
            'notifications',
            data=data
        )
        logger.info("Sent node.js notification to User %d" % user_id)
    except Exception:
        logger.warn(get_stacktrace_string())