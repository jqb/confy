# -*- coding: utf-8 -*-

try:
    import importlib
except ImportError:
    from .packages import importlib


try:
    import six
except ImportError:
    from .packages import six


try:
    from itertools import izip
except ImportError:
    izip = zip
