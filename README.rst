====================
balistos Pyramid App
====================

A Heroku-deployable Pyramid app that lets users edit and play shared Youtube playlists

* `Source code @ GitHub <https://github.com/ferewuz/balistos>`_
* `Dev Docs @ GitHub <https://github.com/ferewuz/balistos/blob/master/docs/develop.rst>`_
* `Test Coverage @ Coveralls <https://coveralls.io/r/ferewuz/balistos>`_
* `Continuous Integration @ Travis-CI <https://travis-ci.org/ferewuz/balistos/builds>`_
* `Deployed @ Heroku <http://balistos.herokuapp.com>`_

.. image:: https://travis-ci.org/ferewuz/balistos.png?branch=master
  :target: https://travis-ci.org/ferewuz/balistos

.. image:: https://coveralls.io/repos/ferewuz/balistos/badge.png?branch=master
  :target: https://coveralls.io/r/ferewuz/balistos?branch=master




How it works
============

Balistos is automatically deployable
to Heroku (via GitHub and Travis CI).

Local development
=================

Run Makefile:
  `make`

Start app with:
  `bin/pserve etc/development.ini`

Run tests with:
  `make tests`
