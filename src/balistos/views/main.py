# -*- coding: utf-8 -*-
"""Main views on front page"""

from balistos.static import balistos_assets
from balistos.static import youtube_assets
from datetime import datetime
from pyramid.view import view_config
from pyramid.response import Response
from balistos.models.playlist import Playlist
from balistos.models.clip import PlaylistClip
from balistos.models.clip import Clip
from pyramid_basemodel import Session
from pyramid.httpexceptions import HTTPNotFound

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
    session = request.session
    if not 'playlist' in session or not session['playlist']:
        session['playlist'] = str(Playlist.get_all()[0].uri)
    return {}


@view_config(
    route_name='playlist_videos',
)
def playlist_videos(request):
    """
    View that returns videos of our playlist in json format

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: json listing all videos as http response
    :rtype:   pyramid.response.Response
    """
    if not request.is_xhr:
        return HTTPNotFound()
    playlist = Playlist.get(request.session['playlist'])
    pclips = get_playlist_videos(playlist)
    return Response(body=json.dumps(pclips), content_type='application/json')


@view_config(
    route_name='set_playlist',
    renderer='balistos:templates/main.pt',
    layout='default',
)
def set_playlist(request):
    """
    View that sets playlist in our session

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: nothing, just renders template
    :rtype:   empty dict
    """

    balistos_assets.need()
    youtube_assets.need()
    session = request.session
    session['playlist'] = request.matchdict.get('playlist')
    return {}


@view_config(
    route_name='playlist_add_video',
)
def playlist_add_video(request):
    """
    View that adds video to playlist currently in session and returns
    changed playlist videos list

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: dict for each clip that is part of playlist
    :rtype:   list of dicts
    """
    if not request.is_xhr:
        return HTTPNotFound()
    title = request.GET['title']
    image_url = request.GET['image']
    youtube_video_id = request.GET['id']
    duration = time_from_iso_format(request.GET['duration'])
    playlist = Playlist.get(request.session['playlist'])
    clip = Clip.get(youtube_video_id)
    if not clip:
        clip = Clip(
            title=title,
            image_url=image_url,
            youtube_video_id=youtube_video_id,
            likes=0,
            duration=duration,
        )
        Session.add(clip)
        Session.flush()
    pclip = PlaylistClip.get_by_playlist_and_clip(playlist, clip)
    if not pclip:
        pclip = PlaylistClip(
            added=datetime.now(),
            likes=0,
            state=0,
            clip=clip,
            playlist=playlist,
        )
        Session.add(pclip)
        Session.flush()
    else:
        pclip.likes += 1
    pclips = get_playlist_videos(playlist)
    return Response(body=json.dumps(pclips), content_type='application/json')


def get_playlist_videos(playlist):
    """
    Method that returns all the clips that are part of playlist

    :param    playlist: playlist of which we want to get videos
    :type     playlist: balistos.models.playlist.Playlist

    :returns: dict for each clip that is part of playlist
    :rtype:   list of dicts
    """
    result = []
    pclips = []
    if check_if_finished(PlaylistClip.get_active_playlist_clip(playlist)):
        next_pclip = PlaylistClip.get_queue_playlist_clip(playlist)
        if next_pclip:
            next_pclip.state = 2
            next_pclip.started = datetime.now()
            set_next_in_queue(playlist)
            Session.flush()

    pclips.append(PlaylistClip.get_active_playlist_clip(playlist))
    next_pclip = PlaylistClip.get_queue_playlist_clip(playlist)
    if next_pclip:
        pclips.append(next_pclip)
    else:
        set_next_in_queue(playlist)
    wait_clips = PlaylistClip.get_by_playlist_waiting(playlist)
    if wait_clips:
        pclips = pclips + wait_clips
    for pclip in pclips:
        clip = pclip.clip
        if pclip.state == 2:
            start_time = (datetime.now() - pclip.started).total_seconds()
        else:
            start_time = 0
        result.append(
            {
                'id': clip.youtube_video_id,
                'title': clip.title,
                'likes': pclip.likes,
                'image': clip.image_url,
                'start_time': start_time
            },
        )
    return result


def check_if_finished(pclip):
    """
    Check if currently active clip finished playing and remove it from playing,
    state if it is.

    :param    pclip: active playlist clip
    :type     pclip: balistos.models.playlist.PlaylistClip

    :returns: True if clip is finished and we removed it, False otherwise
    :rtype:   boolean
    """
    duration = pclip.clip.duration
    started = pclip.started
    if (datetime.now()-started).total_seconds() > duration:
        Session.delete(pclip)
        Session.flush()
        return True
    return False


def set_next_in_queue(playlist):
    """
    Set next video in queue based on likes, time added

    :param    playlist: playlist for which next clip we are setting
    :type     playlist: balistos.models.playlist.Playlist
    """
    pclips = PlaylistClip.get_by_playlist_waiting(playlist)
    if pclips:
        pclips[0].state = 1
        Session.flush()


def time_from_iso_format(date):
    """
    Converts iso format to datetime object

    :param    date: 'PT#M#S' formatted date
    :type     date: str

    :returns: converted date
    :rtype:   datetime.timedelta
    """

    date = date.split('PT')[1].split('M')
    if len(date) > 1:
        minutes = date[0]
        seconds = date[1].split('S')[0]
        return int(minutes)*60 + int(seconds)
    else:
        return int(date[0].split('S')[0])
