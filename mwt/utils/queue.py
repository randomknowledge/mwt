from redis.client import Redis
from rq.connections import get_current_connection, push_connection
from rq.queue import Queue
from .log import logger
from .. import constants

def setup_rq_connection():
    redis_conn = get_current_connection()
    if redis_conn == None:
        opts = constants.REDIS_SETTINGS.get('connection')
        logger.debug('Establishing Redis connection to DB %(db)s at %(host)s:%(port)s' % opts)
        redis_conn = Redis(**opts)
        push_connection(redis_conn)

def enqueue(function, *args, **kwargs):
    if constants.REDIS_SETTINGS.get('eager', False):
        return function(*args, **kwargs)

    setup_rq_connection()
    queue = kwargs.pop('queue', constants.REDIS_SETTINGS.get('queue', 'default'))
    timeout = kwargs.pop('timeout', 180)
    return Queue(queue).enqueue(function, *args, timeout=timeout, **kwargs)