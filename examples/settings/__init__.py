# -*- coding: utf-8 -*-
import os
import confy


# Define loader and override module name to minimize mess inside this module.
# By having confy as context manager here highlights fact that loading configuration
# happens in special environment conditions.
with confy.loader(__file__) as confy:

    # merge few sources together into "config" variable
    # all the settings defined inside 'base', 'development'
    # (or other file which name might be defined under 'CONFIGURATION_MODE'
    # environ variable), and 'local' modules
    config = confy.merge(
        confy.from_modules('base', os.environ.get('CONFIGURATION_MODE', 'development')),
        confy.from_modules('local', silent=True),
    )
