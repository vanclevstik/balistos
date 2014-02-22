# -*- coding: utf-8 -*-

from pyramid.view import view_config
from pyramid.response import Response
from balistos.models.user import User
from balistos.models.clip import PlaylistClip
from balistos.models.clip import PlaylistClipUser
from pyramid_basemodel import Session
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from passlib.hash import sha256_crypt
from pyramid.security import remember
from pyramid.security import forget

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
