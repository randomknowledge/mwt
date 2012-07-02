from datetime import datetime
import urllib2
from django.utils import simplejson
from ..tasks import BaseTaskPlugin


__version__ = (0, 1, 3)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT Server Reachabe Plugin'
__description__ = """MWT Server Reachabe Plugin.
Simply checks if a remote Server is reachable via HTTP
"""
__params__ = ['url']


class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib2.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302


class Main(BaseTaskPlugin):

    def process(self):
        t = datetime.utcnow()
        server = self.options.get('url')

        opener = urllib2.build_opener(NoRedirectHandler())
        urllib2.install_opener(opener)

        exception = None
        headers = None

        try:
            url = urllib2.urlopen(server, None, 30)
        except urllib2.URLError, e:
            success = False
            elapsed = datetime.utcnow() - t
            message = "Server %s seams to be down. Didn't answer after %s" % (server, elapsed)
            exception = str(e.reason)
        else:
            info = url.info()
            headers = str(info).strip()
            elapsed = datetime.utcnow() - t
            success = True
            message = "Server %s reponded in %s" % (server, elapsed),
            if info.get('location', ''):
                success = False
                message = "Request on %s got header location: %s" % (server, info.get('location'))

        self.result = simplejson.dumps({
            'success': success,
            'message': message,
            'headers': headers,
            'exception': exception,
            })
