# -*- coding: utf-8 -*-
import re
import inspect
from itertools import chain
from collections import Mapping

import six

from .utils import OrderedSet, Importer


var_re = re.compile('\{[ ]*(\w+)[ ]*\}')
identifier_re = re.compile('[_A-Za-z][_a-zA-Z0-9]*$')


class InterpolationProperty(object):
    def __init__(self, name, template, var_names):
        self.name = name
        self.template = template
        self.var_names = var_names

    def call_callables(self, attr):
        func = getattr(attr, '__call__', lambda: attr)
        return func()

    def __get__(self, instance, type=None):
        values = dict([
            (vname, self.call_callables(instance[vname]))
            for vname in self.var_names
        ])
        return self.template.format(**values)


class ImporterProperty(object):
    def __init__(self, importer):
        self.importer = importer

    def __get__(self, instance, type=None):
        return self.importer.import_it()


class Raw(six.text_type):
    pass


class CollectionMeta(type):
    @classmethod
    def __choose_property(cls, name, value):
        if issubclass(value.__class__, Importer):
            return ImporterProperty(value)

        if issubclass(value.__class__, six.string_types) and not issubclass(value.__class__, Raw):
            var_names = var_re.findall(value)
            if var_names:
                return InterpolationProperty(name, value, var_names)

        return value

    def __new__(cls, cls_name, bases, attrs):
        super_new = super(CollectionMeta, cls).__new__

        visible_attributes = OrderedSet(chain.from_iterable(
            elem for elem in (getattr(base, '_attributes', []) for base in bases)
        ))

        for name, value in attrs.items():
            if not inspect.isfunction(value) and not name.startswith("_"):
                visible_attributes.add(name)
            attrs[name] = cls.__choose_property(name, value)

        attrs.update(
            _attributes=list(visible_attributes),
        )
        return super_new(cls, cls_name, bases, attrs)


class Collection(six.with_metaclass(CollectionMeta)):
    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise KeyError(name)

    def __iter__(self):
        return iter(self._attributes)

    def __unicode__(self):
        return six.u("<Collection: %s>") % ", ".join(self._attributes)

    def __str__(self):
        return unicode(self)

    def __repr__(self):
        return unicode(self)

    def __setitem__(self, name, value):
        setattr(self, name, value)

    def _merge(self, mapping):
        for key in mapping.keys():
            self[key] = mapping[key]

    def _from_sequence(self, seq):
        for double in seq:
            if len(double) != 2:
                raise ValueError("{0!r} doesn't have a length of 2".format(
                        double))
            self[double[0]] = double[1]

    def _update(self, arg, kwargs):
        if arg:
            if isinstance(arg, Mapping):
                self._merge(arg)
            else:
                self._from_sequence(arg)
        if kwargs:
            self._merge(kwargs)

    def update(self, arg=None, **kwargs):
        self._update(arg, kwargs)

    def items(self):
        return zip(self._attributes, self)

    def keys(self):
        return self._attributes

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    @classmethod
    def extend(cls, **kwargs):
        newtype = type("Collection", (cls,), kwargs)
        return newtype()


Mapping.register(Collection)
collection = Collection()
