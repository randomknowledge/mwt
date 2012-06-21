from urllib2 import urlopen
from mwt.plugins.tasks import BaseTaskPlugin

class Main(BaseTaskPlugin):
    def process(self):
        url = urlopen(self.testrun.test.url)
        self.successmessage = url.info()