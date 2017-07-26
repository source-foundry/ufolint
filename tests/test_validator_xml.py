#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest

try:  # pragma: no cover
    import xml.etree.cElementTree as Etree            # python 2
except ImportError:  # pragma: no cover
    import xml.etree.ElementTree as Etree             # python 3

from ufolint.validators.xmlvalidators import is_valid_xml_path


def test_validators_xml_is_valid_xml_pass():
    test_path = os.path.join('tests', 'testfiles', 'xml', 'validxml.plist')
    res = is_valid_xml_path(test_path)
    assert res[0] is True
    assert isinstance(res[1], Etree.ElementTree) is True


def test_validators_xml_is_valid_xml_fail():
    test_path = os.path.join('tests', 'testfiles', 'xml', 'invalidxml.plist')
    res = is_valid_xml_path(test_path)
    assert res[0] is False
    assert len(res[1]) > 0    # test for a string from the exception message raised by ElementTree.parse()
