from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Link(Base):
    __tablename__ = 'links'
    name = Column(String, unique=True, primary_key=True)
    nameId = Column(String, ForeignKey("pages.name"))

    def __init__(self, name, nameId):
        self.name = name
        self.nameId = nameId

    def __repr__(self):
        return self.name
