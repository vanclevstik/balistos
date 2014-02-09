# -*- coding: utf-8 -*-
"""Main views on front page"""

from balistos.static import balistos_assets
from balistos.static import youtube_assets
from pyramid.view import view_config
from pyramid.response import Response
from balistos.models.clip import PlaylistClip
from pyramid.httpexceptions import HTTPFound

import json


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
    youtube_assets.need()
    return {}


@view_config(
    route_name='playlist_video',
)
def playlist_video(request):
    pclip = PlaylistClip.get_all()[0]
    clip = pclip.clip
    return Response(
        body=json.dumps(
            [{
                'id': clip.youtube_video_id,
                'title': clip.title,
                'likes': pclip.likes,
                'image': clip.image_url
            }, ]
        ),
        content_type='application/json')


@view_config(
    route_name='set_playlist',
)
def set_playlist(request):
    session = request.session
    session['playlist'] = request.matchdict.get('playlist')
    url = request.route_url('main')
    return HTTPFound(location=url)
