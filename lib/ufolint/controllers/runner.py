#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ufoLib import UFOReader, UFOLibError

from ufolint.utilities import file_exists, dir_exists
from ufolint.data.tstobj import Result
from ufolint.stdoutput import StdStreamer


class HeadHoncho(object):
    def __init__(self, ufopath):
        self.ufopath = ufopath
        self.ufo = None
        self.ufoversion = None
        self.failures_list = []       # list of strings that include all failures across all tests for final report

    def run(self):
        # =====================================
        #
        #  UFO directory / filepath validations
        #
        # =====================================

        # [START] UFO directory filepath, import, version check, ufo obj define
        ss = StdStreamer(self.ufopath)
        print(" ")
        print('~' * len(self.ufopath))
        print(self.ufopath)
        print('~' * len(self.ufopath))
        print(" ")
        ss.stream_testname("UFO directory")
        self._check_ufo_dir_path_exists()                 # tests user defined UFO directory path
        self._check_ufo_dir_extension()                   # tests for .ufo extension on directory
        self._check_ufo_import_and_define_ufo_version()   # defines UFOReader object as class property after import
        ss.stream_end_test()
        # [END] UFO directory filepath, import, version check, ufo obj define

        # [START] UFO version specific filepath tests
        ss.stream_testname("UFO v" + str(self.ufoversion) + " paths")
        # TODO: implement tests
        ss.stream_end_test()



        # Tests completed, stream all failure results as a newline delimited list to user and exit with status code 1
        # if failures are present, status code 0 if failures are not present
        ss = StdStreamer(self.ufopath)
        ss.stream_final_failures(self.failures_list)

    # =====================================
    #
    #  TESTS
    #
    # =====================================

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
            ufo = UFOReader(self.ufopath)
            self.ufoversion = ufo.formatVersion
            self.ufo = ufo
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
