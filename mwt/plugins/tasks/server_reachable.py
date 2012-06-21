from urllib2 import urlopen, URLError
from celery.task import Task
from mwt import logger

class Main(Task):
    def run(self, run, **kwargs):
        try:
            run.start()
            url = urlopen(run.test.url)
        except Exception, e:
            logger.fatal("Test failed: %s" % e)
            run.fail(e)
        else:
            run.success(url.info())