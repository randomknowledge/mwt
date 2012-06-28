from django.conf import settings
import subprocess
import os
from django.utils import simplejson

from . import BaseTaskPlugin


__version__ = (0, 0, 2)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT Google Search Index Plugin'
__description__ = """MWT Google Search Index Plugin
Checks the position in google search for a given keyword.
"""
__params__ = ['search', 'url_regex']


class Main(BaseTaskPlugin):
    def process(self):

        PHANTOM_JS_BIN = settings.PHANTOM_JS_BIN or 'phantomjs'
        CASPER_JS_BIN = settings.CASPER_JS_BIN or 'casperjs'
        os.environ['PHANTOMJS_EXECUTABLE']  = PHANTOM_JS_BIN

        current_dir = os.path.dirname(os.path.abspath(__file__))
        cmd = ('%s %s/js/google_search_index.js' % (CASPER_JS_BIN, current_dir)).split()

        search = self.options.get('search')
        url_regex = self.options.get('url_regex')

        cmd.append(search)
        cmd.append(url_regex)

        try:
            output = subprocess.check_output(cmd)
        except AttributeError:
            output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

        result = simplejson.loads(output)

        if result.get('success'):
            idx = result.get('searchIndex', 0)
            if idx > 0:
                self.successmessage = "'%s' found at position %d." % (search, idx)
            else:
                self.successmessage = "'%s' is not in the first %d results." % (search, result.get('maxIndex'))
        else:
            raise Exception("CasperJS was unsuccessful: %s" % result.get('message'))
