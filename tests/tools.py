# -*- coding: utf-8 -*-
"""
Confy testing tools
"""
from nose.tools import assert_equal as eq

try:
    from nose.tools import (
        assert_in,
        assert_not_in,
    )
except ImportError:
    def assert_in(thing, container):
        assert thing in container, "There's no '%s' in %s" % (thing, repr()[:100])

    def assert_not_in(thing, container):
        assert thing not in container, "'%s' IS in %s, but shouldn't" % (thing, repr()[:100])
