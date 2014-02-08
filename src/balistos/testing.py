# -*- coding: utf-8 -*-

from balistos.scripts.populate import insert_data
from pyramid_basemodel import Base
from pyramid_basemodel import Session
from sqlalchemy import create_engine


def createTestDB():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    insert_data()
