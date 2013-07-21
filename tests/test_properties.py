# -*- coding: utf-8 -*-
import unittest
import confy


class BaseProperty(unittest.TestCase):
    def setUp(self):
        self.property_class = confy.BaseProperty
        self.property = self.property_class()

    def test_get_should_raise_exception(self):
        self.assertRaises(NotImplementedError, self.property.get, None)  # instance == None

    def test_raw_value_should_raise_exception(self):
        try:
            self.property.raw_value
        except NotImplementedError:
            pass  # expected
        else:
            self.fail("BaseProperty.raw_value should raise NotImplementedError")

    def test_build_class_method_should_raise_exception(self):
        self.assertRaises(NotImplementedError, self.property_class.build, "name", "value")


class ValueProperty(unittest.TestCase):
    def setUp(self):
        self.property_class = confy.ValueProperty
        self.property_with_string = self.property_class("a value")
        self.property_with_int = self.property_class(25)

    def test_should_build_ValueProperty_instance_for_all_the_values_except_BaseProperty(self):
        prop, ok = self.property_class.build("name", "a value")
        assert ok == True
        assert prop.get(None) == self.property_with_string.get(None)
        assert prop.raw_value == self.property_with_string.raw_value

        prop, ok = self.property_class.build("name", 25)
        assert ok == True
        assert prop.get(None) == self.property_with_int.get(None)
        assert prop.raw_value == self.property_with_int.raw_value

        prop, ok = self.property_class.build("name", self.property_with_int)
        assert ok == True
        assert prop == self.property_with_int


class InterpolationProperty(unittest.TestCase):
    def setUp(self):
        self.property_class = confy.InterpolationProperty
        self.data = {
            "name": "John",
            "last_name": "Smith",
            "age": 31,
            "full_name": (lambda: "John Smith"),
        }
        self.name_property = self.property_class("name", "{name}", ["name"])
        self.last_name_property = self.property_class("last_name", "{last_name}", ["last_name"])
        self.age_property = self.property_class("age", "{age}", ["age"])
        self.full_name_property = self.property_class("full_name", "{full_name}", ["full_name"])
        self.full_data_property = self.property_class("full_data", "{name} {last_name}, {age}", [
            "name", "last_name", "age",
        ])

    def test_should_fetch_proper_value_from_data(self):
        assert self.name_property.get(self.data) == "John"
        assert self.last_name_property.get(self.data) == "Smith"
        assert self.age_property.get(self.data) == "31"  # yes, string is expected

    def test_raw_value_should_be_original_one(self):
        assert self.name_property.raw_value == "{name}"
        assert self.last_name_property.raw_value == "{last_name}"
        assert self.age_property.raw_value == "{age}"
        assert self.full_name_property.raw_value == "{full_name}"

    def test_callables_should_be_called(self):
        assert self.full_name_property.get(self.data) == "John Smith"

    def test_custom_properties_should_be_able_to_read_other_values(self):
        assert self.full_data_property.get(self.data) == "John Smith, 31"

    def test_classmethod_build_should_construct_property_from_the_given_string(self):
        prop, ok = self.property_class.build("full_data", "{name} {last_name}, {age}")
        assert ok == True
        assert self.full_data_property.get(self.data) == prop.get(self.data)
