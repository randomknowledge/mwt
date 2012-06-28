from . import CasperJSTask


__version__ = (0, 0, 2)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT Google Search Index Plugin'
__description__ = """MWT Google Search Index Plugin
Checks the position in google search for a given keyword.
"""
__params__ = ['search', 'url_regex']


class Main(CasperJSTask):
    def process(self):
        search = self.options.get('search')
        url_regex = self.options.get('url_regex')

        self.addJavaScriptParameter(search)
        self.addJavaScriptParameter(url_regex)
        self.runJavaScript()

        if self.javascript_result.get('success'):
            idx = self.javascript_result.get('searchIndex', 0)
            if idx > 0:
                self.successmessage = "'%s' found at position %d." % (search, idx)
            else:
                self.successmessage = "'%s' is not in the first %d results." % (search, self.javascript_result.get('maxIndex'))
        else:
            raise Exception("CasperJS was unsuccessful: %s" % self.javascript_result.get('message'))
