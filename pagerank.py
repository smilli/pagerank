import argparse

parser = argparse.ArgumentParser(description='Domain-specific PageRank')
parser.add_argument('-d', '--domain', help='The domain that the search should '
    'be restricted to.  All URLs prefixed by this will be visited. '
    '"http://" or "www" is not necessary.  Ex: "en.wikipedia.org/wiki/"',
    required=True)
parser.add_argument('-t', '--transitions', help='The number of transitions or '
    'pages to visit.  Ex: 10000', type=int, required=True)
parser.add_argument('-u', '--default', help='The url that the search will '
    'default to when it gets to a dead end. Use if you have a URL that '
    'provides a random page on the domain. '
    'Ex: en.wikipedia.org/wiki/Special:Random')
args = parser.parse_args()

def pagerank():
    pass

if __name__ == '__main__':
    pass
