# -*- coding: utf-8 -*-
import unittest
import confy


class NonMapping(object):
    def __init__(self):
        self._data = {
            'key': 'value',
        }

    def keys(self):
        return self._data.keys()

    def __getitem__(self, name):
        return self._data[name]


class CollectionFeatures(unittest.TestCase):
    def setUp(self):
        self.settings = confy.collection._new(dict(
            API = confy.collection(
                root = 'http://fancy.com/api',
                GET_OBJECT = '{root}/get',
                ADD_OBJECT = '{root}/add',
                REMOVE_OBJECT = '{root}/remove',
                UNEXISTED_VARIABLE = '{unexisted}/hello!'
            ),
            FAKE_BACKEND_CLASS = confy.lazyimport('tests.fake.backend.FakeBackend'),
            FAKE_BACKEND_MODULE = confy.lazyimport('tests.fake.backend'),
            RAW_VALUE = confy.raw('{with "raw" I can put {} as many special things as I want}'),
            URLS = confy.lazy(lambda self: "%s %s" % (self.API.GET_OBJECT, self.API.ADD_OBJECT)),
            PROJECT_ROOT = confy.rootpath('..'),
        ), private={
            # confy.rootpath stuff won't work without __rootpath__ private variable
            '__rootpath__': '/path/to/project/settings/__init__.py',
        })

    def test_variable_interpolation_should_work_as_a_charm(self):
        API = self.settings.API
        API.root = 'http://api.veryfancy.com'

        assert API.GET_OBJECT == 'http://api.veryfancy.com/get'
        assert API.ADD_OBJECT == 'http://api.veryfancy.com/add'
        assert API.REMOVE_OBJECT == 'http://api.veryfancy.com/remove'

    def test_interpolation_for_variable_that_does_not_exists_raises_key_error(self):
        self.assertRaises(KeyError, lambda: self.settings.API.UNEXISTED_VARIABLE)

    def test_lazyimport(self):
        from tests.fake.backend import FakeBackend
        assert self.settings.FAKE_BACKEND_CLASS == FakeBackend

    def test_lazyimport_module(self):
        from tests.fake import backend
        assert self.settings.FAKE_BACKEND_MODULE == backend

    def test_raw(self):
        assert self.settings.RAW_VALUE == '{with "raw" I can put {} as many special things as I want}'

    def test_lazy_evaluation_should_work_as_a_charm(self):
        api = self.settings.API
        assert self.settings.URLS == "%s %s" % (api.GET_OBJECT, api.ADD_OBJECT)

    def test_rootpath_constructs_relatively_correct_paths(self):
        assert self.settings.PROJECT_ROOT == '/path/to/project'

    def test_collectionize(self):
        testdict = {
            'DATABASE': {
                'ENGINE': confy.lazyimport('tests.fake.backend.FakeBackend'),
                'NAME': 'testdb',
                'USER': 'test',
                'PASSWORD': 'test',
                'HOST': 'test.db.com',
                'PORT': '9000',

                'testdata': confy.collection({
                    'fixtures': confy.rootpath('..', 'fixtures', 'testdata.json')
                }),
            },
            'HELLO': 'world',
        }

        private = {
            '__rootpath__': '/path/to/project/settings/__init__.py',
        }
        result = confy.Collection.collectionize(testdict, private=private)

        assert isinstance(result.DATABASE, confy.Collection)
        assert isinstance(result.DATABASE.testdata, confy.Collection)

        private_name = confy.utils.private_attribute_name(confy.Collection, 'private')
        assert getattr(result.DATABASE, private_name) == private
        assert getattr(result.DATABASE.testdata, private_name) == private

        assert result.DATABASE.testdata.fixtures == '/path/to/project/fixtures/testdata.json'


class CollectionDict(unittest.TestCase):
    def setUp(self):
        self.collection = confy.collection(
            protocol = "http",
            URL = "{protocol}://something.com",
        )

    def test__contains__should_work_as_expected(self):
        value = self.collection.get('URL')
        assert value == 'http://something.com'
        assert 'URL' in self.collection

        value = self.collection.pop('URL')
        assert value == 'http://something.com'
        assert 'URL' not in self.collection

    def test_pop_should_return_value_not_property(self):
        value = self.collection.pop('URL')
        assert value == 'http://something.com'
        assert 'URL' not in self.collection

    def test_pop_should_raise_key_error(self):
        self.assertRaises(KeyError, self.collection.pop, 'unexisted')

    def test_popitem_should_return_name_with_value_tuple(self):
        name, value = self.collection.popitem()
        assert name not in self.collection

    def test_popitem_raises_error_then_collection_is_empty(self):
        self.collection.clear()
        self.assertRaises(KeyError, self.collection.popitem)

    def test_keys(self):
        current = set(self.collection.keys())
        expected = set(['protocol', 'URL'])
        assert current == expected

    def test_values(self):
        current = set(self.collection.values())
        expected = set(['http', 'http://something.com'])
        assert current == expected

    def test__eq__(self):
        assert self.collection == dict(self.collection)
        assert self.collection.__eq__(NonMapping()) == False

    def test__ne__(self):
        data = dict(self.collection)
        assert self.collection == data

        data['protocol'] = 'https'
        assert self.collection != data

    def test_update_takes_exactly_1_postional_arguments(self):
        self.assertRaises(TypeError, self.collection.update, {}, {})  # except self!

        try:
            self.collection.update({
                'key': 'value',
            })
        except TypeError:
            self.fail("Update should work with just one positional argument")

    def test_update_that_runs_on_class_complains_about_on_arguments(self):
        self.assertRaises(TypeError, confy.collection.update)

    def test_update_works_also_with_non_mappings_and_iterables_of_tuples(self):
        assert 'key' not in self.collection
        self.collection.update(NonMapping())
        assert 'key' in self.collection

        assert 'key2' not in self.collection
        self.collection.update([('key2', 'value2')])
        assert 'key2' in self.collection

    def test_setdefault(self):
        assert 'protocol' in self.collection
        result = self.collection.setdefault('protocol', 'value')
        assert result == 'http'
        assert 'protocol' in self.collection

        assert 'unexisted' not in self.collection
        result = self.collection.setdefault('unexisted', 'value')
        assert result == 'value'
        assert 'unexisted' in self.collection

    def test_iterkeys(self):
        assert list(self.collection.keys()) == list(self.collection.iterkeys())

    def test_deleting_item(self):
        del self.collection['protocol']
        assert 'protocol' not in self.collection

    def test_get(self):
        assert 'key' not in self.collection
        result = self.collection.get('key')
        assert result is None

        result = self.collection.get('key', 'default')
        assert result == 'default'

    def test_itervalues(self):
        assert list(self.collection.values()) == list(self.collection.itervalues())

    def test_iteritems(self):
        assert list(self.collection.items()) == list(self.collection.iteritems())

    def test_properties(self):
        assert len(self.collection.properties()) == 2

    def test_extend(self):
        result = self.collection.extend({
            'key': 'value'
        })
        assert result != self.collection
        assert 'key' in result

    def test_raw(self):  # returns raw value
        raw_value = self.collection.raw('URL')
        assert raw_value == '{protocol}://something.com'

    def test_raw_items(self):
        raw_items = self.collection.raw_items()
        assert len(raw_items) == 2

        keys = set()
        values = set()
        for name, raw_value in raw_items:
            keys.add(name)
            values.add(raw_value)

        expected_keys = set([
            'protocol', 'URL'
        ])
        assert expected_keys == keys

        expected_values = set([
            'http', '{protocol}://something.com'
        ])
        assert expected_values == values

    def test_raw_values(self):
        expected_values = set([
            'http', '{protocol}://something.com'
        ])
        assert expected_values == set(self.collection.raw_values())

    def test_setitem(self):
        self.collection['hello'] = 'world'
        assert self.collection.hello == 'world'
        assert 'world' in self.collection.values()

    def test_str_repr_unicode_returns_the_same(self):
        str_ = self.collection.__str__()
        repr_ = self.collection.__repr__()
        unicode_ = self.collection.__unicode__()
        assert str_ == repr_ == unicode_

        expected = "<Collection: %s>" % list(self.collection.keys())
        assert str_ == expected

    def test_collection_might_be_treated_as_source_too(self):
        context = self.collection.load({})
        assert context['protocol'] == 'http'
        assert context['URL'] == 'http://something.com'


class CollectionModule(unittest.TestCase):
    def setUp(self):
        self.collection = confy.collection(
            protocol = "http",
            URL = "{protocol}://something.com",
        )
        self.module = confy.Module('settings', 'unexisted/settings/__init__.pyc', self.collection)

    def test_supports_getitem_protocol(self):
        assert self.module['protocol'] == 'http'
