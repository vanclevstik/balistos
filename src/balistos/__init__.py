# -*- coding: utf-8 -*-
"""Application initiallization"""

from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid_basemodel import Session
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.view import notfound_view_config
from sqlalchemy import engine_from_config


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
    ]

    def __init__(self, request):
        pass  # pragma: no cover


@notfound_view_config()
def notfound(request):
    return render_to_response('templates/404.pt', {})


def configure(config):
    config.include('pyramid_layout')

    config.include('pyramid_fanstatic')
    # routing
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/home')
    config.add_route('users', '/users')
    config.add_route('playlist_video', '/playlist_video')
    config.add_route('main', '/')
    config.scan('balistos', ignore=['balistos.tests', 'balistos.testing'])


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
    )
    authorization_policy = ACLAuthorizationPolicy()
    config = Configurator(
        settings=settings,
        root_factory=RootFactory,
        authentication_policy=authentication_policy,
        authorization_policy=authorization_policy,
        session_factory=session_factory,
    )
    configure(config)

    config.include('pyramid_basemodel')
    config.include('pyramid_tm')
    return config.make_wsgi_app()
