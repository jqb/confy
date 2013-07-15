# -*- coding: utf-8 -*-
import confy


with confy.loader(__file__) as confy:
    config = confy.merge(
        confy.from_modules('data/base', confy.env('CONFIGURATION_MODE', 'data/development')),
    )
