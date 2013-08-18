# -*- coding: utf-8 -*-
import unittest
import confy


here = confy.utils.create_path_function(__file__)


class ModuleSourceTest(unittest.TestCase):
    def test_source_loads_on_demand_all_the_variables_from_given_modules(self):
        source = confy.sources.ModuleSource([
            here('tconf', 'data', 'base.py'),
            here('tconf', 'data', 'development.py'),
        ])

        expected_variables = set([  # all from tests/tconf/data/{base,development}.py
            'api_domain',
            'API_ADD',
            'API_DELETE',
            's3_assets_domain',
            'CONTENTURL',
            'SITECONTENTURL',
            'FAKE_BACKEND_CLASS',
            'DATABASE',
        ])

        ctx = source.load({
            'confy': confy,
        })
        ctx_variables = set((name for name in ctx.keys() if name not in [
            '__builtins__',
            'confy',
        ]))
        assert expected_variables == ctx_variables

    def test_unexisted_source_raises_error(self):
        source = confy.sources.ModuleSource([
            here('tconf', '_unexisted_', 'base.py'),
        ])
        self.assertRaises(IOError, source.load, {})

    def test_unexisted_source_do_not_raise_error_if_theres_silent_mode_on(self):
        source = confy.sources.ModuleSource([
            here('tconf', '_unexisted_', 'base.py'),
        ], silent=True)

        try:
            result = source.load({})
        except IOError:
            self.fail("No IOError exception should be raised")

        assert result == {}


class EnvironmentVariableSourceTest(unittest.TestCase):
    def setUp(self):
        self.environ = {
            'DB_NAME': 'dbname',
            'DB_HOST': 'dbhost',
            'DB_PASS': 'dbpass',
        }

        self.source = confy.sources.EnvironmentVariableSource([
            'DB_NAME', 'DB_HOST', 'DB_PASS',
        ], environ=self.environ)

    def test_should_read_exactly_pointed_variables(self):
        result = self.source.load({})
        assert result == self.environ

    def test_possible_to_rename_variables(self):
        source = confy.sources.EnvironmentVariableSource([
            'DB_NAME:DBN', 'DB_HOST:DBH', 'DB_PASS:DBP',
        ], environ=self.environ)

        result = source.load({})
        assert set(result.keys()) == set(['DBN', 'DBH', 'DBP'])

    def test_unexisted_variables_raises_error(self):
        source = confy.sources.EnvironmentVariableSource([
            '_ENEXISTED_',
        ], environ=self.environ)

        self.assertRaises(KeyError, source.load, {})

    def test_unexisted_variables_do_not_raises_error_for_silent_mode(self):
        source = confy.sources.EnvironmentVariableSource([
            '_ENEXISTED_',
        ], environ=self.environ, silent=True)

        try:
            result = source.load({})
        except KeyError:
            self.fail("No KeyError should be raised")

        assert result == {}


try:
    import configparser
except ImportError:
    configparser = None


if configparser:
    class INISourceTest(unittest.TestCase):
        def test_read_pointed_files(self):
            source = confy.sources.INISource([
                here('tconf', 'test.ini')
            ])

            result = source.load({})
            assert set(result.keys()) == set([
                'development', 'production',
            ])

        def test_reading_unexisted_file_raises_error(self):
            source = confy.sources.INISource([
                here('tconf', '_unexisted_.ini')
            ])
            self.assertRaises(IOError, source.load, {})

        def test_reading_section_that_not_exists_raise_error(self):
            source = confy.sources.INISource([
                here('tconf', 'test.ini')
            ], sections=['_unexisted_'])
            self.assertRaises(KeyError, source.load, {})

        def test_reading_section_that_not_exists_wont_raise_error_on_silent_mode(self):
            source = confy.sources.INISource([
                here('tconf', 'test.ini')
            ], sections=['_unexisted_'], silent=True)
            try:
                result = source.load({})
            except KeyError:
                self.fail("No KeyError should be raise here (silent is True)")

            assert result == {}


class EnvironmentDirectoryTest(unittest.TestCase):
    def test_read_pointed_directory(self):
        source = confy.sources.EnvironmentDirectory([
            here('tconf', 'envvars'),
        ])

        result = source.load({})
        assert result == {
            'DATABASE': {
                'NAME': 'testdb',
                'PASSWORD': 'test',
                'PORT': '9000',
                'testdata': {
                    'fixtures': 'testdata.json',
                },
                'USER': 'testuser',
            },
            'HELLO': 'world!',
        }

    def test_read_unexisted_directory_raises_error(self):
        source = confy.sources.EnvironmentDirectory([
            here('tconf', '_unexisted_vars_')
        ])
        self.assertRaises(IOError, source.load, {})

    def test_spliting_path_into_tuple_works_as_a_charm(self):
        source = confy.sources.EnvironmentDirectory([])
        assert source._split_path('hello/world') == ('hello', 'world')
        assert source._split_path('/hello/world') == ('hello', 'world')
        assert source._split_path('hello/world/') == ('hello', 'world')
        assert source._split_path('/hello/world/') == ('hello', 'world')
