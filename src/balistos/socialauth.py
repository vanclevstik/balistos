# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from social.strategies.pyramid_strategy import PyramidStrategy


SOCIAL_AUTH_SETTINGS = {
    'SOCIAL_AUTH_LOGIN_URL': '/',
    'SOCIAL_AUTH_LOGIN_REDIRECT_URL': '/home',
    'SOCIAL_AUTH_USER_MODEL': 'balistos.models.user.User',
    'SOCIAL_AUTH_LOGIN_FUNCTION': 'balistos.socialauth.login_user',
    'SOCIAL_AUTH_LOGGEDIN_FUNCTION': 'balistos.socialauth.login_required',
    'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': (
        'social.backends.google.GoogleOAuth2',
        'social.backends.facebook.FacebookOAuth2',
        ),
    'SOCIAL_AUTH_STRATEGY': 'balistos.socialauth.PyramidStrategy'
}


def login_user(strategy, user):
    """
    Login user with newly made user model connected to social auth

    :param    strategy: strategy for social auth
    :type     strategy: balistos.socialauth.PyramidStrategy
    :param    user:     logged in user
    :type     user:     balistos.models.user.User
    """
    strategy.request.session['username'] = user.username
    headers = remember(strategy.request, user.username)
    strategy.request.response.headerlist.extend(headers)


def login_required(request):
    """
    Checks if login is required

    :param    request: Curren request
    :type     request: pyramid.request.Request
    """
    return getattr(request, 'user', None) is not None


class PyramidStrategy(PyramidStrategy):
    """
    Extends existing strategy to also support setting correct headers
    """

    def redirect(self, url):
        """Return a response redirect to the given URL"""
        return HTTPFound(location=url, headers=self.request.response.headers)
