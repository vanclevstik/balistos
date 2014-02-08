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
    relpath='css/balistos.css',
    minified='css/balistos.min.css',
    minifier='cssmin',
    depends=[bootstrap],
)

balistos_js = Resource(
    library=lib_balistos,
    relpath='js/balistos.js',
    minified='js/balistos.min.js',
    minifier='jsmin',
    depends=[jquery],
    bottom=True,
)

knockout_js = Resource(
    library=lib_balistos,
    relpath='js/knockout.js',
    minified='js/knockout.min.js',
    minifier='jsmin',
    bottom=True,
)

youtube_js = Resource(
    library=lib_balistos,
    relpath='js/youtube.js',
    minified='js/youtube.min.js',
    minifier='jsmin',
    depends=[jquery, knockout_js],
)

balistos_assets = Group([
    jquery,
    bootstrap,
    modernizr,
    balistos_js,
    balistos_css,
])
