# -*- coding: utf-8 -*-
"""Tests."""

from pyramid import testing

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
        from balistos import main
        settings = {'sqlalchemy.url': 'sqlite://'}
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/home', status=200)
        self.assertIn(b'balistos!', res.body)
