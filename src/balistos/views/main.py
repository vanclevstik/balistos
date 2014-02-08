# -*- coding: utf-8 -*-
"""Main views on front page"""

from balistos.static import balistos_assets
from balistos.static import youtube_js
from pyramid.view import view_config


@view_config(
    route_name='home',
    renderer='balistos:templates/home.pt',
    layout='default',
)
def home(request):
    """The home page."""
    balistos_assets.need()
    return {
        'name': 'balistos',
    }


@view_config(
    route_name='main',
    renderer='balistos:templates/main.pt',
    layout='default',
)
def main(request):
    """Main page view"""
    balistos_assets.need()
    youtube_js.need()
    return {}
