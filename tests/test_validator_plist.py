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
groups_test_dir_failpath = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'groupsPL')
kerning_test_dir_failpath = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'kerningPL')
lib_test_dir_failpath = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'libPL')
contents_test_dir_failpath = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'contentsPL')
layercontents_test_dir_failpath = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'layercontentsPL')
layerinfo_test_dir_failpath = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'layerinfoPL')

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

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fail_list = meta_validator.run_xml_validation()

        assert len(fail_list) == 1
        assert 'metainfo.plist failed XML validation' in fail_list[0].test_long_stdstream_string
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO2-XMLmeta.ufo' in out
    assert 'metainfo.plist' in out


def test_validators_plist_ufo3_metainfo_xml_fail(capsys):
    meta_ufo_path = os.path.join(metainfo_test_dir_failpath, 'UFO3-XMLmeta.ufo')
    meta_validator = plistvalidators.MetainfoPlistValidator(meta_ufo_path, 3, ufo3_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fail_list = meta_validator.run_xml_validation()

        assert len(fail_list) == 1
        assert 'metainfo.plist failed XML validation' in fail_list[0].test_long_stdstream_string
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO3-XMLmeta.ufo' in out
    assert 'metainfo.plist' in out


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


# ///////////////////////////////////////////////////////
#
#  groups.plist validator tests
#
# ///////////////////////////////////////////////////////


# Success tests

def test_validators_plist_ufo2_groups_success():
    groups_validator = plistvalidators.GroupsPlistValidator(ufo2_test_success_path, 2, ufo2_dir_list)

    xml_fail_list = groups_validator.run_xml_validation()
    ufolib_fail_list = groups_validator.run_ufolib_import_validation()

    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_groups_success():
    groups_validator = plistvalidators.GroupsPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)

    xml_fail_list = groups_validator.run_xml_validation()
    ufolib_fail_list = groups_validator.run_ufolib_import_validation()

    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


# Fail tests

def test_validators_plist_ufo2_groups_missing_file_fail():
    groups_ufo_path = os.path.join(groups_test_dir_failpath, 'UFO2-MissingGroups.ufo')
    groups_validator = plistvalidators.GroupsPlistValidator(groups_ufo_path, 2, ufo2_dir_list)

    xml_fail_list = groups_validator.run_xml_validation()
    ufolib_fail_list = groups_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_groups_missing_file_fail():
    groups_ufo_path = os.path.join(groups_test_dir_failpath, 'UFO3-MissingGroups.ufo')
    groups_validator = plistvalidators.GroupsPlistValidator(groups_ufo_path, 3, ufo3_dir_list)

    xml_fail_list = groups_validator.run_xml_validation()
    ufolib_fail_list = groups_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo2_groups_xml_fail():
    groups_ufo_path = os.path.join(groups_test_dir_failpath, 'UFO2-XMLgr.ufo')
    groups_validator = plistvalidators.GroupsPlistValidator(groups_ufo_path, 2, ufo2_dir_list)

    fail_list = groups_validator.run_xml_validation()

    assert len(fail_list) == 1
    assert 'groups.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_groups_xml_fail():
    groups_ufo_path = os.path.join(groups_test_dir_failpath, 'UFO3-XMLgr.ufo')
    groups_validator = plistvalidators.GroupsPlistValidator(groups_ufo_path, 3, ufo3_dir_list)

    fail_list = groups_validator.run_xml_validation()

    assert len(fail_list) == 1
    assert 'groups.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo2_groups_ufo_import_fail():
    groups_ufo_path = os.path.join(groups_test_dir_failpath, 'UFO2-UFOlibError.ufo')
    groups_validator = plistvalidators.GroupsPlistValidator(groups_ufo_path, 2, ufo2_dir_list)

    fail_list = groups_validator.run_ufolib_import_validation()

    assert len(fail_list) == 1
    assert 'groups.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_groups_ufo_import_fail():
    groups_ufo_path = os.path.join(groups_test_dir_failpath, 'UFO3-UFOlibError.ufo')
    groups_validator = plistvalidators.GroupsPlistValidator(groups_ufo_path, 3, ufo3_dir_list)

    fail_list = groups_validator.run_ufolib_import_validation()

    assert len(fail_list) == 1
    assert 'groups.plist' in fail_list[0].test_long_stdstream_string


# ///////////////////////////////////////////////////////
#
#  kerning.plist validator tests
#
# ///////////////////////////////////////////////////////


# Success tests

def test_validators_plist_ufo2_kerning_success():
    kerning_validator = plistvalidators.KerningPlistValidator(ufo2_test_success_path, 2, ufo2_dir_list)

    xml_fail_list = kerning_validator.run_xml_validation()
    ufolib_fail_list = kerning_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_kerning_success():
    kerning_validator = plistvalidators.KerningPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)

    xml_fail_list = kerning_validator.run_xml_validation()
    ufolib_fail_list = kerning_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


# Fail tests

def test_validators_plist_ufo2_kerning_missing_file_fail():
    kerning_ufo_path = os.path.join(kerning_test_dir_failpath, 'UFO2-MissingKern.ufo')
    kerning_validator = plistvalidators.KerningPlistValidator(kerning_ufo_path, 2, ufo2_dir_list)

    xml_fail_list = kerning_validator.run_xml_validation()
    ufolib_fail_list = kerning_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_kerning_missing_file_fail():
    kerning_ufo_path = os.path.join(kerning_test_dir_failpath, 'UFO3-MissingKern.ufo')
    kerning_validator = plistvalidators.KerningPlistValidator(kerning_ufo_path, 3, ufo3_dir_list)

    xml_fail_list = kerning_validator.run_xml_validation()
    ufolib_fail_list = kerning_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo2_kerning_xml_fail():
    kerning_ufo_path = os.path.join(kerning_test_dir_failpath, 'UFO2-XMLkern.ufo')
    kerning_validator = plistvalidators.KerningPlistValidator(kerning_ufo_path, 2, ufo2_dir_list)

    xml_fail_list = kerning_validator.run_xml_validation()

    assert isinstance(xml_fail_list, list)
    assert len(xml_fail_list) == 1
    assert 'kerning.plist' in xml_fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_kerning_xml_fail():
    kerning_ufo_path = os.path.join(kerning_test_dir_failpath, 'UFO3-XMLkern.ufo')
    kerning_validator = plistvalidators.KerningPlistValidator(kerning_ufo_path, 3, ufo3_dir_list)

    xml_fail_list = kerning_validator.run_xml_validation()

    assert isinstance(xml_fail_list, list)
    assert len(xml_fail_list) == 1
    assert 'kerning.plist' in xml_fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo2_kerning_ufo_import_fail():
    kerning_ufo_path = os.path.join(kerning_test_dir_failpath, 'UFO2-UFOlibError.ufo')
    kerning_validator = plistvalidators.KerningPlistValidator(kerning_ufo_path, 2, ufo2_dir_list)

    fail_list = kerning_validator.run_ufolib_import_validation()

    assert isinstance(fail_list, list)
    assert len(fail_list) == 1
    assert 'kerning.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_kerning_ufo_import_fail():
    kerning_ufo_path = os.path.join(kerning_test_dir_failpath, 'UFO3-UFOlibError.ufo')
    kerning_validator = plistvalidators.KerningPlistValidator(kerning_ufo_path, 3, ufo3_dir_list)

    fail_list = kerning_validator.run_ufolib_import_validation()

    assert isinstance(fail_list, list)
    assert len(fail_list) == 1
    assert 'kerning.plist' in fail_list[0].test_long_stdstream_string


# ///////////////////////////////////////////////////////
#
#  lib.plist validator tests
#
# ///////////////////////////////////////////////////////

# Success tests

def test_validators_plist_ufo2_lib_success():
    lib_validator = plistvalidators.LibPlistValidator(ufo2_test_success_path, 2, ufo2_dir_list)

    xml_fail_list = lib_validator.run_xml_validation()
    ufolib_fail_list = lib_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_lib_success():
    lib_validator = plistvalidators.LibPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)

    xml_fail_list = lib_validator.run_xml_validation()
    ufolib_fail_list = lib_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


# Fail tests

def test_validators_plist_ufo2_lib_missing_file_fail():
    lib_ufo_path = os.path.join(lib_test_dir_failpath, 'UFO2-MissingLib.ufo')
    lib_validator = plistvalidators.LibPlistValidator(lib_ufo_path, 2, ufo2_dir_list)

    xml_fail_list = lib_validator.run_xml_validation()
    ufolib_fail_list = lib_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_lib_missing_file_fail():
    lib_ufo_path = os.path.join(lib_test_dir_failpath, 'UFO3-MissingLib.ufo')
    lib_validator = plistvalidators.LibPlistValidator(lib_ufo_path, 3, ufo3_dir_list)

    xml_fail_list = lib_validator.run_xml_validation()
    ufolib_fail_list = lib_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo2_lib_xml_fail():
    lib_ufo_path = os.path.join(lib_test_dir_failpath, 'UFO2-XMLlib.ufo')
    lib_validator = plistvalidators.LibPlistValidator(lib_ufo_path, 2, ufo2_dir_list)

    fail_list = lib_validator.run_xml_validation()

    assert isinstance(fail_list, list)
    assert len(fail_list) == 1
    assert 'lib.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_lib_xml_fail():
    lib_ufo_path = os.path.join(lib_test_dir_failpath, 'UFO3-XMLlib.ufo')
    lib_validator = plistvalidators.LibPlistValidator(lib_ufo_path, 3, ufo3_dir_list)

    fail_list = lib_validator.run_xml_validation()

    assert isinstance(fail_list, list)
    assert len(fail_list) == 1
    assert 'lib.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo2_lib_ufolib_import_fail():
    lib_ufo_path = os.path.join(lib_test_dir_failpath, 'UFO2-UFOlibError.ufo')
    lib_validator = plistvalidators.LibPlistValidator(lib_ufo_path, 2, ufo2_dir_list)

    fail_list = lib_validator.run_ufolib_import_validation()

    assert isinstance(fail_list, list)
    assert len(fail_list) == 1
    assert 'lib.plist' in fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_lib_ufolib_import_fail():
    lib_ufo_path = os.path.join(lib_test_dir_failpath, 'UFO3-UFOlibError.ufo')
    lib_validator = plistvalidators.LibPlistValidator(lib_ufo_path, 3, ufo3_dir_list)

    fail_list = lib_validator.run_ufolib_import_validation()

    assert isinstance(fail_list, list)
    assert len(fail_list) == 1
    assert 'lib.plist' in fail_list[0].test_long_stdstream_string


# ///////////////////////////////////////////////////////
#
#  contents.plist validator tests
#
# ///////////////////////////////////////////////////////

# Success tests

def test_validators_plist_ufo2_contents_success():
    lib_validator = plistvalidators.ContentsPlistValidator(ufo2_test_success_path, 2, ufo2_dir_list)

    xml_fail_list = lib_validator.run_xml_validation()
    ufolib_fail_list = lib_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_contents_success():
    lib_validator = plistvalidators.ContentsPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)

    xml_fail_list = lib_validator.run_xml_validation()
    ufolib_fail_list = lib_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


# Fail tests

def test_validators_plist_ufo2_contents_missing_file_fail():
    contents_ufo_path = os.path.join(contents_test_dir_failpath, 'UFO2-MissingCont.ufo')
    contents_validator = plistvalidators.ContentsPlistValidator(contents_ufo_path, 2, ufo2_dir_list)

    xml_fail_list = contents_validator.run_xml_validation()
    ufolib_fail_list = contents_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_contents_missing_file_fail():
    contents_ufo_path = os.path.join(contents_test_dir_failpath, 'UFO3-MissingCont.ufo')
    contents_validator = plistvalidators.ContentsPlistValidator(contents_ufo_path, 3, ufo3_dir_list)

    xml_fail_list = contents_validator.run_xml_validation()
    ufolib_fail_list = contents_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_contents_missing_file_fail(capsys):
    contents_ufo_path = os.path.join(contents_test_dir_failpath, 'UFO3-UnlistedGlifs.ufo')
    contents_validator = plistvalidators.ContentsPlistValidator(contents_ufo_path, 3, ufo3_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        contents_validator.run_ufolib_import_validation()

    out, _ = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'rogue files not listed in contents.plist: a.001.glif' in out


def test_validators_plist_ufo2_contents_xml_fail(capsys):
    contents_ufo_path = os.path.join(contents_test_dir_failpath, 'UFO2-XMLcont.ufo')
    contents_validator = plistvalidators.ContentsPlistValidator(contents_ufo_path, 2, ufo2_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        xml_fail_list = contents_validator.run_xml_validation()

        assert isinstance(xml_fail_list, list)
        assert len(xml_fail_list) == 1
        assert 'contents.plist' in xml_fail_list[0].test_long_stdstream_string
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO2-XMLcont.ufo' in out
    assert 'contents.plist' in out


def test_validators_plist_ufo3_contents_xml_fail(capsys):
    contents_ufo_path = os.path.join(contents_test_dir_failpath, 'UFO3-XMLcont.ufo')
    contents_validator = plistvalidators.ContentsPlistValidator(contents_ufo_path, 3, ufo3_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        xml_fail_list = contents_validator.run_xml_validation()

        assert isinstance(xml_fail_list, list)
        assert len(xml_fail_list) == 1
        assert 'contents.plist' in xml_fail_list[0].test_long_stdstream_string
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO3-XMLcont.ufo' in out
    assert 'contents.plist' in out


def test_validators_plist_ufo2_contents_ufolib_import_fail(capsys):
    contents_ufo_path = os.path.join(contents_test_dir_failpath, 'UFO2-UFOlibError.ufo')
    contents_validator = plistvalidators.ContentsPlistValidator(contents_ufo_path, 2, ufo2_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fail_list = contents_validator.run_ufolib_import_validation()

        assert isinstance(fail_list, list)
        assert len(fail_list) == 1
        assert 'contents.plist' in fail_list[0].test_long_stdstream_string
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO2-UFOlibError.ufo' in out
    assert 'contents.plist' in out


def test_validators_plist_ufo3_contents_ufolib_import_fail(capsys):
    contents_ufo_path = os.path.join(contents_test_dir_failpath, 'UFO3-UFOlibError.ufo')
    contents_validator = plistvalidators.ContentsPlistValidator(contents_ufo_path, 3, ufo3_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fail_list = contents_validator.run_ufolib_import_validation()

        assert isinstance(fail_list, list)
        assert len(fail_list) == 1
        assert 'contents.plist' in fail_list[0].test_long_stdstream_string
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO3-UFOlibError.ufo' in out
    assert 'contents.plist' in out


# ///////////////////////////////////////////////////////
#
#  layercontents.plist validator tests
#
# ///////////////////////////////////////////////////////

# Success tests

def test_validators_plist_ufo2_layercontents_success():
    """
    Not part of the UFO v2 spec so should not fail without the file in the source directory
    """
    lc_validator = plistvalidators.LayercontentsPlistValidator(ufo2_test_success_path, 2, ufo2_dir_list)

    xml_fail_list = lc_validator.run_xml_validation()
    ufolib_fail_list = lc_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_layercontents_success():
    """
    UFO 3+ spec only
    :return:
    """
    lc_validator = plistvalidators.LayercontentsPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)

    xml_fail_list = lc_validator.run_xml_validation()
    ufolib_fail_list = lc_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


# Fail tests

def test_validators_plist_ufo2_layercontents_missing_file_fail():
    """
    Not part of UFO v2 spec should not fail on missing file
    """
    lc_ufo_path = os.path.join(layercontents_test_dir_failpath, 'UFO2-MissingLC.ufo')
    lc_validator = plistvalidators.LayercontentsPlistValidator(lc_ufo_path, 2, ufo2_dir_list)

    xml_fail_list = lc_validator.run_xml_validation()
    ufolib_fail_list = lc_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_layercontents_missing_file_fail():
    """
    UFO v3+ spec only.
    Does not fail here for missing file, missing mandatory file check is performed in runner.py module
    """
    lc_ufo_path = os.path.join(layercontents_test_dir_failpath, 'UFO3-MissingLC.ufo')
    lc_validator = plistvalidators.LayercontentsPlistValidator(lc_ufo_path, 3, ufo3_dir_list)

    xml_fail_list = lc_validator.run_xml_validation()
    ufolib_fail_list = lc_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_layercontents_xml_fail(capsys):
    lc_ufo_path = os.path.join(layercontents_test_dir_failpath, 'UFO3-XMLlc.ufo')
    lc_validator = plistvalidators.LayercontentsPlistValidator(lc_ufo_path, 3, ufo3_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        xml_fail_list = lc_validator.run_xml_validation()

        assert isinstance(xml_fail_list, list)
        assert len(xml_fail_list) == 1
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO3-XMLlc.ufo' in out
    assert 'layercontents.plist' in out


def test_validators_plist_ufo3_layercontents_ufolib_import_fail(capsys):
    lc_ufo_path = os.path.join(layercontents_test_dir_failpath, 'UFO3-UFOlibError.ufo')
    lc_validator = plistvalidators.LayercontentsPlistValidator(lc_ufo_path, 3, ufo3_dir_list)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        fail_list = lc_validator.run_ufolib_import_validation()

        assert isinstance(fail_list, list)
        assert len(fail_list) == 1
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert 'UFO3-UFOlibError.ufo' in out
    assert 'layercontents.plist' in out


# ///////////////////////////////////////////////////////
#
#  layerinfo.plist validator tests
#
# ///////////////////////////////////////////////////////

# Success tests

def test_validators_plist_ufo2_layerinfo_success():
    """
    file is missing from UFO2 test directory.  Should not fail, not part of UFO2 spec
    """
    li_validator = plistvalidators.LayerinfoPlistValidator(ufo2_test_success_path, 2, ufo2_dir_list)

    xml_fail_list = li_validator.run_xml_validation()
    ufolib_fail_list = li_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_layerinfo_success():
    li_validator = plistvalidators.LayerinfoPlistValidator(ufo3_test_success_path, 3, ufo3_dir_list)

    xml_fail_list = li_validator.run_xml_validation()
    ufolib_fail_list = li_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


# Fail tests

def test_validators_plist_ufo3_layerinfo_missing_file_fail():
    li_ufo_path = os.path.join(layerinfo_test_dir_failpath, 'UFO3-MissingLI.ufo')
    li_validator = plistvalidators.LayerinfoPlistValidator(li_ufo_path, 3, ufo3_dir_list)

    xml_fail_list = li_validator.run_xml_validation()
    ufolib_fail_list = li_validator.run_ufolib_import_validation()

    assert isinstance(xml_fail_list, list)
    assert isinstance(ufolib_fail_list, list)
    assert len(xml_fail_list) == 0
    assert len(ufolib_fail_list) == 0


def test_validators_plist_ufo3_layerinfo_xml_fail():
    li_ufo_path = os.path.join(layerinfo_test_dir_failpath, 'UFO3-XMLli.ufo')
    li_validator = plistvalidators.LayerinfoPlistValidator(li_ufo_path, 3, ufo3_dir_list)

    xml_fail_list = li_validator.run_xml_validation()

    assert isinstance(xml_fail_list, list)
    assert len(xml_fail_list) == 1
    assert 'layerinfo.plist' in xml_fail_list[0].test_long_stdstream_string


def test_validators_plist_ufo3_layerinfo_ufolib_import_fail():
    li_ufo_path = os.path.join(layerinfo_test_dir_failpath, 'UFO3-UFOLibError.ufo')
    li_validator = plistvalidators.LayerinfoPlistValidator(li_ufo_path, 3, ufo3_dir_list)

    fail_list = li_validator.run_ufolib_import_validation()

    assert isinstance(fail_list, list)
    assert len(fail_list) == 1
    assert 'layerinfo.plist' in fail_list[0].test_long_stdstream_string


