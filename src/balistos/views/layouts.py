# -*- coding: utf-8 -*-
"""Application's views."""

from pyramid_layout.layout import layout_config


@layout_config(name='default', template='balistos:templates/default_layout.pt')
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
