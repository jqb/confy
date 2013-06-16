# -*- coding: utf-8 -*-
VERSION = '0.2beta'


from .api import Loader
from .properties import (
    BaseProperty, ValueProperty, InterpolationProperty, ImporterProperty,
    RawProperty, LazyProperty,
)

loader = Loader
collection = Loader.collection
env = Loader.env
Collection = Loader.Collection
