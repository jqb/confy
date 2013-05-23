# -*- coding: utf-8 -*-
import importlib
import collections
from os.path import join, dirname, abspath
from contextlib import contextmanager

import six


def create_path_function(thefile):
    root = abspath(join(dirname(abspath(thefile))))
    return lambda *a: abspath(join(root, *a))


@contextmanager
def extrabuiltins(things):
    builtins = six.moves.builtins
    try:
        for name, thing in things.items():
            setattr(builtins, name, thing)
        yield
    finally:
        for name in things:
            delattr(builtins, name)


class syspath(object):
    def __init__(self, paths):
        self.paths = paths

    def extend(self):
        import sys
        if self.paths:
            for path in reversed(self.paths):
                sys.path.insert(0, path)

    def cleanup(self):
        import sys
        if self.paths:
            for path in reversed(self.paths):
                sys.path.remove(path)

    def __enter__(self):
        self.extend()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()



def execfile(file_path, global_vars=None, local_vars=None):
    with open(file_path) as f:
        code = compile(f.read(), file_path, 'exec')
        six.exec_(code, global_vars, local_vars)
    return global_vars, local_vars


def flatten(*things, **kwargs):
    flat_only_types = tuple(kwargs.get('flat_only') or ())
    flatten = []

    def item_and_item_type(item):
        return item, type(item)

    for m, m_type in map(item_and_item_type, things):
        if not flat_only_types and issubclass(m_type, collections.Iterable):
            flatten.extend(m)
        elif issubclass(m_type, flat_only_types):
            flatten.extend(m)
        else:
            flatten.append(m)

    return flatten


class OrderedSet(collections.OrderedDict):
    def __init__(self, sequence=None):
        super(OrderedSet, self).__init__([
            (e, True) for e in (sequence or [])
        ])

    def add(self, elem):
        self[elem] = True

    def extend(self, sequence):
        for elem in sequence:
            self[elem] = True


class Importer(object):
    def __init__(self, path):
        self.__path = path
        self.__importeditem = None

    def import_it(self):
        if not self.__importeditem:
            if '.' in self.__path:
                path_to_item, last_item = self.__path.rsplit('.', 1)
            else:
                path_to_item, last_item = self.__path, None

            item = importlib.import_module(path_to_item)

            if last_item is None:
                return item

            try:
                self.__importeditem = getattr(item, last_item)
            except AttributeError as e:
                raise AttributeError("Module '%s': => %s" % (path_to_item, e.message))
        return self.__importeditem
