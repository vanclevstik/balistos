# -*- coding: utf-8 -*-
"""Installer for the balistos package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = \
    read('README.rst') + \
    read('docs', 'CHANGELOG.rst') + \
    read('docs', 'LICENSE.rst')

setup(
    name='balistos',
    version='0.1',
    description="""Web application that lets users edit and play shared
        Youtube playlists""",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Vanč Levstik',
    author_email='vanc.levstik@gmail.com',
    keywords='pyramid playlist shared youtube',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    paster_plugins=['pyramid'],
    install_requires=[
        'fanstatic',
        'gdata',
        'isodate',
        'js.bootstrap',
        'js.deform',
        'js.jquery',
        'passlib',
        'psycopg2',
        'pyramid',
        'pyramid_basemodel',
        'pyramid_debugtoolbar',
        'pyramid_deform',
        'pyramid_fanstatic',
        'pyramid_layout',
        'pyramid_tm',
        'SQLAlchemy',
        'transaction',
        'unidecode',
        'zope.sqlalchemy',
    ],
    extras_require={
        'test': [
            'coverage',
            'fanstatic [cssmin,jsmin]',
            'flake8',
            'nose',
            'nose-selecttests',
            'Sphinx',
            'unittest2',
            'webtest',
        ],
        'development': [
            'pyramid_debugtoolbar',
            'Sphinx',
            'waitress',
        ],
    },
    entry_points="""\
    [paste.app_factory]
    main = balistos:main

    # Fanstatic resource library
    [fanstatic.libraries]
    balistos = balistos.static:lib_balistos

    """,
)
