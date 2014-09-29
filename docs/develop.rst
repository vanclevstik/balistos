Local development
=================

Prerequisites
-------------

* GCC, make, and similar (``apt-get install build-essential``)
* PostgreSQL development headers (``apt-get install libpq-dev``)
* Python 2.7 with development headers (``apt-get install python-dev``)
* virtualenv (``apt-get install python-virtualenv``)
* pip (``apt-get install python-pip``)
* git (``apt-get install git``)
* Redis (``apt-get install redis-server``)or RabbitMQ server for celery broker
* Heroku Toolbelt (https://toolbelt.heroku.com/)

Code style guide
----------------

We follow `plone.api's style guide
<http://ploneapi.readthedocs.org/en/latest/contribute/conventions.html>`_. Read
it & use it.


Setting up a local development environment
------------------------------------------

Prepare the environment::

    # fetch latest code
    $ git clone https://github.com/ferewuz/balistos.git
    $ cd balistos

    # build development environment
    $ make

    # Set environment variable to .ini you want to use
    $ export BALISTOS_CONFIG=etc/development.ini  # you can use different .ini if you want

    # Set correct broker url in celeryconfig.py

Now you can run a variety of commands::

    # if your DB is empty, populate it with demo content
    $ make db

    # Run redis server
    $ redis-server

    # Start the celery workers
    $ bin/celery -A balistos.tasks worker -loglevel=debug
    $ bin/celery -A balistos.tasks beat --loglevel=debug

    # Start the development instance of Pyramid
    $ bin/pserve etc/development.ini --reload

    # development commands
    $ make docs  # generate HTML format of docs for local viewing
    $ make tests  # run all tests
    $ make coverage  # generate HTML report of test coverage
    $ make clean  # clean up if something is broken and start from scratch


Running migration script
------------------------

For database migration we are using alembic scripts

Add a new alembic upgrade script::

    $ bin/alembic -c etc/development.ini -n app:main revision --autogenerate -m "YOUR REVISION INFO"

Run the script::

    $ bin/alembic -c etc/development.ini -n app:main upgrade head
