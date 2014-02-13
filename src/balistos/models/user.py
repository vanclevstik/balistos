# -*- coding: utf-8 -*-
"""User model."""

from pyramid_basemodel import Base
from pyramid_basemodel import BaseMixin
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship


class Group(Base, BaseMixin):
    """A class representing a Group."""

    __tablename__ = 'groups'

    name = Column(
        String,
        unique=True,
    )

    @classmethod
    def by_id(self, group_id):
        """Get a Group by id."""
        return Group.query.filter_by(id=group_id).first()

    @classmethod
    def by_name(self, name):
        """Get a Group by name."""
        return Group.query.filter_by(name=name).first()

    @classmethod
    def get_all(class_, order_by='name', filter_by=None, limit=1000):
        """Return all groups.

        filter_by: dict -> {'name': 'foo'}

        By default, order by Group.name.
        """
        Group = class_
        q = Group.query
        q = q.order_by(getattr(Group, order_by))
        if filter_by:
            q = q.filter_by(**filter_by)
        q = q.limit(limit)
        return q


class User(Base, BaseMixin):
    """A class representing a User."""

    __tablename__ = 'users'

    username = Column(
        String,
        unique=True,
        nullable=False,
    )

    email = Column(
        String,
        unique=True,
        nullable=True,
    )

    fullname = Column(
        Unicode(200),
        nullable=True,
    )

    password = Column(
        Unicode(120),
        nullable=True,
    )

    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship(
        Group,
        single_parent=False,
        backref=backref(
            'playlistclips',
            cascade='all, delete-orphan',
            single_parent=False,
            uselist=True,
        ),
    )

    @classmethod
    def get_by_username(self, username):
        """Get a User by username."""
        result = User.query.filter_by(username=username)
        if result.count() < 1:
            return None

        return result.one()

    @classmethod
    def get_all(class_, order_by='fullname', filter_by=None):
        """Return all users.

        filter_by: dict -> {'name': 'foo'}

        By default, order by User.fullname.
        """
        User = class_
        q = User.query
        q = q.order_by(getattr(User, order_by))
        if filter_by:
            q = q.filter_by(**filter_by)
        return q
