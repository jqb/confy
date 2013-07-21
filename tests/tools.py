# -*- coding: utf-8 -*-
"""
Confy testing tools
"""
import os
import sys


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
