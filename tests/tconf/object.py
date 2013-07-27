# -*- coding: utf-8 -*-
import os
import confy


with confy.loader(__file__) as confy:
    config = confy.merge(
        confy.from_modules('data/base', os.environ.get('CONFIGURATION_MODE', 'data/development')),
    )
