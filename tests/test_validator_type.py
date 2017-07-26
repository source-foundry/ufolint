#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from ufolint.validators.typevalidators import is_float_type, is_int_type, is_float_in_a_string
from ufolint.validators.typevalidators import is_int_in_a_string, is_int_or_float_type, is_string_type, is_list_type


def test_typevalidator_is_float_type_true():
    assert is_float_type(9.121) is True


def test_typevalidator_is_float_type_false():
    assert is_float_type("test") is False


def test_typevalidator_is_int_type_true():
    assert is_int_type(6) is True


def test_typevalidator_is_int_type_false():
    assert is_int_type("test") is False


def test_typevalidator_is_float_in_a_string_true():
    assert is_float_in_a_string("9.141") is True


def test_typevalidator_is_float_in_a_string_false():
    assert is_float_in_a_string("sixteen") is False


def test_typevalidator_is_int_in_a_string_true():
    assert is_int_in_a_string("6") is True


def test_typevalidator_is_int_in_a_string_false():
    assert is_int_in_a_string("test") is False


def test_typevalidator_is_int_or_float_type_true():
    assert is_int_or_float_type(6) is True
    assert is_int_or_float_type(9.1423) is True


def test_typevalidator_is_int_or_float_type_false():
    assert is_int_or_float_type("test") is False


def test_typevalidator_is_string_type_true():
    assert is_string_type("test") is True


def test_typevalidator_is_string_type_false():
    assert is_string_type(9) is False


def test_typevalidator_is_list_type_true():
    assert is_list_type([1, 2, 3]) is True


def test_typevalidator_is_list_type_false():
    assert is_list_type("testing") is False