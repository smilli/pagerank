import argparse
import random
import sqlite3
import csv
from collections import Counter
from scraper import Scraper
from db import DB

parser = argparse.ArgumentParser(description='Domain-specific PageRank')
parser.add_argument('-d', '--domain', help='The domain that the search should '
    'be restricted to.  All urls prefixed by this will be visited. '
    '"http://" or "www" is not necessary.  Ex: "en.wikipedia.org/wiki/"',
    required=True)
parser.add_argument('-t', '--transitions', help='The number of transitions or '
    'pages to visit.  Ex: 10000', type=int, required=True)
parser.add_argument('-u', '--default', help='The url that the search will '
    'default to when it gets to a dead end. Use if you have a url that '
    'provides a random page on the domain. '
    'Ex: http://en.wikipedia.org/wiki/Special:Random')
parser.add_argument('-f', '--sqlite-file', help='File to use for storing nodes '
    'and outgoing links')
parser.add_argument('-s', '--start', help='The url to start at.',
        type=int)


class PageRanker():

    def __init__(self, scraper, start, default, db):
        self.scraper = scraper
        self.start = start
        self.default = default
        self.db = db

    def crawl(self, num_transitions):
        if self.start:
            queue = [start]
        else:
            queue = []
        i = 0
        while i < num_transitions:
            if not queue:
                queue += self.scraper.get_valid_links(self.default)
            else:
                link = queue.pop(0)
                outgoing = self.scraper.get_valid_links(link)
                saved = self.db.create_page(url=link, rank=1, links=outgoing)
                if not saved:
                    continue
                queue += outgoing
                i += 1

    def update_ranks(self, num_iterations=1):
        """
        Update Pageranks for currently crawled websites.
        """
        for _ in range(num_iterations):
            self.db.update_ranks()


if __name__ == '__main__':
    args = parser.parse_args()
    if not (args.start or args.default):
        parser.error('You must provide a start url (-s/--start) if you don\'t '
            'provide a default url (-u/--default).')
    scraper = WikiScraper(args.domain) # can change to Scraper for general usage
    pageranker = PageRanker(scraper, args.start, args.default, DB())
    pageranker.crawl(args.transitions)
    pageranker.update_ranks()
