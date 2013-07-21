# -*- coding: utf-8 -*-
import unittest
import confy


class ConfyModuleAPI(unittest.TestCase):
    def test_has_all_required_elemnets(self):
        expected = [
            'VERSION',

            # properties
            'BaseProperty', 'ImporterProperty', 'InterpolationProperty',
            'LazyProperty', 'RawProperty', 'ValueProperty',

            # loader and all the falks
            'Loader', 'loader', 'collection', 'env', 'lazyimport', 'lazy', 'raw',

            # submodules
            'utils', 'properties', 'api'
        ]
        module_contents = dir(confy)

        for name in expected:
            assert name in module_contents

