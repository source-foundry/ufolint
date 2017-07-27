#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os


class StdStreamer(object):
    def __init__(self, ufo_path):
        self.ufopath = ufo_path
        self.short_success_string = "."
        self.short_fail_string = "F"
        self.fail_long_indicator = "[FAIL]"

    def stream_testname(self, testname_string):
        sys.stdout.write("[" + testname_string + "] ")

    def stream_results_list(self, result_list):
        for resultobj in result_list:
            self.stream_result(resultobj)

    def stream_result(self, resultobj):
        if resultobj.test_failed is True:
            self._stream_short(self.short_fail_string)
            if resultobj.exit_failure is True:
                fail_string = self.ufopath + " failed! Exit with status code 1"
                print(os.linesep)
                print("=" * len(fail_string))
                print(self.ufopath + " failed! Exit with status code 1")
                print("=" * len(fail_string))
                print(" ")
                print("Test result that led to failure:")
                print(self.fail_long_indicator + " " + resultobj.test_long_stdstream_string)
                print(" ")  # add newline to stdout before exiting
                sys.exit(1)
        elif resultobj.test_failed is False:
            self._stream_short(self.short_success_string)

    def stream_final_failures(self, result_list):
        if len(result_list) > 0:
            fail_string = self.ufopath + " failed! Exit with status code 1"
            print(" ")
            print("=" * len(fail_string))
            print(self.ufopath + " failed! Exit with status code 1")
            print("=" * len(fail_string))
            print(" ")

            for resultobj in result_list:
                print(self.fail_long_indicator + " " + resultobj.test_long_stdstream_string)
            sys.exit(1)
        else:
            success_string = self.ufopath + " - All tests passed!"
            print(" ")
            print(" ")
            print("=" * len(success_string))
            print(success_string)
            print("=" * len(success_string))
            sys.exit(0)

    def _stream_short(self, output_string):
        sys.stdout.write(output_string)

    def _stream_long(self, output_string):
        print(output_string)

