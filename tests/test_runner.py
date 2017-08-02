#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest


from ufolint.controllers.runner import MainRunner
from ufolint.stdoutput import StdStreamer

# Constants for tests
ufo2_test_success_path = os.path.join('tests', 'testfiles', 'ufo', 'passes', 'UFO2-Pass.ufo')
ufo3_test_success_path = os.path.join('tests', 'testfiles', 'ufo', 'passes', 'UFO3-Pass.ufo')
ufo_fail_dir_basepath = os.path.join('tests', 'testfiles', 'ufo', 'fails')

# MainRunner class instantiation

def test_ufolint_runner_ufo2_mainrunner_class_instantiation():
    mr = MainRunner(ufo2_test_success_path)
    assert mr.ufopath == ufo2_test_success_path
    assert mr.ufolib_reader is None
    assert mr.ufoversion is None
    assert mr.failures_list == []
    assert mr.ufo_glyphs_dir_list == []
    assert mr.ufoobj is None


def test_ufolint_runner_ufo3_mainrunner_class_instantiation():
    mr = MainRunner(ufo3_test_success_path)
    assert mr.ufopath == ufo3_test_success_path
    assert mr.ufolib_reader is None
    assert mr.ufoversion is None
    assert mr.failures_list == []
    assert mr.ufo_glyphs_dir_list == []
    assert mr.ufoobj is None


# Class method tests


# _check_layercontents_plist_exists
def test_ufolint_runner_ufo2_check_layercontents_plist_method_fail():
    """
    UFOv2 does not include a layercontents.plist file in spec.  the test dir does not include this file.  this test is
    run in a version specific manner in runner.py so it should fail
    """
    mr = MainRunner(ufo2_test_success_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._check_layercontents_plist_exists()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufolint_runner_ufo3_check_layercontents_plist_method_success(capsys):
    ss = StdStreamer(ufo3_test_success_path)
    mr = MainRunner(ufo3_test_success_path)
    mr._check_layercontents_plist_exists()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string


def test_ufolint_runner_ufo3_check_layercontents_plist_method_fail():
    lc_fail_path = os.path.join(ufo_fail_dir_basepath, 'layercontentsPL', 'UFO3-MissingLC.ufo')
    mr = MainRunner(lc_fail_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._check_layercontents_plist_exists()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


# _check_metainfo_plist_exists
def test_ufolint_runner_ufo2_check_metainfo_plist_method_success(capsys):
    ss = StdStreamer(ufo2_test_success_path)
    mr = MainRunner(ufo2_test_success_path)
    mr._check_metainfo_plist_exists()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string


def test_ufolint_runner_ufo2_check_metainfo_plist_method_fail():
    mi_fail_path = os.path.join(ufo_fail_dir_basepath, 'metainfoPL', 'UFO2-MissingMeta.ufo')
    mr = MainRunner(mi_fail_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._check_metainfo_plist_exists()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufolint_runner_ufo3_check_metainfo_plist_method_success(capsys):
    ss = StdStreamer(ufo3_test_success_path)
    mr = MainRunner(ufo3_test_success_path)
    mr._check_metainfo_plist_exists()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string


def test_ufolint_runner_ufo3_check_metainfo_plist_method_fail():
    mi_fail_path = os.path.join(ufo_fail_dir_basepath, 'metainfoPL', 'UFO3-MissingMeta.ufo')
    mr = MainRunner(mi_fail_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._check_metainfo_plist_exists()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


# _check_ufo_import_and_define_ufo_version
def test_ufolint_runner_ufo2_checkufoimportdefineversion_success(capsys):
    ss = StdStreamer(ufo2_test_success_path)
    mr = MainRunner(ufo2_test_success_path)
    mr._check_ufo_import_and_define_ufo_version()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string
    assert mr.ufoversion == 2


def test_ufolint_runner_ufo2_checkufoimportdefineversion_fail():
    mi_fail_path = os.path.join(ufo_fail_dir_basepath, 'metainfoPL', 'UFO2-MissingMeta.ufo')
    mr = MainRunner(mi_fail_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._check_ufo_import_and_define_ufo_version()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufolint_runner_ufo3_checkufoimportdefineversion_success(capsys):
    ss = StdStreamer(ufo3_test_success_path)
    mr = MainRunner(ufo3_test_success_path)
    mr._check_ufo_import_and_define_ufo_version()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string
    assert mr.ufoversion == 3


def test_ufolint_runner_ufo3_checkufoimportdefineversion_fail():
    mi_fail_path = os.path.join(ufo_fail_dir_basepath, 'metainfoPL', 'UFO3-MissingMeta.ufo')
    mr = MainRunner(mi_fail_path)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._check_ufo_import_and_define_ufo_version()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


# _check_ufo_dir_extension
def test_ufolint_runner_checkufodirextension_success(capsys):
    testsource_dir = "Test-Regular.ufo"
    ss = StdStreamer(testsource_dir)
    mr = MainRunner(testsource_dir)
    mr._check_ufo_dir_extension()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string


def test_ufolint_runner_checkufodirextension_fail():
    testsource_dir = "Test-Regular"
    mr = MainRunner(testsource_dir)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._check_ufo_dir_extension()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


# _check_ufo_dir_path_exists
def test_ufolint_runner_ufodirpathexists_success(capsys):
    ss = StdStreamer(ufo3_test_success_path)
    mr = MainRunner(ufo3_test_success_path)
    mr._check_ufo_dir_extension()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string


def test_ufolint_runner_ufodirpathexists_fail():
    testpath = "Bogus-Regular.ufo"
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._check_ufo_dir_path_exists()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


# _validate_read_data_types_metainfo_plist

def test_ufolint_runner_ufo2_validate_types_metainfo_success(capsys):
    ss = StdStreamer(ufo2_test_success_path)
    mr = MainRunner(ufo2_test_success_path)
    mr._validate_read_data_types_metainfo_plist()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string


def test_ufolint_runner_ufo3_validate_types_metainfo_success(capsys):
    ss = StdStreamer(ufo3_test_success_path)
    mr = MainRunner(ufo3_test_success_path)
    mr._validate_read_data_types_metainfo_plist()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string


def test_ufolint_runner_ufo2_validate_types_metainfo_missing_formatversion_fail():
    testpath = os.path.join(ufo_fail_dir_basepath, 'runner', 'UFO2-Metainfo-FVmissing.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._validate_read_data_types_metainfo_plist()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufolint_runner_ufo3_validate_types_metainfo_missing_formatversion_fail():
    testpath = os.path.join(ufo_fail_dir_basepath, 'runner', 'UFO3-Metainfo-FVmissing.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._validate_read_data_types_metainfo_plist()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufolint_runner_ufo2_validate_types_metainfo_badtype_formatversion_fail():
    testpath = os.path.join(ufo_fail_dir_basepath, 'runner', 'UFO2-Metainfo-FVwrongtype.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._validate_read_data_types_metainfo_plist()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufolint_runner_ufo3_validate_types_metainfo_badtype_formatversion_fail():
    testpath = os.path.join(ufo_fail_dir_basepath, 'runner', 'UFO3-Metainfo-FVwrongtype.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._validate_read_data_types_metainfo_plist()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufolint_runner_ufo3_validate_types_metainfo_raises_exception_fail():
    testpath = os.path.join(ufo_fail_dir_basepath, 'metainfoPL', 'UFO3-XMLmeta.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._validate_read_data_types_metainfo_plist()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


# _validate_read_load_glyphsdirs_layercontents_plist
def test_ufolint_runner_ufo2_validatereadload_layercontents_success(capsys):
    ss = StdStreamer(ufo3_test_success_path)
    mr = MainRunner(ufo3_test_success_path)
    mr._validate_read_load_glyphsdirs_layercontents_plist()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string


def test_ufolint_runner_ufo3_validatereadload_layercontents_success(capsys):
    ss = StdStreamer(ufo3_test_success_path)
    mr = MainRunner(ufo3_test_success_path)
    mr._validate_read_load_glyphsdirs_layercontents_plist()
    out, err = capsys.readouterr()
    assert out == ss.short_success_string


def test_ufolint_runner_ufo2_validatereadload_layercontents_fail():
    testpath = os.path.join(ufo_fail_dir_basepath, 'layercontentsPL', 'UFO2-MissingLC.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._validate_read_load_glyphsdirs_layercontents_plist()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufolint_runner_ufo3_validatereadload_layercontents_fail():
    testpath = os.path.join(ufo_fail_dir_basepath, 'layercontentsPL', 'UFO3-MissingLC.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr._validate_read_load_glyphsdirs_layercontents_plist()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


# run method ufolint specific validation tests

def test_ufolint_runner_ufo2_run_success():
    mr = MainRunner(ufo2_test_success_path)
    mr.run()

    assert mr.ufoversion == 2
    assert isinstance(mr.failures_list, list)
    assert len(mr.failures_list) == 0   # nothing failed during the run of a valid UFO directory


def test_ufolint_runner_ufo3_run_success():
    mr = MainRunner(ufo3_test_success_path)
    mr.run()

    assert mr.ufoversion == 3
    assert isinstance(mr.failures_list, list)
    assert len(mr.failures_list) == 0  # nothing failed during the run of a valid UFO directory


#  -- version outside of supported range test

def test_ufolint_runner_unsupported_version():
    testpath = os.path.join(ufo_fail_dir_basepath, 'metainfoPL', 'UFO2-VersionFail.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr.run()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


#  -- missing a defined glyphs directory in v3+

def test_ufolint_runner_missing_layercontents_plist_defined_glyphs_dir():
    testpath = os.path.join(ufo_fail_dir_basepath, 'layercontentsPL', 'UFO3-MissingGlyphsDir.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr.run()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


#  -- missing mandatory file test

def test_ufolint_runner_mandatory_file_missing_test():
    testpath = os.path.join(ufo_fail_dir_basepath, 'contentsPL', 'UFO2-MissingCont.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr.run()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


#  -- XML validation test

def test_ufolint_runner_xml_validation_fail_test():
    testpath = os.path.join(ufo_fail_dir_basepath, 'fontinfoPL', 'UFO3-XMLfi.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr.run()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


#  -- ufoLib import validation
def test_ufolint_runner_ufolib_import_fail_test():
    testpath = os.path.join(ufo_fail_dir_basepath, 'fontinfoPL', 'UFO3-UFOlibError.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr.run()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


#  -- .glif file spec validation
def test_ufolint_runner_glif_validation_fail_test():
    testpath = os.path.join(ufo_fail_dir_basepath, 'glif', 'UFO3-UFOlibError.ufo')
    mr = MainRunner(testpath)

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        mr.run()

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
