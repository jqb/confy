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
        self._file = file or './_current_directory_'
        self._syspaths = syspaths or ['.']
        self._rootpath = create_path_function(self._file)

    # processing configuration
    def _get_syspath(self):
        return [self._rootpath(*s.split(os.sep)) for s in self._syspaths]

    def _get_extrabuildins(self):
        return {
            'confy': self
        }
    # end

    # api
    def merge(self, *sources):
        def do_merge(context):
            for s in sources:
                context = s.load(context)
            return context

        with syspath(self._get_syspath()):
            with extrabuiltins(self._get_extrabuildins()):
                context = do_merge({})

        return Collection.collectionize(context, defaults={
            '__rootpath__': self._file,
        })

    def define_module(self, name, sources):
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
    # end
