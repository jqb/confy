# -*- coding: utf-8 -*-
import fnmatch

from collections import Mapping

from .compat import izip


def get(adict, composed_key):
    data = adict
    for key in composed_key:
        data = data[key]
    return data


def set(adict, composed_key, value, dictfactory=dict):
    data = adict
    for key in composed_key[:-1]:
        if key not in data:
            data[key] = dictfactory()
        data = data[key]
    data[composed_key[-1]] = value


def keys(adict, composed_key_list):
    def walk(mapping, visitor, path=()):
        for key, value in mapping.items():
            if isinstance(value, Mapping):
                walk(value, visitor, path + (key,))
            else:
                visitor(path + (key,), value)

    paths = []

    def visitor(path, value):
        for composed_key in composed_key_list:
            if all([
                fnmatch.fnmatch(k, ptr)
                for k, ptr in izip(path, composed_key)
            ]) and path not in paths:
                paths.append(path)

    walk(adict, visitor)
    return paths


def query(adict, composed_key_list):
    composed_keys = keys(adict, composed_key_list)
    adict = [
        (ckey, get(adict, ckey)) for ckey in composed_keys
    ]
    return adict
