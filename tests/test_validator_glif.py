#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

from ufolint.data.ufo import Ufo2, Ufo3
from ufolint.validators.glifvalidators import run_all_glif_validations

ufo2_test_success_path = os.path.join('tests', 'testfiles', 'ufo', 'passes', 'UFO2-Pass.ufo')
ufo3_test_success_path = os.path.join('tests', 'testfiles', 'ufo', 'passes', 'UFO3-Pass.ufo')

ufo2_dir_list = [['public.default', 'glyphs']]
ufo3_dir_list = [['public.default', 'glyphs'], ['public.background', 'glyphs.public.background']]

glif_fail_dir = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'glif')


# Success tests

def test_validators_glif_ufo2_run_all_glif_validations_success():
    ufoobj = Ufo2(ufo2_test_success_path, ufo2_dir_list)
    failure_list = run_all_glif_validations(ufoobj)
    assert isinstance(failure_list, list)
    assert len(failure_list) == 0   # no failures detected


def test_validators_glif_ufo3_run_all_glif_validations_success():
    ufoobj = Ufo3(ufo3_test_success_path, ufo3_dir_list)
    failure_list = run_all_glif_validations(ufoobj)
    assert isinstance(failure_list, list)
    assert len(failure_list) == 0   # no failures detected


# Fail tests

def test_validators_glif_ufo2_run_all_glif_validations_missing_glif_fail():
    fail_ufo = os.path.join(glif_fail_dir, 'UFO2-MissingGlif.ufo')
    ufoobj = Ufo2(fail_ufo, ufo2_dir_list)
    failure_list = run_all_glif_validations(ufoobj)
    assert len(failure_list) == 1


def test_validators_glif_ufo3_run_all_glif_validations_missing_glif_fail():
    fail_ufo = os.path.join(glif_fail_dir, 'UFO3-MissingGlif.ufo')
    ufoobj = Ufo3(fail_ufo, ufo3_dir_list)
    failure_list = run_all_glif_validations(ufoobj)
    assert len(failure_list) == 1


def test_validators_glif_ufo2_run_all_glif_validations_ufolib_import_fail():
    fail_ufo = os.path.join(glif_fail_dir, 'UFO2-UFOlibError.ufo')
    ufoobj = Ufo2(fail_ufo, ufo2_dir_list)
    failure_list = run_all_glif_validations(ufoobj)
    assert len(failure_list) == 1


def test_validators_glif_ufo3_run_all_glif_validations_ufolib_import_fail():
    fail_ufo = os.path.join(glif_fail_dir, 'UFO3-UFOlibError.ufo')
    ufoobj = Ufo3(fail_ufo, ufo3_dir_list)
    failure_list = run_all_glif_validations(ufoobj)
    assert len(failure_list) == 1

