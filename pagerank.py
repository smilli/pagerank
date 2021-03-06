import argparse
import random
import sqlite3
import csv
from collections import Counter
from scraper import Scraper, WikiScraper
from db import DB

parser = argparse.ArgumentParser(description='Domain-specific PageRank')
parser.add_argument('-d', '--domain', help='The domain/path that the search '
    'should be restricted to.  Only urls prefixed by this will be visited. '
    'Ex: "http://en.wikipedia.org/wiki/"',
    required=True)
parser.add_argument('-t', '--transitions', help='The number of transitions or '
    'pages to visit.  Ex: 10000', type=int, required=True)
parser.add_argument('-u', '--default', help='The url that the search will '
    'default to when it gets to a dead end. Use if you have a url that '
    'provides a random page on the domain. '
    'Ex: http://en.wikipedia.org/wiki/Special:Random')
parser.add_argument('-c', '--db', help='Database connection to store pages in '
    'Ex: postgresql://localhost/pagerank')
parser.add_argument('-s', '--start', help='The url to start at.')


class PageRanker():

    def __init__(self, scraper, start, default, db):
        self.scraper = scraper
        self.start = start
        self.default = default
        self.db = db

    def crawl(self, num_transitions):
        if self.start:
            queue = [self.start]
        else:
            queue = []
        i = 0
        while i < num_transitions:
            if not queue:
                queue += self.scraper.get_valid_links(self.default)
            else:
                link = queue.pop(0)
                print(link)
                outgoing = self.scraper.get_valid_links(link)
                saved = self.db.create_page(url=link, rank=1, links=outgoing)
                print(link, outgoing, saved)
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

    def get_top_ranked(self, num_to_get=None):
        return self.db.get_urls_ordered_by_rank(num_to_get)

if __name__ == '__main__':
    args = parser.parse_args()
    if not (args.start or args.default):
        parser.error('You must provide a start url (-s/--start) if you don\'t '
            'provide a default url (-u/--default).')
    scraper = Scraper(args.domain)
    pageranker = PageRanker(scraper, args.start, args.default, DB(args.db))
    pageranker.crawl(args.transitions)
    pageranker.update_ranks(25)
    print(pageranker.get_top_ranked(10))
