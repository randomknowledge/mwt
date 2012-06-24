from django.conf import settings
import logging
import sys
import inspect


class Logger(object):
    debug = lambda self, *args, **kwargs: self.log('debug', *args, **kwargs)
    info = lambda self, *args, **kwargs: self.log('info', *args, **kwargs)
    warn = lambda self, *args, **kwargs: self.log('warn', *args, **kwargs)
    warning = lambda self, *args, **kwargs: self.log('warn', *args, **kwargs)
    error = lambda self, *args, **kwargs: self.log('error', *args, **kwargs)
    fatal = error

    def log(self, level, message, *args, **kwargs):
        '''
        Log the specified message with log level "level".

        Level can be one of 'debug', 'info', 'notice', 'warning', 'error'/'fatal'.
        Messages can contain placeholders "%s" with the actual content in *args.
        Sentry will group messages with the same message and only different args.

        If there's a keyword argument "request" with a Django request object, details
        about the request will be logged as well.
        If there's a keyword argument "exception" which evaluates as True, all
        details about the last exception will be captured as well
        '''
        kw = {}
        if 'request' in kwargs:
            kw['extra'] = {'request': kwargs['request']}

            if kwargs['request'].user.is_authenticated():
                kw['extra']['data'] = {
                    'data': {'username': kwargs['request'].user.username},
                    }

        if 'exception' in kwargs:
            exc = sys.exc_info()
            if exc[0] is not None:
                kw['exc_info'] = exc

        # walk up the call stack and get the callers __name__
        caller = inspect.getmodule(inspect.stack()[2][0])
        if caller:
            caller = caller.__name__
        else:
            caller = settings.PROJECT_NAME
        getattr(logging.getLogger(caller), level.lower())(message, *args, **kw)

logger = Logger()
