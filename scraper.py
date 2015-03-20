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
        valid_links = []
        try:
            html = urlopen(url).read()
            soup = BeautifulSoup(html)
            for tag in soup.findAll('a', href=True):
                parsed_href = urlparse(tag['href'])
                if parsed_href.netloc:
                    href = ''.join(parsed_href[:-1])
                else:
                    href = urljoin(url, ''.join(parsed_href[:-1]))
                if href != url and self.is_url_valid(href):
                    valid_links.append(href)
        finally:
            return valid_links

class WikiScraper(Scraper):

    def is_url_valid(self, url):
        """Check if an absolute url is valid"""
        if ':' in urlparse(url).path:
            return False
        stripped = self.strip_scheme(url)
        return stripped.startswith(self.domain)
