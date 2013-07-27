# -*- coding: utf-8 -*-
import os
import confy


with confy.loader(__file__) as confy:
    confy.module(__name__, [
        confy.from_modules('data/base', os.environ.get('CONFIGURATION_MODE', 'data/development')),
    ])
