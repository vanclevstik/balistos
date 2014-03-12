# -*- coding: utf-8 -*-

from balistos.scripts.populate import insert_data
from pyramid_basemodel import Base
from pyramid_basemodel import Session
from sqlalchemy import create_engine


def createTestDB():
    engine = create_engine('sqlite:///:memory:')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
    insert_data()
