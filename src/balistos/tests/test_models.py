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

    def test_user_get_all_empty(self):
        from balistos.models.user import User
        user = User.get_by_username('test_user')
        Session.delete(user)
        Session.flush()
        self.assertEqual(0, User.get_all().count())


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

    def test_playlist_get_all_empty(self):
        from balistos.models.playlist import Playlist
        playlist = Playlist.get('test_playlist')
        Session.delete(playlist)
        Session.flush()
        self.assertEqual(0, Playlist.get_all().count())
