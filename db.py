from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker
from collections import Counter
from models import Page, PageLink, Base


class DB:

    def __init__(self, db_conn=None):
        if db_conn:
            self.engine = create_engine(db_conn)
        else:
            self.engine = create_engine('postgresql://localhost/pagerank')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def get_or_create(self, session, model, **kwargs):
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    def create_page(self, url, rank, links):
        """
        Create and save page.

        Params:
            url: [string] the url of the page
            rank: [float] the Pagerank score
            links: [links] outgoing links from page and their frequencies
        """
        num_links = len(links)
        links_counter = Counter(links)
        session = self.Session()
        try:
            page = self.get_or_create(session=session, model=Page,
                    url=url, rank=rank)
            if page.explored:
                return False
            for (link, num_occurences) in links_counter.most_common():
                outgoing_page = self.get_or_create(session=session,
                        model=Page, url=link, rank=rank)
                pagelink = PageLink(start_page_id=page.id,
                        outgoing_page_id=outgoing_page.id,
                        probability=num_occurences/num_links)
                session.add(pagelink)
            page.explored = True
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            return False
        return True

    def update_ranks(self):
        session = self.Session()
        try:
            for page_link in session.query(PageLink).all():
                page_link.pagerank_contrib = page_link.new_pagerank_contrib()
            for page, new_rank in session.query(Page,
                    func.sum(PageLink.pagerank_contrib)).filter(Page.id ==
                            PageLink.outgoing_page_id).group_by(Page.id).all():
                page.rank = new_rank
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            return False
        return True

    def get_urls_ordered_by_rank(self, limit):
        """
        Get pages ordered by rank (descending).
        """
        session = self.Session()
        if not limit:
            pages = session.query(Page.url).order_by(Page.rank.desc()).all()
        else:
            pages = (session.query(Page.url).order_by(Page.rank.desc()).
                    limit(limit).all())
        return pages
