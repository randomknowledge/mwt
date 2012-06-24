from ...utils.exceptions import get_stacktrace_string
from ...utils.log import logger


class BaseTaskPlugin(object):
    testrun = None
    successmessage = ''
    options = {}

    def run(self, run_obj, **kwargs):
        self.testrun = run_obj
        self.options = run_obj.test.get_options_for_plugin_dsn(plugin_dsn=str(self.__module__))

        try:
            self._startrun()
            self.process()
        except Exception:
            logger.fatal("Test failed: %s" % get_stacktrace_string())
            self.testrun.fail(get_stacktrace_string())
        else:
            self._endrun()

    def _startrun(self):
        self.testrun.start()

    def process(self):
        pass

    def _endrun(self):
        self.testrun.success(self.successmessage)