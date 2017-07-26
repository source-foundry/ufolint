#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ufolint.data.tstobj import Result


def test_data_tstobj_result_class_instantiation_defaults():
    filepath = "testpath"
    res = Result(filepath)
    assert res.test_filepath == "testpath"
    assert res.test_failed is None
    assert res.test_long_stdstream_string == ""
