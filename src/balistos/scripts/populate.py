# -*- coding: utf-8 -*-
"""TODO: docstring"""

from datetime import datetime
from pyramid_basemodel import Base
from pyramid_basemodel import Session
from balistos.models.user import User
from balistos.models.user import Group
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

        admin_group = Group(name='admins')
        Session.add(admin_group)
        Session.flush()
        test_user = User(
            username='test_user',
            email='test@bar.com',
            fullname=u'Test User',
            # password = 'secret', pregenerated hash to speed up tests
            password=u'3d91b58504a6cc3a159005ee7b16c7ae503ca6ac2a6a3c893837083c236b864a',  # noqa
            group=admin_group,
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
            title=u'fernando torres song with lyric',
            image_url='http://i1.ytimg.com/vi/cpV0ygkmhP4/mqdefault.jpg',
            likes=0,
            youtube_video_id='cpV0ygkmhP4',
            duration=50,
        )

        test_clip2 = Clip(
            title=u'nba spoof',
            image_url='http://i1.ytimg.com/vi/cpV0ygkmhP4/mqdefault.jpg',
            likes=0,
            youtube_video_id='hi60QeNjIDk',
            duration=136,
        )
        Session.add(test_clip)
        Session.add(test_clip2)
        test_playlist_clip = PlaylistClip(
            likes=0,
            added=datetime.now(),
            started=datetime.now(),
            state=2,
            clip=test_clip,
            playlist=test_playlist,
            username=test_user.username,
        )
        test_playlist_clip2 = PlaylistClip(
            likes=0,
            added=datetime.now(),
            state=1,
            clip=test_clip2,
            playlist=test_playlist,
            username=test_user.username,
        )
        Session.add(test_playlist_clip)
        Session.add(test_playlist_clip2)


def main(argv=sys.argv):

    # TODO: check for DB existance etc.? this fails if run more than once
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print 'DATABASE_URL not set, using default SQLite db.'  # noqa
        db_url = 'sqlite:///./balistos-app.db'
    else:
        # import on production (postgresql)
        import balistos.models.postgres_indexes  # noqa

    settings = {'sqlalchemy.url': db_url}
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    insert_data()
    print 'DB populated with dummy data: {0}'.format(db_url)  # noqa


if __name__ == '__main__':
    main()
