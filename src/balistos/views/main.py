# -*- coding: utf-8 -*-
"""Main views on front page"""

from balistos.models.clip import Clip
from balistos.models.clip import PlaylistClip
from balistos.models.clip import PlaylistClipUser
from balistos.models.user import User
from balistos.models.playlist import Playlist
from balistos.models.playlist import PlaylistUser
from balistos.playlist import add_playlist_clip
from balistos.playlist import add_chat_message
from balistos.playlist import get_playlist_videos
from balistos.playlist import remove_playlist_clip
from balistos.playlist import get_playlist_settings
from balistos.playlist import get_active_users
from balistos.playlist import get_chat_messages
from balistos.playlist import create_clips_for_user
from balistos.static import balistos_assets
from balistos.static import youtube_assets
from balistos.utils import normalized_id
from datetime import datetime
from pyramid_basemodel import Session
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.security import authenticated_userid
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import json
import isodate


@view_config(
    route_name='home',
    renderer='balistos:templates/home.pt',
    layout='default',
)
def home(request):
    """The home page."""
    balistos_assets.need()
    username = authenticated_userid(request)
    return {
        'username': username
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
    username = authenticated_userid(request)
    if not username or not 'playlist' in session or not session['playlist']:
        url = request.route_url('home')
        return HTTPFound(location=url)
    return {
        'username': username
    }


@view_config(route_name='playlist_videos')
def playlist_videos(request):
    """
    View that returns videos of our playlist in json format

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: json listing all videos as http response
    :rtype:   pyramid.response.Response
    """
    if not request.is_xhr or not 'playlist' in request.session:
        return HTTPNotFound()
    playlist = Playlist.get(request.session['playlist'])
    username = authenticated_userid(request)
    pclips = get_playlist_videos(playlist, username=username)
    playlist_settings = get_playlist_settings(playlist, username=username)
    chat_messages = get_chat_messages(playlist)
    active_users = get_active_users(playlist)
    return Response(
        body=json.dumps({
            'settings': playlist_settings,
            'users': active_users,
            'messages': chat_messages,
            'videos': pclips
        }),
        content_type='application/json'
    )


@view_config(
    route_name='set_playlist',
    renderer='balistos:templates/main.pt',
    permission='user',
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
    username = authenticated_userid(request)
    if not username:
        return HTTPNotFound()
    session = request.session
    playlist_uri = request.matchdict.get('playlist', None)
    playlist = Playlist.get(playlist_uri)
    user = User.get_by_username(username)
    if not playlist or not user:
        return HTTPNotFound()

    playlist_user = PlaylistUser.get_by_playlist_and_user(playlist, user)
    if not playlist_user and not playlist.public:
        url = request.route_url('home')
        return HTTPFound(location=url)
    if not playlist_user:
        playlist_user = PlaylistUser(
            playlist=playlist,
            user=user,
            permission=2,
            last_active=datetime.now(),
        )
        Session.add(playlist_user)
        create_clips_for_user(playlist_user)

    session['playlist'] = playlist_uri
    return {
        'username': username
    }


@view_config(route_name='playlist_add_video')
def playlist_add_video(request):
    """
    View that adds video to playlist currently in session and returns
    changed playlist videos list

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: dict for each clip that is part of playlist
    :rtype:   list of dicts
    """
    username = authenticated_userid(request)
    if not request.is_xhr or not username:
        return HTTPNotFound()
    title = unicode(request.GET['title'])
    image_url = request.GET['image']
    youtube_video_id = request.GET['id']
    duration = isodate.parse_duration(request.GET['duration']).total_seconds()
    playlist = Playlist.get(request.session['playlist'])
    state = 0
    if not PlaylistClip.get_active_playlist_clip(playlist):
        state = 2
    add_playlist_clip(
        playlist,
        title,
        image_url,
        youtube_video_id,
        duration,
        username=username,
        state=state,
    )
    return Response()


@view_config(route_name='like_video')
def like_video(request):
    """
    Like/unlike a selected video but only if user is logged in
    and didn't like/unlike it yet

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: empty response
    :rtype:   pyramid.response.Response
    """
    if not request.is_xhr:
        return HTTPNotFound()
    user = User.get_by_username(authenticated_userid(request))
    if not user:
        return Response()
    like = int(request.GET['like'])
    youtube_video_id = request.GET['video_id']
    playlist = Playlist.get(request.session['playlist'])
    pclip = PlaylistClip.get_by_playlist_and_clip(
        playlist,
        Clip.get(youtube_video_id)
    )
    pclip_user = PlaylistClipUser.get_by_playlist_clip_and_user(pclip, user)
    if pclip_user.liked == like:
        pclip.likes += like * (-1)
        pclip_user.liked = 0
    elif pclip_user.liked == 0:
        pclip.likes += like
        pclip_user.liked = like
    elif pclip_user.liked != 0:
        pclip.likes += 2*like
        pclip_user.liked = like
    return Response()


@view_config(route_name='remove_video')
def remove_video(request):
    """
    Remove video from playlist if you have correct rights

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: success if video was remove correctly, error otherwise
    :rtype:   pyramid.response.Response
    """
    if not request.is_xhr:
        return HTTPNotFound()
    username = authenticated_userid(request)
    youtube_video_id = request.GET['video_id']
    playlist = Playlist.get(request.session['playlist'])
    if not username or not youtube_video_id:
        return Response(
            body=json.dumps({'error': ''}),
            content_type='application/json'
        )

    if not remove_playlist_clip(playlist, youtube_video_id):
        return Response(
            body=json.dumps({'error': ''}),
            content_type='application/json'
        )

    return Response(
        body=json.dumps({'success': 'Succesfully removed'}),
        content_type='application/json'
    )


@view_config(route_name='chat_message')
def chat_message(request):
    """
    Add chat message to playlist chat

    :param    request: current request
    :type     request: pyramid.request.Request
    :returns: success if video was remove correctly, error otherwise
    :rtype:   pyramid.response.Response
    """
    if not request.is_xhr:
        return HTTPNotFound()
    username = authenticated_userid(request)
    if not username:
        return Response()
    message = request.POST['message']
    playlist = Playlist.get(request.session['playlist'])
    add_chat_message(playlist, username, message)
    return Response()


@view_config(
    route_name='create_playlist',
    permission='user',
)
def create_playlist(request):
    """
    Add new playlist
    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: success if playlist was added correctly, error otherwise
    :rtype:   pyramid.response.Response
    """
    username = authenticated_userid(request)
    user = User.get_by_username(username)
    title = request.POST.get('title', None)
    if not title or not user:
        return HTTPNotFound()
    duration_limit = int(request.GET.get('duration_limit', 600))
    public = request.GET.get('public', True)
    uri = normalized_id(title)
    count = 1
    while Playlist.get(uri):
        uri = uri + str(count)
        count += 1
    playlist = Playlist(
        uri=uri,
        title=title,
        duration_limit=duration_limit,
        public=public,
    )
    Session.add(playlist)
    playlist_user = PlaylistUser(
        playlist=playlist,
        user=user,
        permission=3,
        last_active=datetime.now(),
    )
    Session.add(playlist_user)
    create_clips_for_user(playlist_user)
    url = request.route_url('set_playlist', playlist=uri)
    return HTTPFound(location=url)


@view_config(
    route_name='search_playlists'
)
def search_playlists(request):
    """
    Search and return playlists with similar name

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: playlists that search returned
    :rtype:   list of dicts
    """
    if not request.is_xhr:
        return HTTPNotFound()
    # username = authenticated_userid(request)
    # user = User.get_by_username(username)
    query = request.GET['query']
    playlists = []
    for playlist in Playlist.search_title(query):
        playlists.append({
            'uri': playlist.uri,
            'title': playlist.title
        })

    return Response(
        body=json.dumps(playlists),
        content_type='application/json'
    )


@view_config(
    route_name='add_user_to_playlist'
)
def add_user_to_playlist(request):
    """
    Adds user as member of playlist

    :param    request: current request
    :type     request: pyramid.request.Request
    """
    if not request.is_xhr:
        return HTTPNotFound()
    username = request.GET['username']
    playlist = request.GET['playlist']
    user = User.get_by_username(username)
    playlist_user = PlaylistUser(
        playlist=playlist,
        user=user,
        permission=2,
        last_active=datetime.now(),
    )
    Session.add(playlist_user)
    create_clips_for_user(playlist_user)
    return Response(
        body=json.dumps({'success': 'Succesfully added user'}),
        content_type='application/json'
    )
