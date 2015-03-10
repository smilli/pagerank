from bs4 import BeautifulSoup
import urllib

class Scraper():

    def __init__(self, domain):
        """
        Constructor for Scraper.

        Args:
            domain: [string] path to restrict pages the Scraper visits. Only URLs
                prefixed by this path will be visited by the scraper.  Ex:
                'en.wikipedia.org/wiki'.
        """
        self.domain = self.strip_scheme(domain)

    def strip_scheme(self, url):
        """Return url without the scheme or 'www'."""
        pass

    def is_url_valid(self):
        """Check if a url is valid"""
        pass

    def get_valid_links(self, url):
        """Return list of valid links on the given url."""
        pass
