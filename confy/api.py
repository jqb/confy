# -*- coding: utf-8 -*-
import os

from .utils import flatten, create_path_function, extrabuiltins, syspath, execfile, Importer
from .collection import Collection, Raw


class Loader(object):
    conf_config_extention = 'py'
    conf_global_confy_object_name = 'confy'

    Collection = Collection
    lazyimport = Importer
    raw = Raw


    def __init__(self, file=None, syspaths=None, config_extention=None):
        self._file = file
        self._syspaths = syspaths or ['.']
        self.pathjoin = os.path.join
        self.conf_config_extention = config_extention or self.__class__.conf_config_extention

        if self._file:
            self.from_config_root = create_path_function(self._file)
        else:
            self.from_config_root = None

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
        if not self.from_config_root:
            return []
        return [self.from_config_root(*s.split(os.sep)) for s in syspaths]

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

    def _execfile(self, relative_path, context):
        execfile(self.from_config_root(relative_path), global_vars=context)
        return context

    def _after_execfile(self, context, module_names):
        if 'MODE' not in context:
            context.update(MODE=module_names[-1])
        return context

    def _merge_modules(self, *things, **kwargs):
        syspaths = self._get_syspath(kwargs.get('syspath'))
        extras = self._get_extrabuildins(kwargs.get('extrabuiltins'))
        config_extention = self._get_config_extention(kwargs.get('config_extention'))

        with syspath(syspaths):
            with extrabuiltins(extras):
                attributes = self._before_execfiles({})

                module_names = flatten(things, flat_only=[list, tuple])
                for m in module_names:
                    attributes = self._execfile('%s%s' % (m, config_extention), attributes)

                attributes = self._after_execfile(attributes, module_names)

        return attributes
    # end


    # api
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

    @classmethod
    def env(cls, name, default=None, environ=None):
        environ = environ or os.environ
        return environ.get(name, default)

    new = collection = Collection.extend
    # end


    # context manager support
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    # end
