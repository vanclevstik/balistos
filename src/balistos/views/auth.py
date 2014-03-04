# -*- coding: utf-8 -*-
"""Views for user authentication"""
from balistos.models.user import User
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
        return Response(
            body=json.dumps(msg),
            content_type='application/json',
            headers=headers,
        )
    else:
        msg = {'error': 'Your username and password are not valid.'}
        return Response(
            body=json.dumps(msg),
            content_type='application/json',
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
    email = request.POST['register-email']
    if User.get_by_username(username):
        msg = {'error': 'User with that username already exist'}
        return Response(body=json.dumps(msg), content_type='application/json')
    if User.get_by_email(email):
        msg = {'error': 'User with that email already exist'}
        return Response(body=json.dumps(msg), content_type='application/json')
    password = sha256_crypt.encrypt(request.POST['register-password'])

    try:
        user = User(
            username=username,
            password=password,
            email=email,
        )
        Session.add(user)
        Session.flush()
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

    :returns: redirects to home page
    :rtype:   pyramid.httpexceptions.HTTPFound
    """
    headers = forget(request)
    url = request.route_url('home')
    return HTTPFound(location=url, headers=headers)
