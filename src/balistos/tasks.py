# -*- coding: utf-8 -*-
"""Celery tasks"""

from balistos.models.playlist import Playlist
from balistos.models.clip import PlaylistClip
from balistos.playlist import check_if_finished
from balistos.playlist import set_next_in_queue
from balistos.playlist import play_next_clip
from sqlalchemy.exc import IntegrityError

from celery import Celery
from celery.signals import worker_init
from celery import group
import transaction
from multiprocessing.util import register_after_fork
from sqlalchemy import engine_from_config
from pyramid_basemodel import Session


@worker_init.connect
def bootstrap_pyramid(signal, sender):
    import os
    from pyramid.paster import bootstrap
    sender.app.settings = \
        bootstrap(os.environ['BALISTOS_CONFIG'])['registry'].settings
    engine = engine_from_config(sender.app.settings, 'sqlalchemy.')

    register_after_fork(engine, engine.dispose)

    Session.configure(bind=engine)
celery = Celery()
celery.config_from_object('balistos.celeryconfig')

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@celery.task(ignore_result=True)
def check_playlists():

    playlists = Playlist.get_active_playlists()
    if not playlists:
        return
    job = group([check_playlist.s(playlist.uri) for playlist in playlists])
    job.apply_async()


@celery.task(ignore_result=True)
def check_playlist(playlist_uri):
    transaction.begin()
    playlist = Playlist.get(playlist_uri)
    active_pclip = PlaylistClip.get_active_playlist_clip(playlist)

    if not active_pclip:
        return []
    next_pclip = PlaylistClip.get_queue_playlist_clip(playlist)
    if not next_pclip:
        next_pclip = set_next_in_queue(
            playlist,
            active_pclip.clip.youtube_video_id
        )
    if check_if_finished(active_pclip):
        try:
            a, b = play_next_clip(playlist, active_pclip, next_pclip)
            active_pclip, next_pclip = a, b
        except IntegrityError:
            transaction.abort()
    transaction.commit()
