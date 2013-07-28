# -*- coding: utf-8 -*-
import os
import confy


confy = confy.loader(__file__)

config = confy.merge(
    confy.from_modules('data/base', os.environ.get('CONFIGURATION_MODE', 'data/development')),
)
