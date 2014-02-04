# -*- coding: utf-8 -*-
"""Static resources (JS/CSS/images) for balistos apps."""

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.bootstrap import bootstrap
from js.jquery import jquery
from js.modernizr import modernizr

import logging

logger = logging.getLogger(__name__)


lib_balistos = Library('balistos', 'static')

balistos_css = Resource(
    library=lib_balistos,
    relpath='balistos.css',
    minified='balistos.min.css',
    minifier='cssmin',
    depends=[bootstrap],
)

balistos_js = Resource(
    library=lib_balistos,
    relpath='balistos.js',
    minified='balistos.min.js',
    minifier='jsmin',
    depends=[jquery],
    bottom=True,
)

balistos_assets = Group([
    jquery,
    bootstrap,
    modernizr,
    balistos_js,
    balistos_css,
])
