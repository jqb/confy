# -*- coding: utf-8 -*-
import confy


with confy.loader(__file__) as confy:
    locals().update(confy.from_modules(
        'base', confy.env('CONFIGURATION_MODE', 'development'),
    ))


del confy
