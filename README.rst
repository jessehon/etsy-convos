Convos
==============================

Messaging backend for Etsy

Briefing
-----------

This is a messaging system for Etsy where the user is able to send a message (convo) to another user much like the emailing system.

Etsy members use a feature called Convos to send short messages to each other, similar to email. Each convo has the following attributes:

* A sender
* A recipient
* A subject line, max 140 characters
* A body, max 64k characters
* A status to show if the convo has been read

Additionally, convos are grouped by threads, so the data model needs to show if the convo was in reply to a previous convo. (Replies also share the same subject line as previous convos in the thread.)

Wiki
----------------------

Refer to wiki for details on implementation `wiki`_

Getting up and running
----------------------

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv
* PostgreSQL

First make sure to create and activate a virtualenv_, then open a terminal at the project root and install the requirements for local development::

    $ pip install -r requirements/local.txt

Note that on OSX there will be external dependents

    brew install postgresql
    brew install libmemcached

.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Then, create a PostgreSQL database and add the database configuration using the  ``dj-database-url`` app pattern: ``postgres://db_owner:password@dbserver_ip:port/db_name`` either:

* in the ``config.settings.common.py`` setting file,
* or in the environment variable ``DATABASE_URL``

You can now run the usual Django ``migrate`` and ``runserver`` command::

    $ python manage.py migrate

    $ python manage.py runserver

You can then access the admin using your staff/superuser account::

    127.0.0.1:8000/admin/

Or access the API directly with any user account through `Messages API`_, `Threads API`_, and `Thread messages API`_::

Testing
------------

After completing above, you can start the test runner by::

    $ python manage.py test

Deployment
------------

It is possible to deploy to Heroku or to your own server by using Dokku, an open source Heroku clone.

Heroku
^^^^^^

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create --buildpack https://github.com/heroku/heroku-buildpack-python

    heroku addons:add heroku-postgresql:dev
    heroku pg:backups schedule DATABASE_URL
    heroku pg:promote DATABASE_URL

    heroku addons:add sendgrid:starter
    heroku addons:add memcachier:dev

    heroku config:set DJANGO_SECRET_KEY=RANDOM_SECRET_KEY_HERE
    heroku config:set DJANGO_SETTINGS_MODULE='config.settings.production'

    heroku config:set DJANGO_AWS_ACCESS_KEY_ID=YOUR_AWS_ID_HERE
    heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=YOUR_AWS_S3_BUCKET_NAME_HERE

    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py check --deploy
    heroku run python manage.py createsuperuser
    heroku open

LICENSE: BSD

Settings
------------

etsy_convos relies extensively on environment settings which **will not work with Apache/mod_wsgi setups**. It has been deployed successfully with both Gunicorn/Nginx and even uWSGI/Nginx.

For configuration purposes, the following table maps the 'etsy_convos' environment variables to their Django setting:

======================================= =========================== ============================================== ===========================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ===========================================
DJANGO_AWS_ACCESS_KEY_ID                AWS_ACCESS_KEY_ID           n/a                                            raises error
DJANGO_AWS_SECRET_ACCESS_KEY            AWS_SECRET_ACCESS_KEY       n/a                                            raises error
DJANGO_AWS_STORAGE_BUCKET_NAME          AWS_STORAGE_BUCKET_NAME     n/a                                            raises error
DJANGO_CACHES                           CACHES (default)            locmem                                         memcached
DJANGO_DATABASES                        DATABASES (default)         See code                                       See code
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
======================================= =========================== ============================================== ===========================================

* TODO: Add vendor-added settings in another table

.. _wiki: https://github.com/jessehon/etsy-convos/wiki/Home
.. _Messages API: https://github.com/jessehon/etsy-convos/wiki/Messages-API
.. _Thread messages API: https://github.com/jessehon/etsy-convos/wiki/Thread-Messages-API
.. _Threads API: https://github.com/jessehon/etsy-convos/wiki/Threads-API
