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

    def test_user(self):
        from balistos.models.user import User
        self.assertIsNotNone(User.get_by_username('test_user'))
