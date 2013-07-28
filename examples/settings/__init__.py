# -*- coding: utf-8 -*-
import os
import confy


# Define loader and override module name to minimize mess inside this
# module.
confy = confy.loader(__file__)


# merge few sources together into "config" variable all the settings
# defined inside 'base', 'development' (or other file which name might
# be defined under 'CONFIGURATION_MODE' environ variable in this
# case), and 'local' modules
config = confy.merge(
    confy.from_modules('base', os.environ.get('CONFIGURATION_MODE', 'development')),
    confy.from_modules('local', silent=True),
)
