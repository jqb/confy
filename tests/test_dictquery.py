# -*- coding: utf-8 -*-
import unittest

from confy import dictquery, Collection


class TestCase(unittest.TestCase):
    dict_implementation = None

    def get_data(self):
        data = {
            'DATABASE': {
                'ENGINE': 'tests.fake.backend.FakeBackend',
                'NAME': 'testdb',
                'USER': 'test',
                'PASSWORD': 'test',
                'HOST': 'test.db.com',
                'PORT': '9000',
                'testdata': {
                    'fixtures': 'testdata.json',
                },
            },
        }
        return self.dict_implementation(data)


# dictquery.get
class Get(TestCase):
    dict_implementation = dict

    def test_should_get_neasted_elements(self):
        fixtures = dictquery.get(self.get_data(), ['DATABASE', 'testdata', 'fixtures'])
        assert fixtures == 'testdata.json'

    def test_should_raise_key_error_when_key_does_not_exists(self):
        self.assertRaises(
            KeyError,
            dictquery.get, self.get_data(), ['DATABASE', '<non-existing>', 'fixtures'])


class CollectionGet(Get):
    dict_implementation = Collection
# end / dictquery.get


# dictquery.set
class Set(TestCase):
    dict_implementation = dict

    def test_should_set_neasted_elements(self):
        data = self.get_data()
        dictquery.set(data, ['DATABASE', 'testdata', 'fixtures'], 'other.json')

        fixtures = data['DATABASE']['testdata']['fixtures']
        assert fixtures == 'other.json'

    def test_should_fill_not_existed_keys(self):
        data = self.get_data()
        assert 'SLAVE' not in data['DATABASE']

        impl = self.dict_implementation
        dictquery.set(data, ['DATABASE', 'SLAVE', 'PORT'], 9999, dictfactory=impl)

        assert 'SLAVE' in data['DATABASE']
        assert 'PORT' in data['DATABASE']['SLAVE']
        assert data['DATABASE']['SLAVE']['PORT'] == 9999


class CollectionSet(Set):
    dict_implementation = Collection
# end / dictquery.set


# dictquery.keys
class Keys(TestCase):
    dict_implementation = dict

    def assure_keys(self, patterns, expected_keys):
        data = self.get_data()
        keys = dictquery.keys(data, patterns)
        assert set(keys) == set(expected_keys)

    def test_should_return_all_paths_for_given_composed_keys_patterns(self):
        self.assure_keys([
            ("DA*",),
        ], [
            ('DATABASE', 'testdata', 'fixtures'),
            ('DATABASE', 'NAME'),
            ('DATABASE', 'USER'),
            ('DATABASE', 'HOST'),
            ('DATABASE', 'PASSWORD'),
            ('DATABASE', 'ENGINE'),
            ('DATABASE', 'PORT'),
        ])

        self.assure_keys([
            ("DA*", "EN*"),
        ], [
            ('DATABASE', 'ENGINE'),
        ])

        self.assure_keys([
            ("DA*", "test*", "fix*"),
        ], [
            ('DATABASE', 'testdata', 'fixtures'),
        ])

        self.assure_keys([
            ("DA*", "test*", "fix*"),
            ("DA*", "PASS*"),

        ], [
            ('DATABASE', 'testdata', 'fixtures'),
            ('DATABASE', 'PASSWORD'),
        ])


class CollectionKeys(Keys):
    dict_implementation = Collection.collectionize
# end / dictquery.keys


# dictquery.query
class Query(TestCase):
    dict_implementation = dict

    def assure_result(self, patterns, expected):
        data = self.get_data()
        values = dictquery.query(data, patterns)
        assert set(values) == set(expected)

    def test_should_return_all_paths_and_values_for_given_composed_keys_patterns(self):
        self.assure_result([
            ("DA*",),
        ], [
            (('DATABASE', 'testdata', 'fixtures'), 'testdata.json'),
            (('DATABASE', 'NAME'), 'testdb'),
            (('DATABASE', 'USER'), 'test'),
            (('DATABASE', 'HOST'), 'test.db.com'),
            (('DATABASE', 'PASSWORD'), 'test'),
            (('DATABASE', 'ENGINE'), 'tests.fake.backend.FakeBackend'),
            (('DATABASE', 'PORT'), '9000'),
        ])

        self.assure_result([
            ("DA*", "EN*"),
        ], [
            (('DATABASE', 'ENGINE'), 'tests.fake.backend.FakeBackend'),
        ])

        self.assure_result([
            ("DA*", "test*", "fix*"),
        ], [
            (('DATABASE', 'testdata', 'fixtures'), 'testdata.json'),
        ])

        self.assure_result([
            ("DA*", "test*", "fix*"),
            ("DA*", "PASS*"),

        ], [
            (('DATABASE', 'testdata', 'fixtures'), 'testdata.json'),
            (('DATABASE', 'PASSWORD'), 'test'),
        ])


class CollectionQuery(Keys):
    dict_implementation = Collection.collectionize
# end / dictquery.query
