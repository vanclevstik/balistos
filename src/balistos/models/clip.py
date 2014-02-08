# -*- coding: utf-8 -*-
"""Clip model."""

from pyramid_basemodel import Base
from pyramid_basemodel import BaseMixin
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship


class Clip(Base, BaseMixin):
    """A class representing a User."""

    __tablename__ = 'clips'

    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
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
    def get(self, youtube_id):
        """Get a Clip by youtube_id."""
        result = Clip.filter_by(youtube_id=youtube_id)
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
            q = q.filter(filter_by)
        return q


class PlaylistClip(Base, BaseMixin):
    """A class representing a Playlist clip."""

    __tablename__ = 'playlist_clips'

    id = Column(
        Integer,
        primary_key=True,
        nullable=False)

    likes = Column(
        Integer,
        unique=False,
        nullable=False
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
        single_parent=True,
        backref=backref(
            'clip',
            cascade='all, delete-orphan',
            single_parent=False,
            uselist=False,
        ),
    )

    @classmethod
    def get(self, uri):
        """Get a PlaylistClip by uri."""
        result = PlaylistClip.filter_by(uri=uri)
        if result.count() < 1:
            return None

        return result.one()

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
            q = q.filter(filter_by)
        return q
