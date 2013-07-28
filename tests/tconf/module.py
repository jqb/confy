# -*- coding: utf-8 -*-
import os
import confy


confy =  confy.loader(__file__)


confy.define_module(__name__, [
    confy.from_modules('data/base', os.environ.get('CONFIGURATION_MODE', 'data/development')),
])
