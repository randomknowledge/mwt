import subprocess
from django.utils import simplejson
import os
from django.conf import settings
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


class CasperJSTask(BaseTaskPlugin):

    def __init__(self):
        self.PHANTOM_JS_BIN = settings.PHANTOM_JS_BIN or 'phantomjs'
        self.CASPER_JS_BIN = settings.CASPER_JS_BIN or 'casperjs'
        os.environ['PHANTOMJS_EXECUTABLE']  = self.PHANTOM_JS_BIN
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.cmd = ('%s %s/js/%s.js' % (self.CASPER_JS_BIN, self.current_dir, self.__class__.__module__.split('.').pop())).split()
        self.javascript_result = {}

    def addJavaScriptParameter(self, param):
        self.cmd.append(param)

    def runJavaScript(self):
        try:
            output = subprocess.check_output(self.cmd)
        except AttributeError:
            output = subprocess.Popen(self.cmd, stdout=subprocess.PIPE).communicate()[0]

        self.javascript_result = simplejson.loads(output)