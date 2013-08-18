# -*- coding: utf-8 -*-
import os

from . import dictquery
from .utils import execfile


class BaseSource(object):
    pass


class ModuleSource(BaseSource):
    def __init__(self, names, silent=False):
        self.names = names
        self.silent = silent

    def _before_execfiles(self, context):
        return context

    def _execfile(self, absolute_path, context, silent=False):
        try:
            execfile(absolute_path, global_vars=context)
        except IOError:
            if not silent:
                raise
        return context

    def _after_execfile(self, context, module_name):
        return context

    def load(self, context):
        context = self._before_execfiles(context)

        for m in self.names:
            context = self._execfile(m, context, silent=self.silent)
            context = self._after_execfile(context, m)

        return context


class EnvironmentVariableSource(BaseSource):
    def __init__(self, names, silent=False, environ=None):
        self.names = names
        self.silent = silent
        self.environ = environ or os.environ

    def load(self, context):
        data = {}
        for vardef in self.names:
            if ":" in vardef:
                env_name, setting_name = vardef.split(":")
            else:
                env_name = setting_name = vardef
            try:
                data[setting_name] = self.environ[env_name]
            except KeyError:
                if not self.silent:
                    raise
        context.update(data)
        return context


class INISource(BaseSource):
    def __init__(self, names, sections=None, silent=False):
        self.names = names
        self.silent = silent
        self.sections = sections  # None means ALL

    def load(self, context):
        import configparser

        names = []
        for name in self.names:
            if not os.path.exists(name) and not self.silent:
                raise IOError("No such file or directory: '%s'" % name)
            names.append(name)

        cp = configparser.ConfigParser()
        cp.read(names)

        sections = self.sections or cp.sections()
        try:
            config_as_dict = dict([
                (section_name, dict(cp[section_name]))
                for section_name in sections
            ])
            context.update(config_as_dict)
        except KeyError:  # cp[<key>] raises KeyError not NoSectionError
            if not self.silent:
                raise

        return context


class EnvironmentDirectory(BaseSource):
    def __init__(self, names, silent=False):
        self.names = names
        self.silent = silent

    def _split_path(self, path):
        if path.startswith(os.sep):
            path = path[1:]
        if path.endswith(os.sep):
            path = path[:-1]
        return tuple(path.split(os.sep))

    def _build_composed_keys(self, dirpath):
        pjoin = os.path.join
        psplit = self._split_path

        composed_keys = []
        fullpaths = []

        for root, dirs, files in os.walk(dirpath):
            full_paths = [pjoin(root, filename) for filename in files]
            relative_paths = [
                path.replace(dirpath, '') for path in full_paths
            ]
            keys = [psplit(rpath) for rpath in relative_paths]
            composed_keys.extend(keys)
            fullpaths.extend(full_paths)

        return fullpaths, composed_keys

    def _read_vars(self, data, dirpath):
        fullpaths, composed_keys = self._build_composed_keys(dirpath)
        for fullpath, composed_key in zip(fullpaths, composed_keys):
            with open(fullpath, 'r') as f:
                value = str(f.read())
                dictquery.set(data, composed_key, value)
        return data

    def load(self, context):
        for dirpath in self.names:
            if not os.path.exists(dirpath) and not self.silent:
                raise IOError("No such directory: '%s'" % dirpath)
            else:
                context = self._read_vars(context, dirpath)

        return context
