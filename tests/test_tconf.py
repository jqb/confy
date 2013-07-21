# -*- coding: utf-8 -*-
# sys
import unittest

from .tools import (
    load_module,
)

# local
from .fake.backend import FakeBackend


class TConfMergeTests(unittest.TestCase):
    def test_module_development_mode(self):
        tconf = load_module('tests.tconf.module', CONFIGURATION_MODE='data/development')
        assert tconf.API_ADD == 'http://development.api.com/add/'
        assert tconf.API_DELETE == 'http://development.api.com/delete/'
        assert tconf.FAKE_BACKEND_CLASS == FakeBackend

    def test_module_production_mode(self):
        tconf = load_module('tests.tconf.module', CONFIGURATION_MODE='data/production')
        assert tconf.API_ADD == 'http://production.api.com/add/'
        assert tconf.API_DELETE == 'http://production.api.com/delete/'
        assert tconf.FAKE_BACKEND_CLASS == FakeBackend

    def test_merge_development_mode(self):
        tconf = load_module('tests.tconf.object', CONFIGURATION_MODE='data/development')
        tconf = tconf.config
        assert tconf.API_ADD == 'http://development.api.com/add/'
        assert tconf.API_DELETE == 'http://development.api.com/delete/'
        assert tconf.FAKE_BACKEND_CLASS == FakeBackend

    def test_merge_production_mode(self):
        tconf = load_module('tests.tconf.object', CONFIGURATION_MODE='data/production')
        tconf = tconf.config
        assert tconf.API_ADD == 'http://production.api.com/add/'
        assert tconf.API_DELETE == 'http://production.api.com/delete/'
        assert tconf.FAKE_BACKEND_CLASS == FakeBackend


if __name__ == '__main__':
    unittest.main()
