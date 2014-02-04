# -*- coding: utf-8 -*-
"""Application's views."""

from pyramid_layout.layout import layout_config
from pyramid.view import view_config
from balistos.static import balistos_assets


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
