# -*- coding: utf-8 -*-
# sys
import os
import unittest

from .tools import (
    eq,
    load_module,
)

# local
from .fake.backend import FakeBackend


class TConfMergeTests(unittest.TestCase):
    def cleanup_dict(self, adict, *keys):
        for key in keys:
            try:
                del adict[key]
            except KeyError:
                pass

    def test_development_mode(self):
        tconf = load_module('tests.tconf', CONFIGURATION_MODE='development')

        eq(tconf.API_ADD, 'http://development.api.com/add/')
        eq(tconf.API_DELETE, 'http://development.api.com/delete/')
        eq(tconf.FAKE_BACKEND_CLASS, FakeBackend)

        self.cleanup_dict(os.environ, 'CONFIGURATION_MODE')

    def test_production_mode(self):
        tconf = load_module('tests.tconf', CONFIGURATION_MODE='production')

        eq(tconf.API_ADD, 'http://production.api.com/add/')
        eq(tconf.API_DELETE, 'http://production.api.com/delete/')
        eq(tconf.FAKE_BACKEND_CLASS, FakeBackend)

        self.cleanup_dict(os.environ, 'CONFIGURATION_MODE')


if __name__ == '__main__':
    unittest.main()
