# -*- coding: utf-8 -*-
import unittest
import confy

from nose.tools import (
    assert_equal as eq,
    assert_not_in,
    assert_in,
)


class CollectionFeatures(unittest.TestCase):
    def setUp(self):
        self.settings = confy.collection(
            API = confy.collection(
                root = 'http://fancy.com/api',
                GET_OBJECT = '{root}/get',
                ADD_OBJECT = '{root}/add',
                REMOVE_OBJECT = '{root}/remove',
            ),
            FAKE_BACKEND_CLASS = confy.lazyimport('tests.fake.backend.FakeBackend'),
            FAKE_BACKEND_MODULE = confy.lazyimport('tests.fake.backend'),
            RAW_VALUE = confy.raw('{with "raw" I can put {} as many special things as I want}'),
            URLS = confy.lazy(lambda self: "%s %s" % (self.API.GET_OBJECT, self.API.ADD_OBJECT))
        )

    def test_variable_interpolation_should_work_as_a_charm(self):
        API = self.settings.API
        API.root = 'http://api.veryfancy.com'

        eq(API.GET_OBJECT, 'http://api.veryfancy.com/get')
        eq(API.ADD_OBJECT, 'http://api.veryfancy.com/add')
        eq(API.REMOVE_OBJECT, 'http://api.veryfancy.com/remove')

    def test_lazyimport(self):
        from tests.fake.backend import FakeBackend
        eq(self.settings.FAKE_BACKEND_CLASS, FakeBackend)

    def test_lazyimport_module(self):
        from tests.fake import backend
        eq(self.settings.FAKE_BACKEND_MODULE, backend)

    def test_raw(self):
        eq(self.settings.RAW_VALUE, '{with "raw" I can put {} as many special things as I want}')

    def test_lazy_evaluation_should_work_as_a_charm(self):
        api = self.settings.API
        eq(self.settings.URLS, "%s %s" % (api.GET_OBJECT, api.ADD_OBJECT))


class CollectionDict(unittest.TestCase):
    def setUp(self):
        self.collection = confy.collection(
            protocol = "http",
            URL = "{protocol}://something.com",
        )

    def test__contains__should_work_as_expected(self):
        value = self.collection.get('URL')
        eq(value, 'http://something.com')
        assert_in('URL', self.collection)

        value = self.collection.pop('URL')
        eq(value, 'http://something.com')
        assert_not_in('URL', self.collection)

    def test_pop_should_return_value_not_property(self):
        value = self.collection.pop('URL')
        eq(value, 'http://something.com')
        assert_not_in('URL', self.collection)

    def test_keys(self):
        current = set(self.collection.keys())
        expected = {'protocol', 'URL'}
        eq(current, expected)

    def test_values(self):
        current = set(self.collection.values())
        expected = {'http', 'http://something.com'}
        eq(current, expected)

    def test__eq__(self):
        assert self.collection == dict(self.collection)
