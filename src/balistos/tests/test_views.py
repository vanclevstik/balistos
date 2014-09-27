# -*- coding: utf-8 -*-
"""Tests."""

from pyramid import testing
from balistos.testing import createTestDB
from pyramid_basemodel import Session
import unittest


class TestHome(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home_no_user(self):
        from balistos.views.main import home
        request = testing.DummyRequest()
        result = home(request)
        self.assertIsNone(result['username'])


class TestHomeFunctional(unittest.TestCase):

    def setUp(self):
        from balistos import configure
        Session.remove()
        createTestDB()
        self.config = testing.setUp()
        configure(self.config)
        app = self.config.make_wsgi_app()
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(u'What is Balistos?', res.body)
