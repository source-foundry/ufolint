#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest

from ufolint.data.ufo import Ufo, Ufo2, Ufo3


# Test paths for Ufo objects
test_ufopath = "Test-Regular.ufo"
# UFO v2 tests
test_glyphs_dirlist_2 = [['public.default', 'glyphs']]
# UFO v3 tests
test_glyphs_dirlist_3 = [['public.default', 'glyphs'], ['org.sourcefoundry.another', 'glyphsOther']]

# Expected plist filepaths
## root
metainfo_plist_path = os.path.join('Test-Regular.ufo', 'metainfo.plist')
fontinfo_plist_path = os.path.join('Test-Regular.ufo', 'fontinfo.plist')
groups_plist_path = os.path.join('Test-Regular.ufo', 'groups.plist')
kerning_plist_path = os.path.join('Test-Regular.ufo', 'kerning.plist')
lib_plist_path = os.path.join('Test-Regular.ufo', 'lib.plist')
layercontents_plist_path = os.path.join('Test-Regular.ufo', 'layercontents.plist')
## glyphs subdirectory
contents_plist_path_1 = os.path.join('Test-Regular.ufo', 'glyphs', 'contents.plist')
contents_plist_path_2 = os.path.join('Test-Regular.ufo', 'glyphsOther', 'contents.plist')
layerinfo_plist_path_1 = os.path.join('Test-Regular.ufo', 'glyphs', 'layerinfo.plist')
layerinfo_plist_path_2 = os.path.join('Test-Regular.ufo', 'glyphsOther', 'layerinfo.plist')

# Expected mandatory file path lists
mandatory_list_v2 = [metainfo_plist_path, contents_plist_path_1]
mandatory_list_v3 = [metainfo_plist_path, layercontents_plist_path, contents_plist_path_1, contents_plist_path_2]


def test_data_ufo_ufo_class_instantiation_with_single_glyphsdir():
    ufoobj = Ufo(test_ufopath, test_glyphs_dirlist_2)

    assert ufoobj.ufopath == "Test-Regular.ufo"
    assert ufoobj.glyphsdir_list == test_glyphs_dirlist_2
    assert ufoobj.mandatory_root_basefilepaths is None
    assert ufoobj.mandatory_glyphsdir_basefilepaths is None


def test_data_ufo_ufo_class_instantiation_with_multiple_glyphsdir():
    ufoobj = Ufo(test_ufopath, test_glyphs_dirlist_3)

    assert ufoobj.ufopath == "Test-Regular.ufo"
    assert ufoobj.glyphsdir_list == test_glyphs_dirlist_3
    assert ufoobj.mandatory_root_basefilepaths is None
    assert ufoobj.mandatory_glyphsdir_basefilepaths is None


def test_data_ufo_ufo2_class_instantiation():
    ufoobj = Ufo2(test_ufopath, test_glyphs_dirlist_2)

    assert ufoobj.ufopath == "Test-Regular.ufo"
    assert ufoobj.glyphsdir_list == test_glyphs_dirlist_2
    assert ufoobj.mandatory_root_basefilepaths == ['metainfo.plist']
    assert ufoobj.mandatory_glyphsdir_basefilepaths == ['contents.plist']


def test_data_ufo_ufo3_class_instantiation():
    ufoobj = Ufo3(test_ufopath, test_glyphs_dirlist_3)

    assert ufoobj.ufopath == "Test-Regular.ufo"
    assert ufoobj.glyphsdir_list == test_glyphs_dirlist_3
    assert ufoobj.mandatory_root_basefilepaths == ['metainfo.plist', 'layercontents.plist']
    assert ufoobj.mandatory_glyphsdir_basefilepaths == ['contents.plist']


def test_data_ufo_ufo2_make_root_plist_path():
    ufoobj = Ufo2(test_ufopath, test_glyphs_dirlist_2)

    assert ufoobj._make_root_plist_path('metainfo.plist') == metainfo_plist_path
    assert ufoobj._make_root_plist_path('fontinfo.plist') == fontinfo_plist_path
    assert ufoobj._make_root_plist_path('groups.plist') == groups_plist_path
    assert ufoobj._make_root_plist_path('kerning.plist') == kerning_plist_path
    assert ufoobj._make_root_plist_path('lib.plist') == lib_plist_path


def test_data_ufo_ufo3_make_root_plist_path():
    ufoobj = Ufo3(test_ufopath, test_glyphs_dirlist_3)

    assert ufoobj._make_root_plist_path('metainfo.plist') == metainfo_plist_path
    assert ufoobj._make_root_plist_path('fontinfo.plist') == fontinfo_plist_path
    assert ufoobj._make_root_plist_path('groups.plist') == groups_plist_path
    assert ufoobj._make_root_plist_path('kerning.plist') == kerning_plist_path
    assert ufoobj._make_root_plist_path('lib.plist') == lib_plist_path
    assert ufoobj._make_root_plist_path('layercontents.plist') == layercontents_plist_path


def test_data_ufo_ufo2_make_glyphsdir_plist_path():
    glyphsdirname = "glyphs"
    ufoobj = Ufo2(test_ufopath, test_glyphs_dirlist_2)

    assert ufoobj._make_glyphsdir_plist_path(glyphsdirname, 'contents.plist') == contents_plist_path_1


def test_data_ufo_ufo3_make_glyphsdir_plist_path():
    glyphsdirname = "glyphs"
    ufoobj = Ufo2(test_ufopath, test_glyphs_dirlist_3)

    assert ufoobj._make_glyphsdir_plist_path(glyphsdirname, 'contents.plist') == contents_plist_path_1
    assert ufoobj._make_glyphsdir_plist_path(glyphsdirname, 'layerinfo.plist') == layerinfo_plist_path_1


def test_data_ufo_ufo2_get_root_plist_filepath():
    ufoobj = Ufo2(test_ufopath, test_glyphs_dirlist_2)

    assert ufoobj.get_root_plist_filepath('metainfo.plist') == metainfo_plist_path
    assert ufoobj.get_root_plist_filepath('fontinfo.plist') == fontinfo_plist_path
    assert ufoobj.get_root_plist_filepath('groups.plist') == groups_plist_path
    assert ufoobj.get_root_plist_filepath('kerning.plist') == kerning_plist_path
    assert ufoobj.get_root_plist_filepath('lib.plist') == lib_plist_path


def test_data_ufo_ufo3_get_root_plist_filepath():
    ufoobj = Ufo2(test_ufopath, test_glyphs_dirlist_3)

    assert ufoobj.get_root_plist_filepath('metainfo.plist') == metainfo_plist_path
    assert ufoobj.get_root_plist_filepath('fontinfo.plist') == fontinfo_plist_path
    assert ufoobj.get_root_plist_filepath('groups.plist') == groups_plist_path
    assert ufoobj.get_root_plist_filepath('kerning.plist') == kerning_plist_path
    assert ufoobj.get_root_plist_filepath('lib.plist') == lib_plist_path
    assert ufoobj.get_root_plist_filepath('layercontents.plist') == layercontents_plist_path


def test_data_ufo_ufo2_get_glyphsdir_plist_filepath_list():
    ufoobj = Ufo2(test_ufopath, test_glyphs_dirlist_2)

    assert isinstance(ufoobj.get_glyphsdir_plist_filepath_list('contents.plist'), list) is True
    assert len(ufoobj.get_glyphsdir_plist_filepath_list('contents.plist')) == 1
    assert ufoobj.get_glyphsdir_plist_filepath_list('contents.plist')[0] == contents_plist_path_1


def test_data_ufo_ufo3_get_glyphsdir_plist_filepath_list():
    ufoobj = Ufo3(test_ufopath, test_glyphs_dirlist_3)

    assert isinstance(ufoobj.get_glyphsdir_plist_filepath_list('contents.plist'), list) is True
    assert len(ufoobj.get_glyphsdir_plist_filepath_list('contents.plist')) == 2
    assert ufoobj.get_glyphsdir_plist_filepath_list('contents.plist')[0] == contents_plist_path_1
    assert ufoobj.get_glyphsdir_plist_filepath_list('contents.plist')[1] == contents_plist_path_2

    assert isinstance(ufoobj.get_glyphsdir_plist_filepath_list('layerinfo.plist'), list) is True
    assert len(ufoobj.get_glyphsdir_plist_filepath_list('layerinfo.plist')) == 2
    assert ufoobj.get_glyphsdir_plist_filepath_list('layerinfo.plist')[0] == layerinfo_plist_path_1
    assert ufoobj.get_glyphsdir_plist_filepath_list('layerinfo.plist')[1] == layerinfo_plist_path_2


def test_data_ufo_ufo2_get_mandatory_filepaths_list():
    ufoobj = Ufo2(test_ufopath, test_glyphs_dirlist_2)

    res_list = ufoobj.get_mandatory_filepaths_list()
    assert isinstance(res_list, list)
    assert len(res_list) == 2
    for filepath in res_list:
        assert (filepath in mandatory_list_v2) is True
    assert (fontinfo_plist_path in res_list) is False


def test_data_ufo_ufo3_get_mandatory_filepaths_list():
    ufoobj = Ufo3(test_ufopath, test_glyphs_dirlist_3)

    res_list = ufoobj.get_mandatory_filepaths_list()
    assert isinstance(res_list, list)
    assert len(res_list) == 4
    for filepath in res_list:
        assert (filepath in mandatory_list_v3) is True
    assert (fontinfo_plist_path in res_list) is False






