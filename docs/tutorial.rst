Quick start
===========

All the examples here assumes that settings directory looks exactly the same:

   .. code-block:: bash

       settings/
         |-- __init__.py
         |-- base.py
         |-- development.py
         `-- production.py


Content of settings/__init__.py is also the same:

   .. code-block:: python

        import confy

        with confy.loader(__file__) as confy:
            config = confy.from_modules('base', confy.env('CONFIGURATION_MODE', 'development'))



Variables interpolation
-----------------------

Interpolation is an nice feature in order to make your configuration clean and as simple as possible.
Confy uses standard python "{variable_name}" interpolation, so you don't need to learn anything new.
Let's see simple example.


So if you are using some kind of service inside your application you might want to easily manage
url's you need to work with to avoid simple and annoying problems with misstyped protocol (http vs https)
and super-annoing duplication of copy-and-pasting the same root of url.


Assuming this is content of your "settings/base.py" file:

.. literalinclude:: ../tests/tconf/base.py
   :lines: 1-8


you can easily change values of "api_domain" and "s3_assets_domain" in development.py/production.py
and you don't need to rewrite all the urls once again.


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



Neasted structures
------------------

In general keeping settings as flat'n'simple variables is the best idea, however it makes sense
sometimes to avoid typing the same prefix again and again.


Contents of your "base.py" might look like this

.. code-block:: python

   API = confy.collection(
       domain = "http://api.com",
       ADD    = '{api_domain}/add/'
       DELETE = '{api_domain}/delete/'
   )


Then again, changing domain url is very simple, inside your "development.py"

.. code-block:: python

   API.update(
       domain = "http://api.com",
   )


.. code-block:: python

   >>> import os; os.environ['CONFIGURATION_MODE'] == 'development'
   >>>
   >>> from settings import config
   >>> assert config.API.ADD == 'http://api-development.com/add/'
   >>> assert config.API.DELETE == 'http://api-development.com/delete/'


As you can see it's preatty simple, but two things might have been interested to you.

1) global "confy" object?

   yes - it is global helper **buy ONLY inside your settings folder** and it is global
   only for the time when module is beeing loaded


2) "confy.collection"

   creates confy collection object. Basicaly all you need to know is that it
   behaves exactly as a dictionary, and has additional features like to recognize
   "{interpolation_variables}"

