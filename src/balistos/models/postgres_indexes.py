# -*- coding: utf-8 -*-
"""Indexes that we are using for postgresql and not sqlite."""
from sqlalchemy import Index
from balistos.models.clip import PlaylistClip


Index(
    'playlist_clip_index_active',
    PlaylistClip.playlist_id,
    postgresql_where=PlaylistClip.state == 2,
    unique=True,
)


Index(
    'playlist_clip_index_next',
    PlaylistClip.playlist_id,
    postgresql_where=PlaylistClip.state == 1,
    unique=True,
)
