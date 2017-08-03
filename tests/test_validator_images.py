#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

from ufolint.validators.imagesvalidators import run_all_images_validations
from ufolint.data.ufo import Ufo2, Ufo3


# Constants
ufo2_test_success_path = os.path.join('tests', 'testfiles', 'ufo', 'passes', 'UFO2-Pass.ufo')
ufo3_test_success_path = os.path.join('tests', 'testfiles', 'ufo', 'passes', 'UFO3-Pass.ufo')
images_test_dir_failpath = os.path.join('tests', 'testfiles', 'ufo', 'fails', 'images')

test_glyphs_dirlist_v2 = [['public.default', 'glyphs']]
# UFO v3 tests
test_glyphs_dirlist_v3 = [['public.default', 'glyphs'], ['org.sourcefoundry.another', 'glyphs.public.background']]


# Success tests

def test_ufolint_validators_images_ufo2_success():
    """
    UFOv2 does not include images dir as part of spec.  When missing, returns empty list of failures
    """
    ufoobj = Ufo2(ufo2_test_success_path, test_glyphs_dirlist_v2)
    fail_list = run_all_images_validations(ufoobj)
    assert isinstance(fail_list, list)
    assert len(fail_list) == 0


def test_ufolint_validators_images_ufo3_success():
    ufoobj = Ufo3(ufo3_test_success_path, test_glyphs_dirlist_v3)
    fail_list = run_all_images_validations(ufoobj)
    assert isinstance(fail_list, list)
    assert len(fail_list) == 0


# Fail tests

def test_ufolint_validators_images_ufo3_emptydir():
    """
    Should return empty list of failures, does not fail
    """
    test_path = os.path.join(images_test_dir_failpath, 'UFO3-EmptyImages.ufo')
    ufoobj = Ufo3(test_path, test_glyphs_dirlist_v3)
    fail_list = run_all_images_validations(ufoobj)
    assert isinstance(fail_list, list)
    assert len(fail_list) == 0


def test_ufolint_validators_images_ufo3_missingdir():
    """
    Should return empty list of failures, does not fail
    """
    test_path = os.path.join(images_test_dir_failpath, 'UFO3-ImagesDirNotPresent.ufo')
    ufoobj = Ufo3(test_path, test_glyphs_dirlist_v3)
    fail_list = run_all_images_validations(ufoobj)
    assert isinstance(fail_list, list)
    assert len(fail_list) == 0


def test_ufolint_validators_images_ufo3_badimagefile():
    test_path = os.path.join(images_test_dir_failpath, 'UFO3-NonPNGImage.ufo')
    ufoobj = Ufo3(test_path, test_glyphs_dirlist_v3)
    fail_list = run_all_images_validations(ufoobj)
    assert len(fail_list) == 1    # includes failure Result object (jpg file contained in directory)
    assert 'testimg.jpg' in fail_list[0].test_long_stdstream_string
