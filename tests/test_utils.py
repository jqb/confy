# -*- coding: utf-8 -*-
import unittest
from confy.utils import (
    smart_ext, split_filenames, create_path_function, Importer,
    extrabuiltins, syspath
)


class UtilsTest(unittest.TestCase):
    def test_smart_ext(self):
        assert smart_ext("config") == "config"
        assert smart_ext("config.py") == "config.py"

        # forcing ext only if file name does not contain ext
        assert smart_ext("config", ext="py") == "config.py"
        assert smart_ext("config", ext="ini") == "config.ini"

        # should be smart enough if someobdy will pass "." dots in ext
        assert smart_ext("config", ext=".py") == "config.py"
        assert smart_ext("config", ext=".ini") == "config.ini"

        assert smart_ext("config.py", ext="py") == "config.py"
        assert smart_ext("config.py", ext="ini") == "config.py"

    def test_create_path_function(self):
        rootpath = create_path_function('/path/to/project/_.in')
        assert rootpath() == '/path/to/project'
        assert rootpath('..') == '/path/to'
        assert rootpath('somedata') == '/path/to/project/somedata'

    def test_split_filenames(self):
        names = ['base,development', 'production,local']
        result = split_filenames(names)

        assert result == ['base', 'development', 'production', 'local']

        result = split_filenames(names, ext='py')
        assert result == ['base.py', 'development.py', 'production.py', 'local.py']


class ImporterTest(unittest.TestCase):
    def test_importing_module(self):
        importer = Importer('tests')
        module = importer.import_it()

        import tests as m
        assert module == m
        assert module.fake.backend == m.fake.backend

    def test_importing_class(self):
        importer = Importer('tests.fake.backend.FakeBackend')
        item = importer.import_it()

        from tests.fake.backend import FakeBackend
        assert item == FakeBackend

    def test_not_existing_module(self):
        importer = Importer('_nonexisting_')
        self.assertRaises(ImportError, importer.import_it)

    def test_not_existing_item(self):
        importer = Importer('tests._nonexisting_')
        self.assertRaises(ImportError, importer.import_it)

    def test_imported_item_is_cached(self):
        importer = Importer('tests.fake.backend.FakeBackend')
        class_ = importer.import_it()
        assert importer._Importer__importeditem == class_

        class2 = importer.import_it()
        assert class_ == class2
        assert class_ is class2


class ExtrabuiltinsTest(unittest.TestCase):
    def test_as_contextmanager(self):
        class Builtins(object):
            pass

        builtins = Builtins()  # fake builtins just for test

        extras = extrabuiltins({'hello': 'world'}, builtins=builtins)
        with extras:
            assert 'hello' in dir(builtins)

        assert 'hello' not in dir(builtins)


class SyspathTest(unittest.TestCase):
    def test_as_contextmanager(self):
        fake_syspath = []  # fake one - just for test

        extras = syspath(['/path/to/lib'], sys_path=fake_syspath)
        with extras:
            assert '/path/to/lib' in fake_syspath

        assert '/path/to/lib' not in fake_syspath
