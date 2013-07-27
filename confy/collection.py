# -*- coding: utf-8 -*-
from types import ModuleType
from collections import MutableMapping, Mapping

import six

from .properties import (
    LazyProperty, RawProperty, InterpolationProperty,
    ImporterProperty, ValueProperty, LazyRootpathProperty,
)


class Collection(object):

    # For extendibility purposes we might want to change / add some properties
    property_classes = [
        LazyRootpathProperty,
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


    # collectionize
    @classmethod
    def collectionize(cls, adict, defaults=None):
        """ Change a dict into a collection. All inner dictionaries
        are changed into collections as well.

        :param adict: dictionary (collections.Mapping) alike object
        :param defaults: default attributes that will be added to all
        new collection objects
        """

        def new(adict):
            c = cls(defaults or {})
            c.update(adict)
            return c

        def convert(adict):
            for key in list(adict.keys()):
                value = adict[key]
                if isinstance(value, Mapping):
                    adict[key] = new(convert(value))
            return new(adict)

        return convert(adict)
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
        return prop.get(self)

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
                "update() takes at most 2 positional arguments ({0} given)".format(args_len)
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
            return False
        return dict(self.items()) == dict(other.items())

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        return len(self.__data)

    # Extra *Collection* methods
    def properties(self):
        return [(name, self.__data[name]) for name in self.keys()]

    def extend(self, *args, **kwargs):
        attrs = Collection(self.properties())
        attrs.update(*args, **kwargs)
        return attrs

    def raw(self, name):
        return self.__raw(name)

    def raw_items(self):
        return [(name, self.__raw(name)) for name in self.keys()]

    def raw_values(self):
        return [self.__raw(name) for name in self.keys()]
    # end

    def __str__(self):
        return six.u('<Collection: %s>' % [
            key for key in self.keys() if not key.startswith('_')
        ])

    __unicode__ = __repr__ = __str__


MutableMapping.register(Collection)


class Module(ModuleType):
    def __init__(self, module_name, filepath, collection):
        super(Module, self).__init__(module_name)
        self.__file__ = filepath
        for name, value in collection.items():
            setattr(self, name, value)

    def __getitem__(self, name):
        return getattr(self, name)
