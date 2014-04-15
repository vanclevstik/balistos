# -*- coding: utf-8 -*-
"""Application initiallization"""

from balistos.models.user import User
from balistos.socialauth import SOCIAL_AUTH_SETTINGS
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import Everyone
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.view import notfound_view_config
from pyramid_basemodel import Base
from pyramid_basemodel import Session
from social.apps.pyramid_app.models import init_social
from sqlalchemy import engine_from_config


DEVELOPER_KEY = ''


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'user'),
        (Allow, 'admins', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        pass  # pragma: no cover


def groupfinder(username, request):
    user = User.get_by_username(username)
    if user and user.group:
        return [user.group.name, ]
    else:
        return []


@notfound_view_config()
def notfound(request):
    return render_to_response('templates/404.pt', {})


def configure(config, sqlite=True):
    config.include('pyramid_layout')

    config.include('pyramid_fanstatic')
    config.include('social.apps.pyramid_app')
    # routing
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_request_method('balistos.utils.get_user', 'user', reify=True)
    config.add_route('home', '/home')
    config.add_route('users', '/users')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('register', '/register')
    config.add_route('playlist_videos', '/playlist_videos')
    config.add_route('playlist_add_video', '/playlist_add_video')
    config.add_route('like_video', '/like_video')
    config.add_route('remove_video', '/remove_video')
    config.add_route('create_playlist', '/create_playlist')
    config.add_route('search_playlists', '/search_playlists')
    config.add_route('latest_playlists', '/latest_playlists')
    config.add_route('add_user_to_playlist', '/add_user_to_playlist')
    config.add_route('main', '/')
    config.add_route('set_playlist', '/playlist/{playlist}')
    config.add_route('chat_message', '/chat_message')
    ignores = ['balistos.tests', 'balistos.testing', ]
    if sqlite:
        ignores.append('balistos.models.postgres_indexes')
    config.scan('balistos', ignore=ignores)


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)

    session_factory = UnencryptedCookieSessionFactoryConfig(
        settings.get('session.secret', 'secret'),
    )

    authentication_policy = AuthTktAuthenticationPolicy(
        secret=settings.get('authtkt.secret', 'secret'),
        hashalg='sha512',
        callback=groupfinder,
        max_age=86400,
    )
    authorization_policy = ACLAuthorizationPolicy()

    SOCIAL_AUTH_SETTINGS['SOCIAL_AUTH_FACEBOOK_KEY'] = settings['social.facebook_key']  # noqa
    SOCIAL_AUTH_SETTINGS['SOCIAL_AUTH_FACEBOOK_SECRET'] = settings['social.facebook_secret']  # noqa
    SOCIAL_AUTH_SETTINGS['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'] = settings['social.google_key']  # noqa
    SOCIAL_AUTH_SETTINGS['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'] = settings['social.google_secret']  # noqa
    settings.update(SOCIAL_AUTH_SETTINGS)

    config = Configurator(
        settings=settings,
        root_factory=RootFactory,
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy,
        session_factory=session_factory,
    )
    is_sqlite = 'sqlite' in settings['sqlalchemy.url']
    configure(config, sqlite=is_sqlite)
    DEVELOPER_KEY = settings['balistos.youtube_key']  # noqa
    config.include('pyramid_basemodel')
    config.include('pyramid_tm')
    config.include('social.apps.pyramid_app')
    init_social(config, Base, Session)
    config.scan('social.apps.pyramid_app')

    return config.make_wsgi_app()
