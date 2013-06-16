# -*- coding: utf-8 -*-
import unittest
import confy


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

        eq = self.assertEqual
        eq(API.GET_OBJECT, 'http://api.veryfancy.com/get')
        eq(API.ADD_OBJECT, 'http://api.veryfancy.com/add')
        eq(API.REMOVE_OBJECT, 'http://api.veryfancy.com/remove')
