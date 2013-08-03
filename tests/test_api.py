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
            'Loader', 'loader', 'collection', 'lazyimport', 'lazy', 'raw',

            # submodules
            'utils', 'properties', 'api'
        ]
        module_contents = dir(confy)

        for name in expected:
            assert name in module_contents


class LoaderApi(unittest.TestCase):
    def test_merge_should_not_contain_any_variables(self):
        expected = []
        loader = confy.loader()

        collection = loader.merge(
            # no sources == empty collection
        )
        assert len(collection) == 0

        for name in expected:
            assert name in collection
