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
    get_current_connection().set(key, value)


def get_value(key):
    setup_rq_connection()
    return get_current_connection().get(key)


def set_run_finished(schedule_run_id):
    v = get_run_counter(schedule_run_id)
    set_value("mwt:schedule:%d" % schedule_run_id, v + 1)


def get_run_counter(schedule_run_id):
    v = 0
    try:
        v = int(get_value("mwt:schedule:%d" % schedule_run_id))
    except Exception:
        pass
    return v


def clear_run(schedule_run_id):
    setup_rq_connection()
    get_current_connection().delete("mwt:schedule:%d" % schedule_run_id)
