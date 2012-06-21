from celery.task import Task
from mwt import logger

class BaseTaskPlugin(Task):
    testrun = None
    successmessage = ''

    def run(self, run_obj, **kwargs):
        self.testrun = run_obj

        try:
            self.startrun()
            self.process()
        except Exception, e:
            logger.fatal("Test failed: %s" % e)
            self.testrun.fail(e)
        else:
            self.endrun()

    def startrun(self):
        self.testrun.start()

    def process(self):
        pass

    def endrun(self):
        self.testrun.success(self.successmessage)