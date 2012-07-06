from redis.client import Redis
from rq.connections import get_current_connection, push_connection
from rq.queue import Queue
from .log import logger
from .. import constants


def setup_rq_connection():
    redis_conn = get_current_connection()
    if redis_conn is None:
        opts = constants.REDIS_SETTINGS.get('connection')
        logger.debug('Establishing Redis connection to DB %(db)s at %(host)s:%(port)s' % opts)
        redis_conn = Redis(**opts)
        push_connection(redis_conn)


def enqueue(function, *args, **kwargs):
    if constants.REDIS_SETTINGS.get('eager', False):
        return function(*args, **kwargs)

    setup_rq_connection()
    queue_prefix = constants.REDIS_SETTINGS.get('queue_prefix')
    queue = queue_prefix + kwargs.pop('queue', 'tasks')
    timeout = kwargs.pop('timeout', 180)
    return Queue(queue).enqueue(function, *args, timeout=timeout, **kwargs)


def set_value(key, value):
    setup_rq_connection()
    if value is None:
        delete_key(key)
    elif type(value) in [int, float, long, bool, str, unicode]:
        get_current_connection().set(key, value)
    elif type(value) in [list, tuple]:
        delete_key(key)
        for entry in value:
            get_current_connection().rpush(key, entry)
    else:
        raise ValueError("Type '%s' not supported!" % type(value))


def get_value(key):
    setup_rq_connection()
    keytype = get_current_connection().type(key)
    if keytype == 'list':
        return get_current_connection().lrange(key, 0, -1)
    else:
        return get_current_connection().get(key)


def add_to_list(key, value):
    setup_rq_connection()
    keytype = get_current_connection().type(key)
    if keytype == 'none':
        set_value(key, [value,])
    elif keytype == 'list':
        get_current_connection().rpush(key, value)


def delete_key(key):
    get_current_connection().delete(key)
