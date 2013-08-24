# -*- coding: utf-8 -*-
VERSION = '0.3.8'


from .api import Loader
from .collection import Module, Collection
from .properties import (
    BaseProperty, ValueProperty, InterpolationProperty, ImporterProperty,
    RawProperty, LazyProperty,
)

loader = Loader
collection = Loader.collection

lazyimport = Loader.lazyimport
lazy = Loader.lazy
raw = Loader.raw
rootpath = Loader.rootpath
