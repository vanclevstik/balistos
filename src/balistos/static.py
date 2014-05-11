# -*- coding: utf-8 -*-
"""Static resources (JS/CSS/images) for balistos apps."""

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.jquery import jquery
from js.modernizr import modernizr

import logging

logger = logging.getLogger(__name__)


lib_balistos = Library('balistos', 'static')

balistos_css = Resource(
    library=lib_balistos,
    relpath='css/style.css',
    minified='css/style.min.css',
    minifier='cssmin',
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
    bottom=True,
)

slider_js = Resource(
    library=lib_balistos,
    relpath='js/simple-slider.min.js',
    bottom=True,
)

youtube_js = Resource(
    library=lib_balistos,
    relpath='js/youtube.js',
    minified='js/youtube.min.js',
    minifier='jsmin',
    depends=[jquery, knockout_js],
)

playlist_js = Resource(
    library=lib_balistos,
    relpath='js/playlist.js',
    minified='js/playlist.min.js',
    minifier='jsmin',
    depends=[jquery, knockout_js],
    bottom=True,
)

sha_js = Resource(
    library=lib_balistos,
    relpath='js/sha256-min.js',
    bottom=True,
)

balistos_assets = Group([
    jquery,
    modernizr,
    balistos_js,
    balistos_css,
    sha_js,
    slider_js
])
youtube_assets = Group([
    knockout_js,
    youtube_js,
    playlist_js
])
