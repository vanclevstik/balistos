# -*- coding: utf-8 -*-
"""Test models."""

from pyramid import testing
from pyramid_basemodel import Session
from balistos.testing import createTestDB

import unittest


class TestUser(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        createTestDB()

    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_username(self):
        from balistos.models.user import User
        self.assertIsNotNone(User.get_by_username('test_user'))

    def test_add_user(self):
        from balistos.models.user import User
        user = User(
            username='test',
            email='foo@bar.com',
            fullname=u'Főo čar'
        )
        Session.add(user)
        Session.flush()
        user = User.get_by_username('test')
        self.assertEqual('test', user.username)
        self.assertEqual('foo@bar.com', user.email)
        self.assertEqual(u'Főo čar', user.fullname)

    def test_add_user_username_only(self):
        from balistos.models.user import User
        user = User(username='test')
        Session.add(user)
        Session.flush()
        user = User.get_by_username('test')
        self.assertEqual('test', user.username)
        self.assertIsNone(user.email)
        self.assertIsNone(user.fullname)

    def test_user_get_all(self):
        from balistos.models.user import User
        users = User.get_all()
        self.assertEqual(1, users.count())
        self.assertEqual('test_user', users[0].username)

    def test_user_get_all_filter_by(self):
        from balistos.models.user import User
        users = User.get_all(filter_by={'fullname': u'Test User'})
        self.assertEqual(1, users.count())
        self.assertEqual('test_user', users[0].username)

    def test_user_get_all_empty(self):
        from balistos.models.user import User
        user = User.get_by_username('test_user')
        Session.delete(user)
        Session.flush()
        self.assertEqual(0, User.get_all().count())
        self.assertIsNone(User.get_by_username('test_user'))


class TestPlaylist(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        createTestDB()

    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_get_uri(self):
        from balistos.models.playlist import Playlist

        playlist = Playlist.get('test_playlist')
        self.assertEqual('test_playlist', playlist.uri)
        self.assertEqual(u'Test Playlist', playlist.title)

    def test_add_playlist(self):
        from balistos.models.playlist import Playlist

        playlist = Playlist(uri='test', title=u'Test')
        Session.add(playlist)
        Session.flush()
        playlist = Playlist.get('test')
        self.assertEqual('test', playlist.uri)
        self.assertEqual(u'Test', playlist.title)

    def test_playlist_get_all(self):
        from balistos.models.playlist import Playlist
        playlists = Playlist.get_all()
        self.assertEqual(1, playlists.count())
        self.assertEqual('test_playlist', playlists[0].uri)

    def test_playlist_get_all_filter_by(self):
        from balistos.models.playlist import Playlist
        playlists = Playlist.get_all(filter_by={'title': u'Test Playlist'})
        self.assertEqual(1, playlists.count())
        self.assertEqual('test_playlist', playlists[0].uri)

    def test_playlist_get_all_filter_by_empty(self):
        from balistos.models.playlist import Playlist
        playlists = Playlist.get_all(filter_by={'title': u'Föo'})
        self.assertEqual(0, playlists.count())

    def test_playlist_get_all_empty(self):
        from balistos.models.playlist import Playlist
        playlist = Playlist.get('test_playlist')
        Session.delete(playlist)
        Session.flush()
        self.assertEqual(0, Playlist.get_all().count())
        self.assertIsNone(Playlist.get('test_playlist'))


class TestClip(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        createTestDB()

    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_get_uri(self):
        from balistos.models.clip import Clip

        clip = Clip.get('cpV0ygkmhP4')
        self.assertEqual('cpV0ygkmhP4', clip.youtube_video_id)
        self.assertEqual(u'fernando torres song with lyric', clip.title)

    def test_add_clip(self):
        from balistos.models.clip import Clip

        clip = Clip(
            youtube_video_id='test',
            title=u'Test',
            likes=5,
            image_url='test_url',
            duration=1,
        )
        Session.add(clip)
        Session.flush()
        clip = Clip.get('test')
        self.assertEqual('test', clip.youtube_video_id)
        self.assertEqual(u'Test', clip.title)
        self.assertEqual(5, clip.likes)
        self.assertEqual('test_url', clip.image_url)
        self.assertEqual(1, clip.duration)

    def test_clip_get_all(self):
        from balistos.models.clip import Clip
        clips = Clip.get_all()
        self.assertEqual(2, clips.count())
        self.assertEqual('cpV0ygkmhP4', clips[0].youtube_video_id)

    def test_clip_get_all_filter_by(self):
        from balistos.models.clip import Clip
        clips = Clip.get_all(filter_by={'likes': 0})
        self.assertEqual(2, clips.count())
        self.assertEqual('cpV0ygkmhP4', clips[0].youtube_video_id)

    def test_clip_get_all_empty(self):
        from balistos.models.clip import Clip
        clips = Clip.get_all()
        for clip in clips:
            Session.delete(clip)
        Session.flush()
        self.assertEqual(0, Clip.get_all().count())
        self.assertIsNone(Clip.get('cpV0ygkmhP4'))


class TestPlaylistClip(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        createTestDB()

    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_get_by_playlist_and_clip(self):
        from balistos.models.clip import PlaylistClip
        from balistos.models.clip import Clip
        from balistos.models.playlist import Playlist

        playlist = Playlist.get('test_playlist')
        clip = Clip.get('cpV0ygkmhP4')
        pclip = PlaylistClip.get_by_playlist_and_clip(playlist, clip)
        self.assertEqual(playlist, pclip.playlist)
        self.assertEqual(clip, pclip.clip)
        self.assertEqual(2, pclip.state)
        self.assertEqual(0, pclip.likes)

    def test_add_pclip(self):
        from balistos.models.clip import PlaylistClip
        from balistos.models.clip import Clip
        from balistos.models.playlist import Playlist
        from datetime import datetime

        playlist = Playlist(uri='test', title=u'Test')
        clip = Clip(
            youtube_video_id='test',
            title=u'Test',
            likes=5,
            image_url='test_url',
            duration=1
        )
        Session.add(clip)
        Session.add(playlist)
        Session.flush()

        pclip = PlaylistClip(
            playlist=playlist,
            clip=clip,
            likes=0,
            state=0,
            added=datetime.now()
        )
        Session.add(pclip)
        Session.flush()
        pclip = PlaylistClip.get_by_playlist_and_clip(playlist, clip)
        self.assertEqual(playlist, pclip.playlist)
        self.assertEqual(clip, pclip.clip)
        self.assertEqual(0, pclip.state)
        self.assertEqual(0, pclip.likes)

    def test_pclip_get_all(self):
        from balistos.models.clip import PlaylistClip
        pclips = PlaylistClip.get_all()
        self.assertEqual(2, pclips.count())

    def test_pclip_get_all_by_playlist(self):
        from balistos.models.clip import PlaylistClip
        from balistos.models.playlist import Playlist

        playlist = Playlist.get('test_playlist')
        pclips = PlaylistClip.get_by_playlist(playlist)
        self.assertEqual(2, len(pclips))

    def test_pclip_get_all_by_playlist_empty(self):
        from balistos.models.clip import PlaylistClip
        from balistos.models.playlist import Playlist

        playlist = Playlist(uri='test', title=u'Test')
        self.assertIsNone(PlaylistClip.get_by_playlist(playlist))

    def test_pclip_get_all_filter_by(self):
        from balistos.models.clip import PlaylistClip
        pclips = PlaylistClip.get_all(filter_by={'likes': 0})
        self.assertEqual(2, pclips.count())

    def test_pclip_get_all_empty(self):
        from balistos.models.clip import PlaylistClip
        pclips = PlaylistClip.get_all()
        for pclip in pclips:
            Session.delete(pclip)
        Session.flush()
        self.assertEqual(0, PlaylistClip.get_all().count())
        self.assertEqual(0, PlaylistClip.get_all().count())
