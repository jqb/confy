# -*- coding: utf-8 -*-
import os

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
