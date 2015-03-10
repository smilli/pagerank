from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin, urlparse

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
        url = ''.join(urlparse(url)[1:])
        if url.startswith('www.'):
            url = url.partition('www.')[2]
        return url

    def is_url_valid(self, url):
        """Check if an absolute url is valid"""
        stripped = self.strip_scheme(url)
        return stripped.startswith(self.domain)

    def get_valid_links(self, url):
        """Return list of valid links on the given url."""
        # TODO(smilli): figure out what to do with self-links
        valid_links = []
        html = urlopen(url).read()
        soup = BeautifulSoup(html)
        for tag in soup.findAll('a', href=True):
            new_url = urljoin(url, tag['href'])
            if self.is_url_valid(new_url):
                valid_links.append(new_url)
        return valid_links
