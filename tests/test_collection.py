# -*- coding: utf-8 -*-
import unittest
import confy

from nose.tools import (
    assert_equal as eq,
    assert_not_in,
    assert_in,
)


class CollectionTest(unittest.TestCase):
    def get_example_conf(self):
        FANCY_API_URL = confy.collection(
            root = 'http://fancy.com/api',
            GET_OBJECT = '{root}/get',
            ADD_OBJECT = '{root}/add',
            REMOVE_OBJECT = '{root}/remove',
        )
        return FANCY_API_URL

    def test_variable_interpolation_should_work_as_a_charm(self):
        API = self.get_example_conf()
        API.root = 'http://api.veryfancy.com'

        eq(API.GET_OBJECT, 'http://api.veryfancy.com/get')
        eq(API.ADD_OBJECT, 'http://api.veryfancy.com/add')
        eq(API.REMOVE_OBJECT, 'http://api.veryfancy.com/remove')



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
