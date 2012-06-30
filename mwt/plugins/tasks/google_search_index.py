from . import CasperJSTaskPlugin


__version__ = (0, 0, 2)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT Google Search Index Plugin'
__description__ = """MWT Google Search Index Plugin
Checks the position in google search for a given keyword.
"""
__params__ = ['search', 'url_regex', 'desired_searchindex']


class Main(CasperJSTaskPlugin):
    def process(self):
        search = self.options.get('search')
        url_regex = self.options.get('url_regex')
        desired_searchindex = self.options.get('desired_searchindex')

        self.addNamedJavaScriptParameter('search', search)
        self.addNamedJavaScriptParameter('url_pattern', url_regex)
        self.addNamedJavaScriptParameter('desired_searchindex', desired_searchindex)
        self.runJavaScript()

        if self.javascript_result.get('exception', False):
            raise Exception("CasperJS was unsuccessful: %s" % self.javascript_result.get('message'))

        self.result = self.javascript_result_string
