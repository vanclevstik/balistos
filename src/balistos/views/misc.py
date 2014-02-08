# -*- coding: utf-8 -*-
"""Miscellanous views"""

from pyramid.response import Response
from pyramid.view import view_config

import os


_here = os.path.dirname(__file__)
_robots = open(os.path.join(_here, '../static', 'robots.txt')).read()
_robots_response = Response(content_type='text/plain',
                            body=_robots)

_icon = open(os.path.join(
             _here, '../static/img', 'favicon.ico')).read()
_fi_response = Response(content_type='image/x-icon',
                        body=_icon)


@view_config(name='favicon.ico')
def favicon_view(context, request):
    return _fi_response


@view_config(name='robots.txt')
def robotstxt_view(context, request):
    return _robots_response
