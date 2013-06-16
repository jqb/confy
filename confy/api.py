# -*- coding: utf-8 -*-
import os
import sys
import imp

from .utils import flatten, create_path_function, extrabuiltins, syspath, execfile, Importer
from .collection import Collection, RawProperty, LazyProperty


class Loader(object):
    conf_config_extention = 'py'
    conf_global_confy_object_name = 'confy'

    Collection = Collection
    lazyimport = Importer
    lazy = LazyProperty
    raw = RawProperty


    def __init__(self, file=None, syspaths=None, config_extention=None):
        self._file = file
        self._syspaths = syspaths or ['.']
        self.conf_config_extention = config_extention or self.__class__.conf_config_extention

        if self._file:
            self.rootpath = create_path_function(self._file)
        else:
            self.rootpath = None

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


    # execfile processing configuration
    def _get_syspath(self, paths=None):
        syspaths = paths or []
        syspaths.extend(self._syspaths)
        if not self.rootpath:
            return []
        return [self.rootpath(*s.split(os.sep)) for s in syspaths]

    def _get_extrabuildins(self, extrabuiltins=None):
        extras = extrabuiltins or {}
        if self.conf_global_confy_object_name not in extras:
            extras[self.conf_global_confy_object_name] = self
        return extras

    def _get_config_extention(self, config_extention=None):
        extention = config_extention or self.conf_config_extention
        return ".%s" % extention if extention else ""
    # end


    # processing
    def _before_execfiles(self, context):
        return context

    def _execfile(self, relative_path, context, silent=False):
        try:
            execfile(self.rootpath(relative_path), global_vars=context)
        except IOError:
            if not silent:
                raise
        return context

    def _after_execfile(self, context, module_names):
        if 'MODE' not in context:
            context.update(MODE=module_names[-1])
        return context

    def _merge_modules(self, *things, **kwargs):
        syspaths = self._get_syspath(kwargs.get('syspath'))
        extras = self._get_extrabuildins(kwargs.get('extrabuiltins'))
        config_extention = self._get_config_extention(kwargs.get('config_extention'))
        silent = kwargs.get('silent')

        with syspath(syspaths):
            with extrabuiltins(extras):
                attributes = self._before_execfiles({})

                module_names = flatten(things, flat_only=[list, tuple])
                for m in module_names:
                    attributes = self._execfile(
                        '%s%s' % (m, config_extention), attributes, silent=silent
                    )
                attributes = self._after_execfile(attributes, module_names)

        return attributes
    # end


    # api
    def merge(self, *mappings):
        attrs = self.collection()
        for m in mappings:
            attrs.update(m)
        return attrs

    def module(self, name, mappings, add_to_sysmodules=True):
        module = imp.new_module(name)
        module.__file__ = self._file
        module.__dict__.update(self.merge(*mappings))
        if add_to_sysmodules:
            sys.modules[name] = module
        return module

    def from_modules(self, *files, **kwargs):
        splited = []
        for file in files:
            splited.extend(
                map(lambda s: s.strip(), file.split(','))
            )
        merged = self._merge_modules(*splited, **kwargs)
        return self.collection(**merged)

    def from_object(self, path, **kwargs):
        module_path, object_name = path.rsplit('.', 1)
        module = self.from_modules(module_path, **kwargs)
        return getattr(module, object_name)

    def from_environ_vars(self, variables, silent=False):
        data = {}
        for vardef in variables:
            if ":" in vardef:
                env_name, setting_name = vardef.split(":")
            else:
                env_name = setting_name = vardef
            try:
                data[setting_name] = os.environ[env_name]
            except KeyError:
                if not silent:
                    raise

        return self.new(**data)

    @classmethod
    def env(cls, name, default=None, environ=None):
        environ = environ or os.environ
        return environ.get(name, default)

    new = collection = Collection().extend
    # end


    # context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    # end
