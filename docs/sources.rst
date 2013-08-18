Source
======

``confy`` supports number of formats from which you can read configuration.
You can see how it works with with modules in quick start tutorial. Here
I'm gonna explain other features.


1) Let's extend our example from quick start tutorial.
   Settings directory now looks like this:


   .. code-block:: bash

       settings/
         |-- __init__.py
         |-- base.py
         |-- development.py
         |-- production.py
         |-- local.py
         |-- sample.ini              # <= ini file
         `-- envvars/                # <= directory with variables like for "envdir"
               |-- DATABASE/         #    http://cr.yp.to/daemontools/envdir.html
               |     |-- USER
               |     |-- PASSWORD
               |     |-- PORT
               |     |-- NAME
               |     `-- HOST
               `-- HELLO


   If you don't have idea how example ``envvars`` could look like,
   please visit
   https://github.com/jqb/confy/tree/master/tests/tconf/envvars inside
   ``confy`` tests directory.


2) Content for ``settings/__init__.py`` for all examples below goes as
   follows:

   .. code-block:: python
      :linenos:

        import confy

        confy = confy.loader(__file__)
        config = confy.merge(
            confy.from_modules('base', 'development'),
            confy.from_modules('local', silent=True),
            confy.from_ini('sample.ini'),
            confy.from_dirs('envvars'),
        )


INI files
---------

``confy`` can easily read standard "ini" files.  If - let's say -
content of ``sample.ini`` is

.. code-block:: ini

   [DEFAULT]
   root = /home/user

   [static]
   project_dir = %{root}/static

   [media]
   project.dir = %{root}/media    # note there's "." not "_" in variable name


when this is what you gonna get when you import ``config`` from
``settings/__init__.py``


.. code-block:: python

   from settings import config

   assert config.static.project_dir == "/home/user/static"   # OK
   assert config.media['project.dir'] == "/home/user/media"  # OK


As you can see ``confy`` supports "." notation as far as variable
names allows it to do so.


Envdir source
-------------

If you know ``deamontools'`` envdir that will be easy
(http://cr.yp.to/daemontools/envdir.html). ``confy`` reads data inside
env directory easily. It's a little bit more powerfull since you're
not restricted to flat names only. Every directory inside pointed
directory is treaded as key in dictionary, so you can have neasted
structures as well.

In my extended example you can see ``envvars`` directory which is read
by ``confy``. This is what you gonna get (all the values are from
confy tests folder: https://github.com/jqb/confy/tree/master/tests/tconf/envvars)


.. code-block:: python

   from settings import config

   assert config.DATABASE.USER == "testdb"       # OK
   assert config.DATABASE.PASSWORD == "testdb"   # OK
   assert config.DATABASE.POST == "9000"         # OK
   # etc...

   assert config.HELLO == "world!"               # OK
