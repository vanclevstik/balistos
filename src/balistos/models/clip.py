# -*- coding: utf-8 -*-
"""Clip model."""

from balistos.models.playlist import Playlist
from pyramid_basemodel import Base
from pyramid_basemodel import BaseMixin
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

    active = Column(
        Boolean,
        nullable=False
    )

    clip_id = Column(Integer, ForeignKey('clips.id'))
    clip = relationship(
        Clip,
        single_parent=False,
        backref=backref(
            'playlistclip',
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
            'playlistclip',
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
            return None

        return result.all()

    @classmethod
    def get_by_playlist_and_clip(self, playlist, clip):
        """Get all PlaylistClip by Playlist and Clip."""
        result = PlaylistClip.query.filter_by(
            playlist=playlist).filter_by(clip=clip)
        if result.count() < 1:
            return None

        return result.one()
