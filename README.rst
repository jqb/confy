confy
=====

Pragmatic & flexible configuration loader that makes your app settings clean and sexy.

ver. 0.3.1 beta

.. image:: https://badge.fury.io/py/confy.png
   :target: https://badge.fury.io/py/confy

.. image:: https://api.travis-ci.org/jqb/confy.png?branch=master
   :target: https://travis-ci.org/jqb/confy

.. image:: https://coveralls.io/repos/jqb/confy/badge.png?branch=master
   :target: https://coveralls.io/r/jqb/confy?branch=master



Supported platforms
-------------------

* Python 2.6
* Python 2.7
* Python 3.2
* Python 3.3


Idea
----

Idea is simple and has been developed by (probably not only) django community, but has
been never standardized. Here it is:


1) keep your configuration in separate python modules inside your
   settings/conf/config/<however-you-call-it> *module* like this::

       settings/
         |-- __init__.py     => you want a *module* - believe me
         |-- default.py      => or base.py or common.py or <whatever>.py - this should be common stuff
         |-- development.py  => change/add all you need to run the app in development mode
         |-- production.py   => change/add all you need to run the app in production mode
         `-- local.py        => everything that depends on your machine you currently working on
                                for your own (and everybody in a team) safety - remove it from version control


2) load those files in the order you want to get the configuration. Use environment
   variables to decide which settings should be loaded.
   In order to do that put following snippet inside settings/__init__.py file::

        import confy

        with confy.loader(__file__) as confy:
            confy.module(__name__, [
                confy.from_modules('base', confy.env('CONFIGURATION_MODE', 'development')),
                confy.from_modules('local', silent=True),
            ])


3) so in the end of the day you can simply import it easily and everythink is setup
   for you

        >>> import settings
        >>> # DONE!
        >>>
        >>> settings.DB_USER  # etc...


This is the basic stuff but "confy" has a lot more to offer.


Why
---

1) I believe in clean and elegant solutions.


2) I have really bad experience with *.ini and "configparser"-like parsers (eg from pylons/pyramid).
   There are few issues with them::

     => Each setting has a type. And you have to write code that changes text into other types.

     => __getitem__ syntax is verbose, actually it's too verbose in some cases

   You don't have this problem when you keep your config/settings inside simple python files,
   however there is no standardized one-and-only-one-good-way how to keep and load those kind of
   files.


3) Recently I've found interesting presentation (https://speakerdeck.com/brutasse/stop-writing-settings-files)
   about configuration injected from environment variables. And I love the idea (untill slide No 12),
   but it has the same issues as *ini files



Configuration sources
---------------------

With "confy" you can simply load the configuration from any source you want, that gives you
flexibility on how and where you want to keep configuration::


    import confy

    with confy.loader(__file__) as confy:
        confy.module(__name__, [
            confy.from_modules('base', confy.env('CONFIGURATION_MODE', 'development')),
            confy.from_modules('local', silent=True),
            confy.from_environ_vars([
                'MY_ENV_VARIABLES_GOES_HERE',
            ], silent=True),
            confy.from_ini('~/.project_rc', silent=True),
        ])


Configuration are loaded one after another, so please keep in mind that variables might be overriden.



Installation
------------

Simple and easy::

   $ pip install confy


Docs
----

You can find documentation here: https://confy.readthedocs.org/en/latest/


Authors
-------

* Jakub Janoszek (kuba.janoszek@gmail.com)
