#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from ufolint.settings import major_version, minor_version, patch_version, HELP, VERSION, USAGE


def test_settings_version_major():
    assert isinstance(int(major_version), int) is True


def test_settings_version_minor():
    assert isinstance(int(minor_version), int) is True


def test_settings_patch_version():
    assert isinstance(int(patch_version), int) is True


def test_settings_help_string():
    assert isinstance(HELP, str) is True
    assert HELP[0:4] == "===="


def test_settings_version_string():
    assert isinstance(VERSION, str)
    assert VERSION[0:4] == "ufol"


def test_settings_usage_string():
    assert isinstance(USAGE, str)
    assert USAGE[0:4] == "ufol"

