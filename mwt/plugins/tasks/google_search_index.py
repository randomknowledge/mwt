from . import CasperJSTaskPlugin
from django.utils import simplejson


__version__ = (0, 0, 2)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT Google Search Index Plugin'
__description__ = """MWT Google Search Index Plugin
Checks the position in google search for a given keyword.
"""
__params__ = {
    'search': {
        'description': u'Search Google for word(s)',
        'mandatory': True,
        'type': 'string',
        'must_match': '\S+',
        'default': '',
    },
    'url_regex': {
        'description': u'URL Regex to search for in results',
        'mandatory': True,
        'type': 'string',
        'must_match': '\S+',
        'default': '',
    },
    'desired_searchindex': {
        'description': u'',
        'mandatory': True,
        'type': 'number',
        'must_match': '^\d{1,3}$',
        'default': 1,
    },
}


class Main(CasperJSTaskPlugin):
    def process(self):
        search = self.options.get('search')
        url_regex = self.options.get('url_regex')
        desired_searchindex = self.options.get('desired_searchindex', 1)

        self.addNamedJavaScriptParameter('search', search)
        self.addNamedJavaScriptParameter('url_pattern', url_regex)
        self.addNamedJavaScriptParameter('desired_searchindex', desired_searchindex)
        self.runJavaScript()

        if self.javascript_result.get('exception', False):
            raise Exception("CasperJS was unsuccessful: %s" % self.javascript_result.get('message'))

        if not 'message' in self.javascript_result:
            if self.javascript_result.get('success', False):
                self.javascript_result['message'] = "'%s' found at position %d. "\
                        "Desired searchindex was %s"\
                        % (search, self.javascript_result.get('searchIndex', 999), desired_searchindex)
            elif self.javascript_result.get('searchIndex', 0) == 0:
                self.javascript_result['message'] = "'%s' not found. "\
                        "Scanned %d results. "\
                        "Desired searchindex was %s"\
                        % (search, self.javascript_result.get('maxIndex', 50), desired_searchindex)
            else:
                self.javascript_result['message'] = "'%s' found at position %d. "\
                        "Desired searchindex was %s"\
                        % (search, self.javascript_result.get('searchIndex', 999), desired_searchindex)
        self.result = simplejson.dumps(self.javascript_result)
