# -*- coding: utf-8 -*-
from collections import MutableMapping, Mapping

from .properties import (
    LazyProperty, RawProperty, InterpolationProperty,
    ImporterProperty, ValueProperty
)


class Collection(object):

    # For extendibility purposes we might want to change / add some properties
    property_classes = [
        LazyProperty,
        RawProperty,
        InterpolationProperty,
        ImporterProperty,
        ValueProperty,
    ]

    def _choose_property(self, name, value):
        for property_cls in self.property_classes:
            prop, success = property_cls.build(name, value)
            if success:
                return prop
        raise ValueError("No property for: %s | %s" % (name, value))
    # end


    def __init__(self, *args, **kwargs):
        dict_data_key = "_%s__data" % self.__class__.__name__
        self.__dict__.update({
            dict_data_key: {},
        })
        self.update(*args, **kwargs)


    # Protected general read / write methods
    def __set(self, name, value):
        self.__data[name] = self._choose_property(name, value)

    def __property(self, name):
        try:
            return self.__data[name]
        except KeyError:
            raise KeyError("Collection has no such key: %s" % name)

    def __get(self, name):
        prop = self.__property(name)
        return prop.get(self)

    def __raw(self, name):
        prop = self.__property(name)
        return prop.raw_value
    # end


    # [] set, get & del protocol
    def __setitem__(self, name, value):
        self.__set(name, value)

    def __getitem__(self, name):
        return self.__get(name)

    def __delitem__(self, name):
        del self.__data[name]
    # end


    # support for get attribute protocol
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return self.__get(name)

    def __setattr__(self, name, value):
        self.__set(name, value)
    # end


    def pop(self, key, **kwargs):
        try:
            prop = self.__data.pop(key, **kwargs)
        except KeyError:
            raise KeyError("Collection has no such key: %s" % key)
        if isinstance(prop, BaseProperty):
            return prop.get(self)
        return prop

    def popitem(self):
        try:
            key = next(iter(self.__data))
        except StopIteration:
            raise KeyError
        value = self.__get(key)
        del self.__data[key]
        return key, value

    def update(*args, **kwds):
        args_len = len(args)

        if args_len > 2:
            raise TypeError(
                "update() takes at most 2 positional arguments ({} given)".format(args_len)
            )
        elif not args:
            raise TypeError("update() takes at least 1 argument (0 given)")

        self = args[0]
        other = args[1] if args_len >= 2 else ()

        if isinstance(other, Mapping):
            for key in other:
                self.__set(key, other[key])
        elif hasattr(other, "keys"):
            for key in other.keys():
                self.__set(key, other[key])
        else:
            for key, value in other:
                self.__set(key, value)
        for key, value in kwds.items():
            self.__set(key, value)

    def setdefault(self, key, default=None):
        try:
            return self.__get(key)
        except KeyError:
            self.__set(key, default)
        return default

    def clear(self):
        self.__data.clear()

    def keys(self):
        return self.__data.keys()

    def items(self):
        return [(name, self.__get(name)) for name in self.__data]

    def values(self):
        return [self.__get(key) for key in self]

    def iterkeys(self):
        return iter(self.__data.keys())

    def itervalues(self):
        for key in self:
            yield self.__get(key)

    def iteritems(self):
        for key in self:
            yield (key, self.__get(key))

    def __iter__(self):
        return iter(self.__data)

    def __contains__(self, key):
        return key in self.__data

    def get(self, key, default=None):
        try:
            return self.__get(key)
        except KeyError:
            return default

    def __eq__(self, other):
        if not isinstance(other, Mapping):
            return NotImplemented
        return dict(self.items()) == dict(other.items())

    def __ne__(self, other):
        return not (self == other)

    # Extra *Collection* methods
    def raw_items(self):
        return [(name, self.__data[name]) for name in self.keys()]

    def extend(self, *args, **kwargs):
        attrs = Collection(self.raw_items())
        attrs.update(*args, **kwargs)
        return attrs
    # end


MutableMapping.register(Collection)
collection = Collection()
