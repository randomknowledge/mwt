from .log import logger

try:
    from announce import AnnounceClient
except Exception:
    pass


def send_nodejs_notification(user_id, data):
    try:
        announce_client = AnnounceClient()
        announce_client.emit(
            user_id,
            'notifications',
            data=data
        )
        logger.info("Sent node.js notification to User %d" % user_id)
    except Exception, e:
        logger.warn(e.message)