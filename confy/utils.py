# -*- coding: utf-8 -*-
import sys
import importlib
from os.path import join, dirname, abspath

import six


def create_path_function(thefile):
    root = abspath(join(dirname(abspath(thefile))))
    return lambda *a: abspath(join(root, *a))


class extrabuiltins(object):
    def __init__(self, things):
        self.things = things
        self.builtins = six.moves.builtins

    def extend(self):
        for name, thing in self.things.items():
            setattr(self.builtins, name, thing)

    def cleanup(self):
        for name in self.things:
            delattr(self.builtins, name)

    def __enter__(self):
        self.extend()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()


class syspath(object):
    def __init__(self, paths, sys_path=None):
        self.paths = paths
        self.sys_path = sys_path or sys.path

    def extend(self):
        if self.paths:
            for path in reversed(self.paths):
                self.sys_path.insert(0, path)

    def cleanup(self):
        if self.paths:
            for path in reversed(self.paths):
                self.sys_path.remove(path)

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
