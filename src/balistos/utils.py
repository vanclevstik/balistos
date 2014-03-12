# -*- coding: utf-8 -*-
"""Utils for balistos product"""
from pyramid.security import authenticated_userid
from balistos.models.user import User


import re
import unidecode


def normalized_id(title):
    title = unidecode.unidecode(title).lower()
    return re.sub('\W+', '-', title.replace("'", '')).strip('-')


def get_user(request):
    username = authenticated_userid(request)
    if username:
        user = User.get_by_username(username)
    else:
        user = None
    return user
