# -*- coding: utf-8 -*-
"""Clip model."""

from balistos.models.playlist import Playlist
from balistos.models.playlist import PlaylistUser
from balistos.models.user import User
from pyramid_basemodel import Base
from pyramid_basemodel import BaseMixin
from pyramid_basemodel import Session
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship


class Clip(Base, BaseMixin):
    """A class representing a Youtube Clip."""

    __tablename__ = 'clips'

    title = Column(
        Unicode,
    )

    image_url = Column(
        String,
        nullable=True
    )

    likes = Column(
        Integer,
        nullable=True,
    )

    youtube_video_id = Column(
        String,
        nullable=False,
        unique=True,
    )

    # Duration in seconds
    duration = Column(
        Integer,
        nullable=False
    )

    @classmethod
    def get(self, youtube_video_id):
        """Get a Clip by youtube_id."""
        result = Clip.query.filter_by(youtube_video_id=youtube_video_id)
        if result.count() < 1:
            return None

        return result.one()

    @classmethod
    def get_all(class_, order_by='likes', filter_by=None):
        """Return all Clips.

        filter_by: dict -> {'name': 'foo'}

        By default, order by Clip.likes.
        """
        Clip = class_
        q = Clip.query
        q = q.order_by(getattr(Clip, order_by))
        if filter_by:
            q = q.filter_by(**filter_by)
        return q


class PlaylistClip(Base, BaseMixin):
    """A class representing a Playlist clip."""

    __tablename__ = 'playlist_clips'

    def __init__(
        self,
        likes=0,
        added=False,
        state=None,
        clip=None,
        playlist=None,
        started=None,
        username=None,
    ):
        Base.__init__(
            self,
            likes=likes,
            added=added,
            state=state,
            clip=clip,
            playlist=playlist,
            started=started,
        )
        BaseMixin.__init__(self)
        for p_user in PlaylistUser.get_by_playlist(playlist):
            owner = p_user.user.username == username
            Session.add(PlaylistClipUser(
                liked=0,
                user=p_user.user,
                playlist_clip=self,
                owner=owner
            ))

    likes = Column(
        Integer,
        unique=False,
        nullable=False,
        default=0,
    )

    added = Column(
        DateTime,
        nullable=False
    )

    # -1 - inactive
    # 0 - in queue
    # 1 - next
    # 2 - playing
    state = Column(
        Integer,
        nullable=False
    )

    started = Column(
        DateTime,
        nullable=True,
    )

    clip_id = Column(Integer, ForeignKey('clips.id'))
    clip = relationship(
        Clip,
        single_parent=False,
        backref=backref(
            'playlistclips',
            cascade='all, delete-orphan',
            single_parent=False,
            uselist=True,
        ),
    )

    playlist_id = Column(Integer, ForeignKey('playlists.id'))
    playlist = relationship(
        Playlist,
        single_parent=False,
        backref=backref(
            'playlistclips',
            cascade='all, delete-orphan',
            single_parent=False,
            uselist=True,
        ),
    )

    @classmethod
    def get_all(class_, order_by='likes', filter_by=None):
        """Return all PlaylistClips.

        filter_by: dict -> {'name': 'foo'}

        By default, order by PlaylistClip.likes.
        """
        PlaylistClip = class_
        q = PlaylistClip.query
        q = q.order_by(getattr(PlaylistClip, order_by))
        if filter_by:
            q = q.filter_by(**filter_by)
        return q

    @classmethod
    def get_by_playlist(self, playlist):
        """Get all PlaylistClip by Playlist id."""
        result = PlaylistClip.query.filter_by(playlist=playlist)

        if result.count() < 1:
            return []

        return result.all()

    @classmethod
    def get_by_playlist_and_clip(self, playlist, clip):
        """Get all PlaylistClip by Playlist and Clip."""
        result = PlaylistClip.query.filter(
            PlaylistClip.playlist == playlist,
            PlaylistClip.clip == clip,
        )
        if result.count() < 1:
            return None

        return result.one()

    @classmethod
    def get_active_playlist_clip(self, playlist):
        """Get playlist clip that is currently active"""
        result = PlaylistClip.query.filter(
            PlaylistClip.playlist == playlist,
            PlaylistClip.state == 2,
        )
        if result.count() < 1:
            return None
        return result.one()

    @classmethod
    def get_queue_playlist_clip(self, playlist):
        """Get playlist clip that is currently next in queue"""
        result = PlaylistClip.query.filter(
            PlaylistClip.playlist == playlist,
            PlaylistClip.state == 1,
        )
        if result.count() < 1:
            return None
        return result.one()

    @classmethod
    def get_by_playlist_waiting(self, playlist):
        """Get all PlaylistClip that are not active or next in queue."""
        result = PlaylistClip.query.filter(
            PlaylistClip.playlist == playlist,
            PlaylistClip.state == 0,
        ).order_by(
            PlaylistClip.likes.desc(),
            PlaylistClip.added.asc()
        )
        if result.count() < 1:
            return None

        return result.all()


class PlaylistClipUser(Base, BaseMixin):

    __tablename__ = 'playlist_clips_users'

    # options are
    # 0 - neutral
    # 1 - liked
    # -1 - disliked
    liked = Column(
        Integer,
        nullable=False,
        default=0,
    )

    owner = Column(
        Boolean,
        nullable=False,
        default=False
    )

    playlist_clip_id = Column(Integer, ForeignKey('playlist_clips.id'))
    playlist_clip = relationship(
        PlaylistClip,
        single_parent=False,
        backref=backref(
            'playlist_clips_users',
            cascade='all, delete-orphan',
            single_parent=False,
            uselist=True,
        )
    )

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        User,
        single_parent=False,
        backref=backref(
            'playlist_clips_users',
            cascade='all, delete-orphan',
            single_parent=False,
            uselist=True,
        )
    )

    @classmethod
    def get_by_playlist_clip_and_user(self, playlist_clip, user):
        """Get PlaylistClipUser by PlaylistClip and User."""
        result = PlaylistClipUser.query.filter(
            PlaylistClipUser.playlist_clip == playlist_clip,
            PlaylistClipUser.user == user
        )
        if result.count() < 1:
            return None

        return result.one()

    @classmethod
    def get_playlist_clip_owner(self, playlist_clip):
        """Get  owner"""
        result = PlaylistClipUser.query.filter(
            PlaylistClipUser.playlist_clip == playlist_clip,
            PlaylistClipUser.owner == True  # noqa
        )
        if result.count() < 1:
            return None

        return result.one().user
