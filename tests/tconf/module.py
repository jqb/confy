# -*- coding: utf-8 -*-
import confy


with confy.loader(__file__) as confy:
    confy.module(__name__, [
        confy.from_modules('data/base', confy.env('CONFIGURATION_MODE', 'data/development')),
    ])
