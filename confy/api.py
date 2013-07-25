# -*- coding: utf-8 -*-
import os
import sys

from .utils import create_path_function, extrabuiltins, syspath, Importer, split_filenames
from .collection import Collection, RawProperty, LazyProperty, Module, LazyRootpathProperty
from .sources import ModuleSource, EnvironmentVariableSource, INISource


class Loader(object):
    collection = Collection
    lazyimport = Importer
    lazy = LazyProperty
    raw = RawProperty
    rootpath = LazyRootpathProperty

    def __init__(self, file=None, syspaths=None):
        self._file = file or '.'
        self._syspaths = syspaths or ['.']
        self._rootpath = create_path_function(self._file)
        self._factories = {}

    # experimental api
    def factory(self, function):
        def invoker(*args, **kwargs):
            return function(self, *args, **kwargs)
        self._factories[function.__name__] = invoker
        return invoker

    def __getattr__(self, name):
        factories = self._factories
        if name in factories:
            return factories[name]
        return object.__getattribute__(self, name)
    # end

    # api
    def merge(self, *sources):
        context = {
            '__rootpath__': self._file,
        }
        for s in sources:
            context = s.load(context)
        return self.collection(**context)

    def module(self, name, sources):
        sys.modules[name] = Module(name, self._file, self.merge(*sources))

    def from_modules(self, *files, **kwargs):
        return ModuleSource(
            names=split_filenames(files, abspath=self._rootpath, ext=kwargs.get('ext', 'py')),
            silent=kwargs.get('silent'),
        )

    def from_environ_vars(self, names, silent=False):
        return EnvironmentVariableSource(
            names=names,
            silent=silent,
            environ=os.environ,
        )

    def from_ini(self, *files, **kwargs):
        return INISource(
            names=split_filenames(files, abspath=self._rootpath, ext=kwargs.get('ext', 'ini')),
            silent=kwargs.get('silent')
        )

    @classmethod
    def env(cls, name, default=None):
        return os.environ.get(name, default)
    # end

    # processing configuration
    def _get_syspath(self, paths=None):
        syspaths = paths or []
        syspaths.extend(self._syspaths)
        return [self._rootpath(*s.split(os.sep)) for s in syspaths]

    def _get_extrabuildins(self):
        return {
            'confy': self
        }
    # end

    # context manager support
    def __enter__(self):
        self._ctx_syspath = syspath(self._get_syspath())
        self._ctx_extrabuildins = extrabuiltins(self._get_extrabuildins())
        self._ctx_syspath.extend()
        self._ctx_extrabuildins.extend()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ctx_syspath.cleanup()
        self._ctx_extrabuildins.cleanup()
        del self._ctx_syspath
        del self._ctx_extrabuildins
    # end
