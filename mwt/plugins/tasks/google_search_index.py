import re
import urllib
from selenium import webdriver

from . import BaseTaskPlugin


__version__ = (0, 0, 1)
__author__ = 'Florian Finke <flo@randomknowledge.org>'
__pluginname__ = 'MWT Google Search Index Plugin'
__description__ = """MWT Google Search Index Plugin
Checks the position in google search for a given keyword.
"""
__params__ = ['search', 'url_regex']


class Main(BaseTaskPlugin):
    def process(self):
        search = self.options.get('search')
        re_url_string = self.options.get('url_regex')
        re_url = re.compile(r'%s' % re_url_string, re.I)

        # TODO: Create generic Firefox profile with more than ten Google search results per page
        #browser = webdriver.Firefox(firefox_profile=FirefoxProfile(profile_directory='/home/flo/.mozilla/firefox/bfdcpq2t.default'))
        browser = webdriver.Firefox()
        try:
            browser.get("http://www.google.de/search?hl=de&%s" % urllib.urlencode({'q': search}))
            idx = 0
            match = None
            for li in browser.find_elements_by_xpath("//li[@class='g']"):
                idx += 1
                anchors = li.find_elements_by_xpath(".//a")
                for anchor in anchors:
                    href = anchor.get_attribute('href')
                    if href and re.match(re_url,href):
                        match = idx
                        break
        except Exception, e:
            raise e
        finally:
            browser.close()

        if match:
            self.successmessage = "Search for '%s': Found '%s' at position %d" % (search, re_url_string, match)
        else:
            self.successmessage = "Search for '%s': '%s' not found :(" % (search, re_url_string)