# -*- coding: utf-8 -*-
import re

import six

from .utils import Importer


class BaseProperty(object):
    def get(self, instance):
        raise NotImplementedError

    @property
    def raw_value(self):
        raise NotImplementedError

    @classmethod
    def build(cls, name, value):
        raise NotImplementedError


class ValueProperty(BaseProperty):
    def __init__(self, value):
        self.value = value

    def get(self, instance):
        return self.value

    @property
    def raw_value(self):
        return self.value

    @classmethod
    def build(cls, name, value):
        if isinstance(value, BaseProperty):
            return value, True
        return cls(value), True


class InterpolationProperty(BaseProperty):
    var_re = re.compile('\{[ ]*(\w+)[ ]*\}')

    def __init__(self, name, template, var_names):
        self.name = name
        self.template = template
        self.var_names = var_names

    def call_callables(self, instance, name):
        attr = instance[name]
        func = getattr(attr, '__call__', lambda: attr)
        return func()

    def get(self, instance):
        values = dict([
            (vname, self.call_callables(instance, vname))
            for vname in self.var_names
        ])
        return self.template.format(**values)

    @property
    def raw_value(self):
        return self.template

    @classmethod
    def build(cls, name, value):
        if isinstance(value, six.string_types):
            var_names = cls.var_re.findall(value)
            if var_names:
                return cls(name, value, var_names), True
        return None, False


class ImporterProperty(BaseProperty):
    def __init__(self, importer):
        self.importer = importer

    def get(self, instance):
        return self.importer.import_it()

    @property
    def raw_value(self):
        return self.importer

    @classmethod
    def build(cls, name, value):
        if isinstance(value, Importer):
            return cls(value), True
        return None, False


class RawProperty(BaseProperty, six.text_type):
    def get(self, instance):
        return self

    @property
    def raw_value(self):
        return self

    @classmethod
    def build(cls, name, value):
        if isinstance(value, cls):
            return value, True
        return None, False


class LazyProperty(BaseProperty):
    def __init__(self, get):
        self.__get = get

    def get(self, instance):
        return self.__get(instance)

    @property
    def raw_value(self):
        return self.__get

    @classmethod
    def build(cls, name, value):
        if isinstance(value, cls):
            return value, True
        return None, False
