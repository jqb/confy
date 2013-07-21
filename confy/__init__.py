# -*- coding: utf-8 -*-
VERSION = '0.3.1beta'


from .api import Loader
from .properties import (
    BaseProperty, ValueProperty, InterpolationProperty, ImporterProperty,
    RawProperty, LazyProperty,
)

loader = Loader
collection = Loader.collection
env = Loader.env

lazyimport = Loader.lazyimport
lazy = Loader.lazy
raw = Loader.raw
