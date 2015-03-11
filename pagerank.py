import argparse
import random
import csv
from collections import Counter
from scraper import Scraper

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
parser.add_argument('-f', '--output-file', help='The file to write results to')
parser.add_argument('-s', '--start', help='The url to start at.',
        type=int)


def pagerank(scraper, start, num_transitions, default, output_file):
    url = start
    cnt = Counter()
    for _ in range(num_transitions):
        valid_links = scraper.get_valid_links(url)
        if valid_links:
            url = random.choice(valid_links)
            cnt[url] += 1
        else:
            url = default
    if output_file:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for page in cnt.most_common():
                writer.writerow(page)
    else:
        print(cnt.most_common(50))


if __name__ == '__main__':
    args = parser.parse_args()
    start = args.start or args.default
    if not start:
        parser.error('You must provide a start url (-s/--start) if you don\'t '
            'provide a default url (-u/--default).')
    scraper = Scraper(args.domain)
    pagerank(scraper, start, args.transitions, args.default, args.output_file)
