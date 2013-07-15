# -*- coding: utf-8 -*-
"""
Confy testing tools
"""
import os
import sys

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


def load_module(settings_module_name, **env_kwargs):
    """
    load / reload given module.
    """
    from confy.packages.importlib import import_module

    old_environ = dict(os.environ)
    os.environ.update(env_kwargs)

    if settings_module_name in sys.modules:
        del sys.modules[settings_module_name]

    module = import_module(settings_module_name)

    os.environ = old_environ
    return module
