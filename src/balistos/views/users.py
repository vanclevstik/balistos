# -*- coding: utf-8 -*-
"""User views"""

from balistos.static import balistos_assets
from balistos.models.user import User
from pyramid.view import view_config


@view_config(
    route_name='users',
    renderer='balistos:templates/users.pt',
    layout='default',
)
def users(request):
    """The users page."""
    balistos_assets.need()
    users = User.get_all()
    return {
        'users': users,
    }
