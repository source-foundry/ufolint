#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
try:
    from plistlib import readPlist as load
    from plistlib import writePlist as dump
except ImportError:
    from plistlib import load
    from plistlib import dump

from ufoLib import UFOReader, UFOLibError

from ufolint.utilities import file_exists, dir_exists
from ufolint.data.tstobj import Result
from ufolint.stdoutput import StdStreamer
from ufolint.data.ufo import Ufo2, Ufo3
from ufolint.controllers.plist import MetainfoPlistValidator, FontinfoPlistValidator, GroupsPlistValidator
from ufolint.controllers.plist import KerningPlistValidator, LibPlistValidator, ContentsPlistValidator
from ufolint.controllers.plist import LayercontentsPlistValidator, LayerinfoPlistValidator


class MainRunner(object):
    def __init__(self, ufopath):
        self.ufopath = ufopath
        self.ufolib_reader = None
        self.ufoversion = None
        self.failures_list = []       # list of strings that include all failures across all tests for final report
        self.ufo_glyphs_dir_list = []  # list of glyphs directory(ies) available in the source (>1 permitted in UFOv3+)

    def run(self):
        # Print UFO filepath header
        print(" ")
        print('~' * len(self.ufopath))
        print(self.ufopath)
        print('~' * len(self.ufopath))
        print(" ")

        # [START] EARLY FAIL TESTS ----------------------------------------------------------------
        #      UFO directory filepath
        #      import with ufoLib
        #      version check
        #      ufo obj define
        #        v3 only: presence of layercontents.plist to define the glyphs directories in source
        #        v2 only: no layercontents.plist, define as single glyphs directory
        ss = StdStreamer(self.ufopath)
        ss.stream_testname("UFO directory")
        self._check_ufo_dir_path_exists()                 # tests user defined UFO directory path
        self._check_ufo_dir_extension()                   # tests for .ufo extension on directory
        self._check_ufo_import_and_define_ufo_version()   # defines UFOReader object as class property after import
        if self.ufoversion == 3:
            self._check_layercontents_plist_present()     # tests for presence of a layercontents.plist in root of UFO
            self._validate_read_load_glyphsdirs_layercontents_plist()  # validate layercontents.plist xml and load glyphs dirs
        elif self.ufoversion == 2:
            self.ufo_glyphs_dir_list = [['public.default', 'glyphs']]  # define as single glyphs directory for UFOv2
        else:   # fail if unsupported UFO version (in ufolint)
            sys.stderr.write(os.linesep + "[ufolint] UFO v" + self.ufoversion + " is not supported in ufolint" + os.linesep)
            sys.exit(1)
        print(" ")
        print("   Found UFO v" + str(self.ufoversion))
        print("   Source defined glyphs directories: ")
        for glyphs_dir in self.ufo_glyphs_dir_list:
            print("     -- " + glyphs_dir[1])
        # [END] EARLY FAIL TESTS ----------------------------------------------------------------

        # [START] MANDATORY FILEPATH TESTS  -----------------------------------------------------
        ss.stream_testname("UFO v" + str(self.ufoversion) + " mandatory filepaths")

        if self.ufoversion == 2:
            ufoobj = Ufo2(self.ufopath, self.ufo_glyphs_dir_list)
        elif self.ufoversion == 3:
            ufoobj = Ufo3(self.ufopath, self.ufo_glyphs_dir_list)
        mandatory_file_list = ufoobj.get_mandatory_filepaths_list()
        for mandatory_file in mandatory_file_list:
            res = Result(mandatory_file)
            if file_exists(mandatory_file):
                res.test_failed = False
                ss.stream_result(res)
            else:
                res.test_failed = True
                res.test_long_stdstream_string = mandatory_file + " was not found in " + self.ufopath
                ss.stream_result(res)
        print(" ")
        # [END] MANDATORY FILEPATH TESTS ----------------------------------------------------------

        # [START] XML VALIDATION TESTS  -----------------------------------------------------------
        ss.stream_testname("XML validations")
        meta_val = MetainfoPlistValidator(self.ufopath, self.ufoversion, self.ufo_glyphs_dir_list)
        fontinfo_val = FontinfoPlistValidator(self.ufopath, self.ufoversion, self.ufo_glyphs_dir_list)
        groups_val = GroupsPlistValidator(self.ufopath, self.ufoversion, self.ufo_glyphs_dir_list)
        kerning_val = KerningPlistValidator(self.ufopath, self.ufoversion, self.ufo_glyphs_dir_list)
        lib_val = LibPlistValidator(self.ufopath, self.ufoversion, self.ufo_glyphs_dir_list)
        contents_val = ContentsPlistValidator(self.ufopath, self.ufoversion, self.ufo_glyphs_dir_list)
        layercont_val = LayercontentsPlistValidator(self.ufopath, self.ufoversion, self.ufo_glyphs_dir_list)
        layerinfo_val = LayerinfoPlistValidator(self.ufopath, self.ufoversion, self.ufo_glyphs_dir_list)

        meta_val.run_xml_validation()
        fontinfo_val.run_xml_validation()
        groups_val.run_xml_validation()
        kerning_val.run_xml_validation()
        lib_val.run_xml_validation()
        contents_val.run_xml_validation()
        layercont_val.run_xml_validation()
        layerinfo_val.run_xml_validation()
        # [END] XML VALIDATION TESTS  --------------------------------------------------------------

        # TESTS COMPLETED -------------------------------------------------------------------------
        #   stream all failure results as a newline delimited list to user and exit with status code 1
        #   if failures are present, status code 0 if failures are not present
        ss = StdStreamer(self.ufopath)
        ss.stream_final_failures(self.failures_list)

    # =====================================
    #
    #  TESTS
    #
    # =====================================

    def _check_layercontents_plist_present(self):
        """
        UFO 3+ test for layercontents.plist file in the top level of UFO directory
        :return: (boolean) True = file present, False = file absent
        """
        ufo3 = Ufo3(self.ufopath)
        ss = StdStreamer(self.ufopath)
        lcp_test_filepath = ufo3.get_root_plist_filepath('layercontents.plist')
        res = Result(lcp_test_filepath)

        if file_exists(lcp_test_filepath):
            res.test_failed = False
            ss.stream_result(res)
        else:
            res.test_failed = True
            res.exit_failure = True  # early exit if cannot find this file to define glyphs directories in UFO source
            res.test_long_stdstream_string = "layercontents.plist was not found in " + self.ufopath
            ss.stream_result(res)




    def _check_ufo_import_and_define_ufo_version(self):
        """
        Tests UFO directory import with ufoLib UFOReader object and defines class property (ufo) with the
        ufoLib UFOReader object.  This object is used for additional tests in this module.  Failures added to the
        class property failures_list for final report
        :return: None
        """
        ss = StdStreamer(self.ufopath)
        res = Result(self.ufopath)
        try:
            ufolib_reader = UFOReader(self.ufopath)
            self.ufoversion = ufolib_reader.formatVersion
            self.ufolib_reader = ufolib_reader
            res.test_failed = False
            ss.stream_result(res)
        except UFOLibError as e:
            res.test_failed = True
            res.test_long_stdstream_string = str(e)
            self.failures_list.append(res)
            ss.stream_result(res)

    def _check_ufo_dir_extension(self):
        """
        Tests for .ufo extension on the user defined (command line) directory path. Results
        streamed through std output stream. Failures added to the
        class property failures_list for final report
        :return: None
        """
        ss = StdStreamer(self.ufopath)
        res = Result(self.ufopath)
        if self.ufopath[-4:] == ".ufo":
            res.test_failed = False
            ss.stream_result(res)
        else:
            res.test_failed = True
            res.test_long_stdstream_string = self.ufopath + " directory does not have a .ufo extension"
            self.failures_list.append(res)
            ss.stream_result(res)

    def _check_ufo_dir_path_exists(self):
        """
        Tests existence of a directory on the user defined (command line) directory path
        Results streamed through std output stream. Failures added to the
        class property failures_list for final report
        :return: None
        """
        ss = StdStreamer(self.ufopath)
        if dir_exists(self.ufopath) is False:
            res = Result(self.ufopath)
            res.test_failed = True
            res.exit_failure = True
            res.test_long_stdstream_string = self.ufopath + " does not appear to be a valid UFO directory"
            self.failures_list.append(res.test_long_stdstream_string)
            ss.stream_result(res)  # raises sys.exit(1) on this failure, do not need to add to failures_list
        else:
            res = Result(self.ufopath)
            res.test_failed = False
            ss.stream_result(res)

    # =====================================
    #
    #  UTILITIES
    #
    # =====================================

    def _validate_read_load_glyphsdirs_layercontents_plist(self):
        ufo = Ufo3(self.ufopath)
        layercontents_plist_path = ufo.get_root_plist_filepath('layercontents.plist')
        res = Result(layercontents_plist_path)
        ss = StdStreamer(layercontents_plist_path)
        try:
            # loads as [ ['layername1', 'glyphsdir1'], ['layername2', 'glyphsdir2'] ]
            self.ufo_glyphs_dir_list = load(layercontents_plist_path)
            res.test_failed = False
            ss.stream_result(res)
        except Exception as e:
            res.test_failed = True
            res.exit_failure = True
            res.test_long_stdstream_string = layercontents_plist_path + ": " + str(e)
            ss.stream_result(res)

