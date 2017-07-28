#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

try:
    import xml.etree.cElementTree as ETree           # python 2
except ImportError:
    import xml.etree.ElementTree as ETree            # python 3

from ufolint.data.tstobj import Result
from ufolint.data.ufo import Ufo2, Ufo3
from ufolint.stdoutput import StdStreamer
from ufolint.utilities import file_exists

from ufoLib import UFOReader, UFOLibError


class AbstractPlistValidator(object):
    def __init__(self, ufopath, ufoversion, glyphs_dir_list):
        self.ufopath = ufopath
        self.ufoversion = ufoversion
        self.glyphs_dir_list = glyphs_dir_list
        self.testfile = None
        if self.ufoversion == 2:
            self.ufoobj = Ufo2(self.ufopath, self.glyphs_dir_list)
        elif self.ufoversion == 3:
            self.ufoobj = Ufo3(self.ufopath, self.glyphs_dir_list)
        self.root_plist_list = self.ufoobj.all_root_plist_files_list
        self.glyphsdir_plist_list = self.ufoobj.all_glyphsdir_plist_files_list
        self.test_fail_list = []

    def _parse_xml(self, testpath):
        res = Result(testpath)
        try:
            ETree.parse(testpath)
            res.test_failed = False
            return res
        except Exception as e:
            res.test_failed = True
            res.test_long_stdstream_string = testpath + " failed XML validation test with error: " + str(e)
            self.test_fail_list.append(res)  # add each failure to test failures list, returned to calling code from run_xml_validation
            return res

    def run_xml_validation(self):
        ss = StdStreamer(self.ufopath)
        if self.testfile in self.root_plist_list:
            testpath = self.ufoobj.get_root_plist_filepath(self.testfile)
            if file_exists(testpath):
                res = self._parse_xml(testpath)
                ss.stream_result(res)
            else:     # there is no file to check, mandatory files have already been checked, this is a success
                res = Result(testpath)
                res.test_failed = False
                ss.stream_result(res)
        elif self.testfile in self.glyphs_dir_list:
            testpath_list = self.ufoobj.get_glyphsdir_plist_filepath_list(self.testfile)
            for testpath in testpath_list:
                if file_exists(testpath):
                    res = self._parse_xml(testpath)
                    ss.stream_result(res)
                else:  # there is no file to check, mandatory files have already been checked, this is a success
                    res = Result(testpath)
                    res.test_failed = False
                    ss.stream_result(res)
        return self.test_fail_list  # return to the calling code so that it can be maintained for final user report

    def run_ufolib_import_validation(self):
        raise NotImplementedError


class MetainfoPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion, glyphs_dir_list):
        super(MetainfoPlistValidator, self).__init__(ufopath, ufoversion, glyphs_dir_list)
        self.testfile = "metainfo.plist"

    def run_ufolib_import_validation(self):
        """
        ufoLib UFOReader.readMetaInfo method validates the UFO version number.  This method adds validation for
        expected reverse URL name scheme in
        :return:
        """
        testpath = self.ufoobj.get_root_plist_filepath(self.testfile)
        res = Result(testpath)
        ss = StdStreamer(self.ufopath)
        try:
            ufolib_reader = UFOReader(self.ufopath)
            ufolib_reader.readMetaInfo()
            res.test_failed = False
            ss.stream_result(res)
        except UFOLibError as e:
            res.test_failed = True
            res.test_long_stdstream_string = testpath + " failed ufoLib import test with error: " + str(e)
            ss.stream_result(res)
            self.test_fail_list.append(res)
        return self.test_fail_list


class FontinfoPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion, glyphs_dir_list):
        super(FontinfoPlistValidator, self).__init__(ufopath, ufoversion, glyphs_dir_list)
        self.testfile = "fontinfo.plist"


class GroupsPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion, glyphs_dir_list):
        super(GroupsPlistValidator, self).__init__(ufopath, ufoversion, glyphs_dir_list)
        self.testfile = "groups.plist"


class KerningPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion, glyphs_dir_list):
        super(KerningPlistValidator, self).__init__(ufopath, ufoversion, glyphs_dir_list)
        self.testfile = "kerning.plist"


class LibPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion, glyphs_dir_list):
        super(LibPlistValidator, self).__init__(ufopath, ufoversion, glyphs_dir_list)
        self.testfile = "lib.plist"


class ContentsPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion, glyphs_dir_list):
        super(ContentsPlistValidator, self).__init__(ufopath, ufoversion, glyphs_dir_list)
        self.testfile = "contents.plist"  # test multiple glyphs directories in v3+


class LayercontentsPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion, glyphs_dir_list):
        super(LayercontentsPlistValidator, self).__init__(ufopath, ufoversion, glyphs_dir_list)
        self.testfile = "layercontents.plist"


class LayerinfoPlistValidator(AbstractPlistValidator):
    def __init__(self, ufopath, ufoversion, glyphs_dir_list):
        super(LayerinfoPlistValidator, self).__init__(ufopath, ufoversion, glyphs_dir_list)
        self.testfile = "layerinfo.plist"

