# -*- coding: utf-8 -*-
import sys
from os.path import join, dirname, abspath

from .compat import six
from .packages import importlib


def create_path_function(thefile):
    root = abspath(join(dirname(abspath(thefile))))
    return lambda *a: abspath(join(root, *a))


class extrabuiltins(object):
    def __init__(self, things, builtins=None):
        self.things = things or {}
        self.builtins = builtins or six.moves.builtins

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
        self.paths = paths or []
        self.sys_path = sys.path if sys_path == None else sys_path

    def extend(self):
        for path in reversed(self.paths):
            self.sys_path.insert(0, path)

    def cleanup(self):
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
                self.__importeditem = item
                return item

            try:
                self.__importeditem = getattr(item, last_item)
            except AttributeError as e:
                raise ImportError("Module '%s': => %s" % (path_to_item, six.text_type(e)))
        return self.__importeditem


def smart_ext(name, ext=None):
    """
    Smartly add extention to the file name

    Usage::

        >>> smart_ext("config")
        "config"
        >>> smart_ext("config.py")
        "config.py"
        >>> smart_ext("config", ext="py")
        "config.py"
        >>> smart_ext("config.py", ext="py")
        "config.py"

    """
    if ext is None:
        return name

    ext = ".%s" % ext if not ext.startswith(".") else ext
    name = name.strip()
    existing_ext = name.rsplit(".", 1)[-1]

    if existing_ext == name:  # no ext acctually
        return "%s%s" % (name, ext)

    return name


def split_filenames(names, abspath=None, ext=None):
    abspath = abspath or (lambda x: x)
    splited = []
    for name in names:
        splited.extend(
            [abspath(smart_ext(s, ext=ext)) for s in name.split(',')]
        )
    return splited


def private_attribute_name(cls, name):
    """ Properly construct name of private variable for the given class.

    :param cls: class object for which the name should be constructed
    :param name: name of the variable

    Usage::

        class User(object):
            def __init__(self, name):
                self.__name = name


        user = User("John")

        # you can't do this
        # user.__name

        # ...but you can do this
        user._User__name == 'John'  # => True
        getattr(user, private_attribute_name(User, 'name')) == 'John'  # => True

    """
    return "_%s__%s" % (cls.__name__, name)
