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

    def test_home(self):
        from balistos.views.main import home
        request = testing.DummyRequest()
        result = home(request)
        self.assertEqual(result['name'], 'balistos')


class TestHomeFunctional(unittest.TestCase):

    def setUp(self):
        from balistos import configure
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
        res = self.testapp.get('/home', status=200)
        self.assertIn(u'balistos!', res.body)
