# -*- coding: utf-8 -*-
"""Playlist model."""

from balistos.models.user import User
from pyramid_basemodel import Base
from pyramid_basemodel import BaseMixin
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship


class Playlist(Base, BaseMixin):
    """A class representing a Playlist."""

    __tablename__ = 'playlists'

    uri = Column(
        String,
        unique=True,
        nullable=False
    )

    title = Column(
        Unicode(200),
        nullable=False
    )

    @classmethod
    def get(self, uri):
        """Get a Playlist by uri."""
        result = Playlist.query.filter_by(uri=uri)
        if result.count() < 1:
            return None

        return result.one()

    @classmethod
    def get_all(class_, order_by='title', filter_by=None):
        """Return all Playlists.

        filter_by: dict -> {'name': 'foo'}

        By default, order by Playlist.title.
        """
        Playlist = class_
        q = Playlist.query
        q = q.order_by(getattr(Playlist, order_by))
        if filter_by:
            q = q.filter_by(**filter_by)
        return q


class PlaylistUser(Base, BaseMixin):

    __tablename__ = 'playlist_user'

    # permission on playlist
    # 0 - no permission
    # 1 - view and play playlist
    # 2 - vote, chat on playlist
    # 3 - admin rights on playlist
    permission = Column(
        Integer,
        nullable=False
    )

    playlist_id = Column(Integer, ForeignKey('playlists.id'))
    playlist = relationship(
        Playlist,
        single_parent=True,
        backref=backref(
            'playlist_user',
            cascade='all, delete-orphan',
            single_parent=False,
            uselist=True,
        )
    )

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        User,
        single_parent=True,
        backref=backref(
            'playlist_user',
            cascade='all, delete-orphan',
            single_parent=False,
            uselist=True,
        )
    )
