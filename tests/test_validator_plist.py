#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

from ufolint.validators import plistvalidators
from ufolint.data.ufo import Ufo2, Ufo3

# ///////////////////////////////////////////////////////
#
#  CONSTANTS
#
# ///////////////////////////////////////////////////////

ufo2_dir_list = [['public.default', 'glyphs']]
ufo3_dir_list = [['public.default', 'glyphs'], ['glyphs.background', 'glyphs.public.background']]

ufo2_test_success_path = os.path.join('tests', 'testfiles', 'ufo', 'passes', 'UFO2-Pass.ufo')
ufo3_test_success_path = os.path.join('tests', 'testfiles', 'ufo', 'passes', 'UFO3-Pass.ufo')

metainfo_test_dir_failpath = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'metainfoPL')
fontinfo_test_dir_failpath = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'fontinfoPL')


# ///////////////////////////////////////////////////////
#
#  Abstract plist validator super class tests
#
# ///////////////////////////////////////////////////////


def test_validators_plist_abstractplist_ufo2_instantiation():
    abvalid = plistvalidators.AbstractPlistValidator(ufo2_test_success_path, 2, ufo2_dir_list)
    assert abvalid.ufopath == ufo2_test_success_path
    assert abvalid.ufoversion == 2
    assert abvalid.glyphs_dir_list == ufo2_dir_list
    assert abvalid.testfile is None
    assert isinstance(abvalid.ufoobj, Ufo2)
    assert abvalid.test_fail_list == []


def test_validators_plist_abstractplist_ufo3_instantiation():
    abvalid = plistvalidators.AbstractPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)
    assert abvalid.ufopath == ufo3_test_success_path
    assert abvalid.ufoversion == 3
    assert abvalid.glyphs_dir_list == ufo3_dir_list
    assert abvalid.testfile is None
    assert isinstance(abvalid.ufoobj, Ufo3)
    assert abvalid.test_fail_list == []


def test_validators_plist_abstractplist_ufo3_unimplemented_ufolib_import_method():
    with pytest.raises(NotImplementedError):
        abvalid = plistvalidators.AbstractPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)
        abvalid.run_ufolib_import_validation()


# ///////////////////////////////////////////////////////
#
#  metainfo.plist validator tests
#
# ///////////////////////////////////////////////////////


# Success tests

def test_validators_plist_ufo2_metainfo_successful_xml_ufolib_tests():
    meta_validator = plistvalidators.MetainfoPlistValidator(ufo2_test_success_path, 2, ufo2_dir_list)
    xml_test_fails = meta_validator.run_xml_validation()
    ufolib_test_fails = meta_validator.run_ufolib_import_validation()
    assert isinstance(xml_test_fails, list)
    assert isinstance(ufolib_test_fails, list)
    assert len(xml_test_fails) == 0
    assert len(ufolib_test_fails) == 0


def test_validators_plist_ufo3_metainfo_successful_xml_ufolib_tests():
    meta_validator = plistvalidators.MetainfoPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)
    xml_test_fails = meta_validator.run_xml_validation()
    ufolib_test_fails = meta_validator.run_ufolib_import_validation()
    assert isinstance(xml_test_fails, list)
    assert isinstance(ufolib_test_fails, list)
    assert len(xml_test_fails) == 0
    assert len(ufolib_test_fails) == 0


# Fail tests

def test_validators_plist_ufo2_metainfo_missing_file_fail(capsys):
    meta_missingfile_ufo_path = os.path.join(metainfo_test_dir_failpath, 'UFO2-MissingMeta.ufo')
    meta_validator = plistvalidators.MetainfoPlistValidator(meta_missingfile_ufo_path, 2, ufo2_dir_list)

    meta_validator.run_xml_validation()   # should not raise SystemExit

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fail_list = meta_validator.run_ufolib_import_validation()
        assert len(fail_list) == 0

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO2-MissingMeta.ufo' in out
    assert 'metainfo.plist' in out


def test_validators_plist_ufo3_metainfo_missing_file_fail(capsys):
    meta_missingfile_ufo_path = os.path.join(metainfo_test_dir_failpath, 'UFO3-MissingMeta.ufo')
    meta_validator = plistvalidators.MetainfoPlistValidator(meta_missingfile_ufo_path, 3, ufo3_dir_list)

    meta_validator.run_xml_validation()   # should not raise SystemExit

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fail_list = meta_validator.run_ufolib_import_validation()
        assert len(fail_list) == 0

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO3-MissingMeta.ufo' in out
    assert 'metainfo.plist' in out


def test_validators_plist_ufo2_metainfo_xml_fail(capsys):
    meta_ufo_path = os.path.join(metainfo_test_dir_failpath, 'UFO2-XMLmeta.ufo')
    meta_validator = plistvalidators.MetainfoPlistValidator(meta_ufo_path, 2, ufo2_dir_list)

    fail_list = meta_validator.run_xml_validation()

    assert len(fail_list) == 1
    assert 'metainfo.plist failed XML validation' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_metainfo_xml_fail(capsys):
    meta_ufo_path = os.path.join(metainfo_test_dir_failpath, 'UFO3-XMLmeta.ufo')
    meta_validator = plistvalidators.MetainfoPlistValidator(meta_ufo_path, 3, ufo3_dir_list)

    fail_list = meta_validator.run_xml_validation()

    assert len(fail_list) == 1
    assert 'metainfo.plist failed XML validation' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo2_metainfo_version_fail(capsys):
    meta_ufo_path = os.path.join(metainfo_test_dir_failpath, 'UFO2-VersionFail.ufo')
    meta_validator = plistvalidators.MetainfoPlistValidator(meta_ufo_path, 2, ufo2_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fail_list = meta_validator.run_ufolib_import_validation()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'metainfo.plist' in out


def test_validators_plist_ufo3_metainfo_version_fail(capsys):
    meta_ufo_path = os.path.join(metainfo_test_dir_failpath, 'UFO3-VersionFail.ufo')
    meta_validator = plistvalidators.MetainfoPlistValidator(meta_ufo_path, 3, ufo3_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fail_list = meta_validator.run_ufolib_import_validation()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'metainfo.plist' in out


# ///////////////////////////////////////////////////////
#
#  fontinfo.plist validator tests
#
# ///////////////////////////////////////////////////////

# Success tests

def test_validators_plist_ufo2_fontinfo_success():
    fontinfo_validator = plistvalidators.FontinfoPlistValidator(ufo2_test_success_path, 2, ufo2_dir_list)

    xml_fail_list = fontinfo_validator.run_xml_validation()
    ufolib_fail_list = fontinfo_validator.run_ufolib_import_validation()

    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_fontinfo_success():
    fontinfo_validator = plistvalidators.FontinfoPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)

    xml_fail_list = fontinfo_validator.run_xml_validation()
    ufolib_fail_list = fontinfo_validator.run_ufolib_import_validation()

    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


# Fail tests

def test_validators_plist_ufo2_fontinfo_missing_file_fail(capsys):
    fontinfo_ufo_path = os.path.join(fontinfo_test_dir_failpath, 'UFO2-MissingFI.ufo')
    fontinfo_validator = plistvalidators.FontinfoPlistValidator(fontinfo_ufo_path, 2, ufo2_dir_list)

    xml_fail_list = fontinfo_validator.run_xml_validation()
    ufolib_fail_list = fontinfo_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_fontinfo_missing_file_fail(capsys):
    fontinfo_ufo_path = os.path.join(fontinfo_test_dir_failpath, 'UFO3-MissingFI.ufo')
    fontinfo_validator = plistvalidators.FontinfoPlistValidator(fontinfo_ufo_path, 3, ufo3_dir_list)

    xml_fail_list = fontinfo_validator.run_xml_validation()
    ufolib_fail_list = fontinfo_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo2_fontinfo_xml_fail(capsys):
    fontinfo_ufo_path = os.path.join(fontinfo_test_dir_failpath, 'UFO2-XMLfi.ufo')
    fontinfo_validator = plistvalidators.FontinfoPlistValidator(fontinfo_ufo_path, 2, ufo2_dir_list)

    fail_list = fontinfo_validator.run_xml_validation()

    assert len(fail_list) == 1
    assert 'fontinfo.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_fontinfo_xml_fail(capsys):
    fontinfo_ufo_path = os.path.join(fontinfo_test_dir_failpath, 'UFO3-XMLfi.ufo')
    fontinfo_validator = plistvalidators.FontinfoPlistValidator(fontinfo_ufo_path, 3, ufo3_dir_list)

    fail_list = fontinfo_validator.run_xml_validation()

    assert len(fail_list) == 1
    assert 'fontinfo.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo2_fontinfo_ufolib_import_fail(capsys):
    fontinfo_ufo_path = os.path.join(fontinfo_test_dir_failpath, 'UFO2-UFOlibError.ufo')
    fontinfo_validator = plistvalidators.FontinfoPlistValidator(fontinfo_ufo_path, 2, ufo2_dir_list)

    fail_list = fontinfo_validator.run_ufolib_import_validation()

    assert len(fail_list) == 1
    assert 'fontinfo.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_fontinfo_ufolib_import_fail(capsys):
    fontinfo_ufo_path = os.path.join(fontinfo_test_dir_failpath, 'UFO3-UFOlibError.ufo')
    fontinfo_validator = plistvalidators.FontinfoPlistValidator(fontinfo_ufo_path, 3, ufo3_dir_list)

    fail_list = fontinfo_validator.run_ufolib_import_validation()

    assert len(fail_list) == 1
    assert 'fontinfo.plist' in fail_list[0].test_long_stdstream_string



