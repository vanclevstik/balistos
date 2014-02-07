# -*- coding: utf-8 -*-
"""Application's views."""

from balistos.static import balistos_assets
from pyramid.response import Response
from pyramid.view import view_config
from pyramid_layout.layout import layout_config

import os


@view_config(
    route_name='home',
    renderer='templates/home.pt',
    layout='default',
)
def home(request):
    """The home page."""
    balistos_assets.need()
    return {
        'name': 'balistos',
    }


@layout_config(name='default', template='templates/default_layout.pt')
class DefaultLayout(object):
    page_title = 'Balistos'

    def __init__(
        self,
        context,
        request,
        current_page='Home',
        hide_sidebar=False,
    ):
        self.context = context
        self.request = request
        self.current_page = current_page

_here = os.path.dirname(__file__)
_robots = open(os.path.join(_here, 'static', 'robots.txt')).read()
_robots_response = Response(content_type='text/plain',
                            body=_robots)


@view_config(name='robots.txt')
def robotstxt_view(context, request):
    return _robots_response
