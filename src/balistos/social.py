# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from pyramid.events import BeforeRender

from social.apps.pyramid_app.utils import backends


def login_user(strategy, user):
    strategy.request.session['user_id'] = user.id


def login_required(request):
    return getattr(request, 'user', None) is not None


@subscriber(BeforeRender)
def add_social(event):
    request = event['request']
    event['social'] = backends(request, request.user)
