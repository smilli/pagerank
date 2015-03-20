Domain-Specific PageRank
=========================
Runs PageRank algorithm constrained to a certain path.

Install
=======
1. git clone https://github.com/smilli/pagerank.git
2. cd pagerank
3. pip install -r requirements.txt

Usage
=====
python pagerank.py[-h] -d DOMAIN -t TRANSITIONS [-u DEFAULT] [-c DB] [-s START]

Make sure you're using python3.

Arguments
=========
  -d DOMAIN, --domain DOMAIN
                        The domain/path that the search should be restricted to.
                        All urls prefixed by this will be visited. Ex:
                        "http://en.wikipedia.org/wiki/"
                        
  -t TRANSITIONS, --transitions TRANSITIONS
                        The number of transitions or pages to visit. Ex: 10000
                        
  -u DEFAULT, --default DEFAULT
                        The url that the search will default to when it gets
                        to a dead end. Use if you have a url that provides a
                        random page on the domain. Ex:
                        http://en.wikipedia.org/wiki/Special:Random
                        
  -c DB, --db DB        Database connection to store pages in Ex:
                        postgresql://localhost/pagerank
                        
  -s START, --start START
                        The url to start at.
