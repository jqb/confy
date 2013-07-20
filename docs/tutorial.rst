Quick start
===========

All the examples here assumes that settings directory looks exactly
the same:

   .. code-block:: bash

       settings/
         |-- __init__.py
         |-- base.py
         |-- development.py
         |-- production.py
         `-- local.py


Content of settings/__init__.py is also the same:

   .. code-block:: python
      :linenos:

        import confy

        with confy.loader(__file__) as confy:
            config = confy.merge(
                confy.from_modules('base', 'development'),
                confy.from_modules('local', silent=True),
            )


Let's just explain what short snippet in settings/__init__.py means.

In line no 3 we're defining a loader. The important thing here is that
we are passing __file__ variable into loader constructor. This makes
our loader aware of possition in the file system where are settings
are and moreover gives usefull "confy.rootpath" method (we'll explain
it later).

Lines 4-7 loades and merges settings from the sources. For sake of
simplicity here we're loading settings only from python modules, but
later we gonna explain other possible configuration sources, too.

Line no 5 loads two modules ('base' and 'development') one after
another.

Line no 6 loads module 'local'. 'silent' param set to True means that
confy won't complain if there's no such module like 'local'. In other
words you can use it to conditionaly load modules (and other settings
sources). This is convinent to configure environment specific
settings.


Variables interpolation
-----------------------

Interpolation is an nice feature in order to make your configuration
clean and as simple as possible.  Confy uses standard python
"{variable_name}" interpolation, so you don't need to learn anything
new.  Let's see simple example.


So if you are using some kind of service inside your application you
might want to easily manage url's you need to work with to avoid
simple and annoying problems with misstyped protocol (http vs https)
and super-annoing duplication of copy-and-pasting the same root of
url.


Assuming this is content of your "settings/base.py" file:

.. literalinclude:: ../tests/tconf/base.py
   :lines: 1-8


you can easily change values of "api_domain" in development.py /
production.py and you don't need to rewrite all the urls once again.


Contents of "settings/development.py":

.. literalinclude:: ../tests/tconf/development.py
   :lines: 4,5

.. code-block:: python

   >>> import os; os.environ['CONFIGURATION_MODE'] == 'development'
   >>>
   >>> from settings import config
   >>> assert config.API_ADD == 'http://api-development.com/add/'
   >>> assert config.API_DELETE == 'http://api-development.com/delete/'


Contents of "settings/production.py":

.. literalinclude:: ../tests/tconf/production.py
   :lines: 4,5


.. code-block:: python

   >>> import os; os.environ['CONFIGURATION_MODE'] == 'production'
   >>>
   >>> from settings import config
   >>> assert config.API_ADD == 'http://production.api.com/add/'
   >>> assert config.API_DELETE == 'http://production.api.com/delete/'



Neasted structures - collections
--------------------------------

In general keeping settings as flat'n'simple variables is the best
idea, however it makes sense sometimes to avoid typing the same prefix
again and again.


Contents of your "base.py" might look like this

.. code-block:: python

   # settings/base.py
   API = confy.collection(
       domain = "http://api.com",
       ADD    = '{domain}/add/',
       DELETE = '{domain}/delete/',
   )


Then again, changing domain url is very simple, inside your
"development.py"

.. code-block:: python

   # settings/development.py
   API.update(
       domain = "http://api-development.com",
   )


.. code-block:: python

   >>> import os; os.environ['CONFIGURATION_MODE'] == 'development'
   >>>
   >>> from settings import config
   >>> assert config.API.ADD == 'http://api-development.com/add/'
   >>> assert config.API.DELETE == 'http://api-development.com/delete/'


As you can see it's preatty simple, but two things might be
interesting to you.


1) global "confy" object?

   yes - it is global helper **buy ONLY inside your settings folder**
   and it is global only for the time when module is beeing
   loaded. Thats why It's been decided to use "with confy.loader"
   statement instead of simple assigment.


2) "confy.collection"

   creates confy collection object. Basicaly all you need to know is
   that it behaves exactly as a dictionary, and has additional
   features like to recognize "{interpolation_variables}" and ability
   to use __getitem__ notation for keys if you want to (keys might be
   non-identifiers as well - but ofcourse you won't be able to get
   them with "." notation).

   .. code-block:: python

      >>> from settings import config
      >>> config.API.ADD == config.API['ADD']  # => True


Lazy property
-------------

Having interpolation property is nice feature but it very rarely
happens that you need more flexibility. "lazy" property is allowing
you to create property-like function that'll be invoked to calculate
value.

.. code-block:: python

   API = confy.collection(
       domain = "http://api.com",
       ADD    = '{domain}/add/',
       DELETE = '{domain}/delete/',
       ALL   = confy.lazy(lambda self: "%s, %s" % (self.ADD, self.DELETE)),
   )

   all_urls = API.ALL  # the function that was passed to "confy.lazy" is invoked here
   assert all_urls == "http://api.com/add/, http://api.com/delete/"


Lazy import property
--------------------

It's often practice to store complete path to
"somekind.of.BackendClass" in settings file.  Hovever you always need
to write code that will later use it to acctualy import the think.
You can stop thinking about it:

.. code-block:: python

   # settings/base.py
   SUPER_DUPER_BACKEND = confy.lazyimport('somekind.of.BackendClass')


.. code-block:: python

   >>> from settings import config  # no import here...
   >>> config.SUPER_DUPER_BACKEND   # ...but here the import is done and BackendClass is ready for you


Raw propery
-----------

Ok - but you really want to use "{}" chars inside your setting
string - exactly as they are. - No problem:


.. code-block:: python

   # settings/base.py
   RAW_STRING = confy.raw('use as many {} specia; {{{ }}}}} () characters as you want')
