from sqlalchemy import (create_engine, Column, Float, Table, Integer, String,
        ForeignKey, Boolean)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Page(Base):

    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    rank = Column(Float)
    outgoing_links = association_proxy('outgoing_links', 'outgoing_page')
    incoming_links = association_proxy('incoming_links', 'start_page')
    explored = Column(Boolean)


class PageLink(Base):

    __tablename__ = 'pagelink'
    start_page_id = Column(Integer, ForeignKey('page.id'), primary_key=True)
    outgoing_page_id = Column(Integer, ForeignKey('page.id'), primary_key=True)
    probability = Column(Float)
    pagerank_contrib = Column(Float)
    start_page = relationship(Page,
            primaryjoin=(start_page_id == Page.id),
            backref='incoming_links')
    outgoing_page = relationship(Page,
            primaryjoin=(outgoing_page_id == Page.id),
            backref='outgoing_links')

    def new_pagerank_contrib(self):
        """
        Get start page's PageRank contribution to the outgoing page.
        """
        return self.start_page.rank * self.probability
