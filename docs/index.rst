.. confy documentation master file, created by
   sphinx-quickstart on Sun Jun 23 13:04:33 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

confy
=====

Pragmatic & flexible **configuration loader** that makes your app settings clean and sexy.


It reads configuration from many differnt sources including: python modules, environment
variables and *.ini files.


Basics example
--------------

Idea is quite simple and has been developed by (probably not only) django community, but has
been never standardized, so you might have seen it before in many differnt forms. Here it is:


1) keep your configuration in separate python modules inside your
   settings (or conf / config / <however-you-call-it>) module like this

   .. code-block:: bash

       settings/
         |-- __init__.py     => short and simple loading code
         |-- base.py         => or base.py or common.py or <whatever>.py - this should be common stuff
         |-- development.py  => change/add all you need to run the app in development mode
         `-- production.py   => change/add all you need to run the app in production mode


2) load those files in the order you want to get the configuration. Use environment
   variables to decide which settings should be loaded.
   In order to do that put the following snippet inside settings/__init__.py file

   .. code-block:: python

      import confy

      with confy.loader(__file__) as confy:
          config = confy.merge(
              confy.from_modules('base', confy.env('CONFIGURATION_MODE', 'development')),
          )


3) so in the end of the day you can simply import it easily and be sure that exactly configuration
   of your choice is there:

   - "base.py" was loaded first
   - according to CONFIGURATION_MODE environment variable value either "development.py" or "production.py"
     was loaded next. It overrides some (or all) variables loaded previously.


   .. code-block:: bash

      $ export CONFIGURATION_MODE=development
      $ python

   .. code-block:: python

        >>> from settings import config
        >>> assert config.MODE == 'development'

   Or:

   .. code-block:: bash

      $ export CONFIGURATION_MODE=production
      $ python

   .. code-block:: python

        >>> from settings import config
        >>> assert config.MODE == 'production'



This is just basic and really simple example. But clean loading is not the only thing "confy" does for you.


Installation
------------

Simple and straight forward:


.. code-block:: bash

   pip install confy



Source
------

All the code is hosted on github https://github.com/jqb/confy


.. toctree::
   :maxdepth: 2

   tutorial


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

