# -*- coding: utf-8 -*-
"""TODO: docstring"""

from datetime import datetime
from pyramid_basemodel import Base
from pyramid_basemodel import Session
from balistos.models.user import User
from balistos.models.playlist import Playlist
from balistos.models.playlist import PlaylistUser
from balistos.models.clip import Clip
from balistos.models.clip import PlaylistClip
from sqlalchemy import engine_from_config

import os
import sys
import transaction


def insert_data():
    with transaction.manager:
        test_user = User(
            username='test_user',
            email='test@bar.com',
            fullname=u'Test User',
        )
        Session.add(test_user)

        test_playlist = Playlist(
            uri='test_playlist',
            title=u'Test Playlist',
        )
        Session.add(test_playlist)
        test_playlist_user = PlaylistUser(
            playlist=test_playlist,
            user=test_user,
            permission=0
        )
        Session.add(test_playlist_user)
        test_clip = Clip(
            likes=0,
            youtube_video_id='test_id'
        )
        Session.add(test_clip)
        test_playlist_clip = PlaylistClip(
            likes=0,
            added=datetime.now(),
            active=True
        )
        Session.add(test_playlist_clip)


def main(argv=sys.argv):

    # TODO: check for DB existance etc.? this fails if run more than once
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print 'DATABASE_URL not set, using default SQLite db.'  # noqa
        db_url = 'sqlite:///./balistos-app.db'

    settings = {'sqlalchemy.url': db_url}
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    insert_data()

    print 'DB populated with dummy data: {0}'.format(db_url)  # noqa


if __name__ == '__main__':
    main()
