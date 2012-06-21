from urllib2 import urlopen
from mwt.plugins.tasks import BaseTaskPlugin


__version__ = (0, 1, 2)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT Server Reachabe Plugin'
__description__ = """MWT Server Reachabe Plugin.
Simply checks if a remote Server is reachable via HTTP
"""


class Main(BaseTaskPlugin):
    def process(self):
        url = urlopen(self.testrun.test.url, None, 30)
        self.successmessage = url.info()
