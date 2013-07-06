# -*- coding: utf-8 -*-
# sys
import os
import unittest

import six
from nose.tools import (
    assert_equal as eq,
)

# local
from . import tconf
from .fake.backend import FakeBackend


class TConfMergeTests(unittest.TestCase):
    def cleanup_dict(self, adict, *keys):
        for key in keys:
            try:
                del adict[key]
            except KeyError:
                pass

    def test_development_mode(self):
        global tconf
        os.environ['CONFIGURATION_MODE'] = 'development'

        tconf = six.moves.reload_module(tconf)

        eq(tconf.API_ADD, 'http://development.api.com/add/')
        eq(tconf.API_DELETE, 'http://development.api.com/delete/')
        eq(tconf.FAKE_BACKEND.CLASS, FakeBackend)

        self.cleanup_dict(os.environ, 'CONFIGURATION_MODE')

    def test_production_mode(self):
        global tconf
        os.environ['CONFIGURATION_MODE'] = 'production'

        tconf = six.moves.reload_module(tconf)

        eq(tconf.API_ADD, 'http://production.api.com/add/')
        eq(tconf.API_DELETE, 'http://production.api.com/delete/')
        eq(tconf.FAKE_BACKEND.CLASS, FakeBackend)

        self.cleanup_dict(os.environ, 'CONFIGURATION_MODE')


if __name__ == '__main__':
    unittest.main()
