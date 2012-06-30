from datetime import datetime
from urllib2 import urlopen
from django.utils import simplejson
from ..tasks import BaseTaskPlugin


__version__ = (0, 1, 2)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT Server Reachabe Plugin'
__description__ = """MWT Server Reachabe Plugin.
Simply checks if a remote Server is reachable via HTTP
"""
__params__ = ['url']

class Main(BaseTaskPlugin):
    def process(self):
        t = datetime.utcnow()
        url = urlopen(self.options.get('url'), None, 30)
        elapsed = datetime.utcnow() - t
        self.result = simplejson.dumps({
            'success': True,
            'message': "Server reponded in %s" % elapsed,
            'headers': "\n<headers>\n%s\n</headers>" % str(url.info()).strip()
        })

