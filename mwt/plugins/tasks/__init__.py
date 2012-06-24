from celery.task import Task
from ...utils.exceptions import get_stacktrace_string
from ...utils.log import logger


class BaseTaskPlugin(Task):
    testrun = None
    successmessage = ''
    options = {}


    def run(self, run_obj, **kwargs):
        self.testrun = run_obj
        self.options = run_obj.test.get_options_for_plugin_dsn(plugin_dsn=str(self.__module__))

        try:
            self.startrun()
            self.process()
        except Exception:
            logger.log('fatal', "Test failed: %s" % get_stacktrace_string())
            self.testrun.fail(get_stacktrace_string())
        else:
            self.endrun()

    def startrun(self):
        self.testrun.start()

    def process(self):
        pass

    def endrun(self):
        self.testrun.success(self.successmessage)