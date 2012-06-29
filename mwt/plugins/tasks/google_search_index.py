from . import CasperJSTaskPlugin


__version__ = (0, 0, 2)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT Google Search Index Plugin'
__description__ = """MWT Google Search Index Plugin
Checks the position in google search for a given keyword.
"""
__params__ = ['search', 'url_regex']


class Main(CasperJSTaskPlugin):
    def process(self):
        search = self.options.get('search')
        url_regex = self.options.get('url_regex')

        self.addNamedJavaScriptParameter('search', search)
        self.addNamedJavaScriptParameter('url_pattern', url_regex)
        self.runJavaScript()

        if self.javascript_result.get('success'):
            self.successmessage = self.javascript_result_string
        else:
            raise Exception("CasperJS was unsuccessful: %s" % self.javascript_result_string)
