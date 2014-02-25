# -*- coding: utf-8 -*-

from balistos.models.clip import PlaylistClip
from balistos.models.clip import PlaylistClipUser
from balistos.models.playlist import Playlist
from balistos.models.playlist import PlaylistUser
from balistos.models.user import User
from datetime import datetime
from passlib.hash import sha256_crypt
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.security import forget
from pyramid.security import remember
from pyramid.view import view_config
from pyramid_basemodel import Session

import json


@view_config(
    route_name='login',
)
def login(request):
    """
    View that logs user in

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: json with message about login
    :rtype:   pyramid.response.Response
    """
    if not request.is_xhr:
        return HTTPNotFound()
    username = request.POST['login-username']
    password = request.POST['login-password']
    user = User.get_by_username(username)
    if user and sha256_crypt.verify(password, user.password):
        headers = remember(request, username)
        msg = {'success': username}
        Response(body=json.dumps(msg), content_type='application/json')
    else:
        msg = {'error': 'Your username and password are not valid.'}
        return Response(
            body=json.dumps(msg),
            content_type='application/json',
            headers=headers
        )


@view_config(
    route_name='register',
)
def register(request):
    """
    View that registers user

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: json with message about login
    :rtype:   pyramid.response.Response
    """
    if not request.is_xhr:
        return HTTPNotFound()
    username = request.POST['register-username']
    if User.get_by_username(username):
        msg = {'error': 'User with that username already exist'}
        return Response(body=json.dumps(msg), content_type='application/json')
    password = sha256_crypt.encrypt(request.POST['register-password'])
    email = request.POST['register-email']
    try:
        user = User(
            username=username,
            password=password,
            email=email,
        )
        Session.add(user)
        Session.flush()
        #XXX need to only make clips for public playlists
        for playlist in Playlist.get_all():
            playlist_user = PlaylistUser(
                playlist=playlist,
                user=user,
                permission=2,
                last_active=datetime.min,
            )
            Session.add(playlist_user)
        for pclip in PlaylistClip.get_all():
            pclipuser = PlaylistClipUser(
                playlist_clip=pclip,
                user=user
            )
            Session.add(pclipuser)
        msg = {'success': username}
        headers = remember(request, username)
        return Response(
            body=json.dumps(msg),
            content_type='application/json',
            headers=headers
        )

    except Exception:
        msg = {'error': ''}
        return Response(body=json.dumps(msg), content_type='application/json')


@view_config(
    route_name='logout',
)
def logout(request):
    """
    View that logs user out

    :param    request: current request
    :type     request: pyramid.request.Request

    :returns: json with message about login
    :rtype:   pyramid.response.Response
    """
    headers = forget(request)
    url = request.route_url('home')
    return HTTPFound(location=url, headers=headers)
