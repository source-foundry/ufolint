#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import pytest

from ufolint.stdoutput import StdStreamer
from ufolint.data.tstobj import Result

# ///////////////////////////////////////////////////////
#
#  CONSTANTS
#
# ///////////////////////////////////////////////////////

test_ufopath = "Test-Regular.ufo"


# ///////////////////////////////////////////////////////
#
# pytest capsys capture tests
#    confirms capture of std output and std error streams
#    confirms capture of correct exit status codes
# ///////////////////////////////////////////////////////


def test_pytest_capsys_stdout(capsys):
    print("bogus text for a test")
    out, err = capsys.readouterr()
    assert out == "bogus text for a test\n"
    assert out != "something else"


def test_pytest_capsys_stdout_without_newline(capsys):
    sys.stdout.write("bogus text for a test")
    out, err = capsys.readouterr()
    assert out == "bogus text for a test"
    assert out != "something else"


def test_pytest_capsys_stderr(capsys):
    sys.stderr.write("more text for a test")
    out, err = capsys.readouterr()
    assert err == "more text for a test"
    assert err != "something else"


def test_pytest_capsys_errorcode_0(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(0)
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_pytest_capsys_errorcode_1(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.exit(1)
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


# ///////////////////////////////////////////////////////
#
# Begin stdoutput module tests
#
# ///////////////////////////////////////////////////////

def test_ufolint_stdout_instantiation():
    ss = StdStreamer(test_ufopath)
    assert ss.ufopath == test_ufopath
    assert ss.short_success_string == "."
    assert ss.short_fail_string == "F"
    assert ss.fail_long_indicator == "[FAIL]"


def test_ufolint_stdout_stream_short(capsys):
    ss = StdStreamer(test_ufopath)
    ss._stream_short("Good Test")
    out, err = capsys.readouterr()
    assert out == "Good Test"


def test_ufolint_stdout_stream_testname(capsys):
    ss = StdStreamer(test_ufopath)
    ss.stream_testname("Good Test")
    out, err = capsys.readouterr()
    assert out == "[Good Test] "


def test_ufolint_stdout_stream_result_successful_test(capsys):
    ss = StdStreamer(test_ufopath)
    res = Result(test_ufopath)
    res.test_failed = False
    ss.stream_result(res)
    out, err = capsys.readouterr()
    assert out == "."


def test_ufolint_stdout_stream_result_fail_test_noexit(capsys):
    ss = StdStreamer(test_ufopath)
    res = Result(test_ufopath)
    res.test_failed = True
    res.test_long_stdstream_string = "testfile.plist"
    ss.stream_result(res)
    out, err = capsys.readouterr()
    assert out == "F"


def test_ufolint_stdout_stream_result_fail_test_withexit(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ss = StdStreamer(test_ufopath)
        res = Result(test_ufopath)
        res.test_failed = True
        res.exit_failure = True
        res.test_long_stdstream_string = "testfile.plist"
        ss.stream_result(res)
    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert out[0] == "F"    # assert that the error flag 'F' is raised in the reported string
    assert "testfile.plist" in out  # assert that the failed file is included in the error message string


def test_ufolint_stdout_stream_results_list_with_multiple_pass_results(capsys):
    ss = StdStreamer(test_ufopath)

    res1 = Result(test_ufopath)
    res1.test_failed = False

    res2 = Result(test_ufopath)
    res2.test_failed = False

    result_list = [res1, res2]

    ss.stream_results_list(result_list)

    out, err = capsys.readouterr()
    assert out == ".."


def test_ufolint_stdout_stream_results_list_with_fail_noexit(capsys):
    ss = StdStreamer(test_ufopath)

    res1 = Result(test_ufopath)
    res1.test_failed = False

    res2 = Result(test_ufopath)
    res2.test_failed = True
    res2.test_long_stdstream_string = "testpath.plist"

    result_list = [res1, res2]
    ss.stream_results_list(result_list)

    out, err = capsys.readouterr()
    assert out[0:2] == ".F"


def test_ufolint_stdout_stream_results_list_with_fail_with_exit(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ss = StdStreamer(test_ufopath)
        res1 = Result(test_ufopath)
        res2 = Result(test_ufopath)

        res1.test_failed = True
        res1.test_long_stdstream_string = "afile.plist"

        res2.test_failed = True
        res2.exit_failure = True
        res2.test_long_stdstream_string = "testfile.plist"

        result_list = [res1, res2]
        ss.stream_results_list(result_list)

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert out[0:2] == "FF"    # assert that the error flag 'F' is raised in the reported string
    assert "testfile.plist" in out  # assert that the failed file is included in the error message string


def test_ufolint_stdout_stream_final_failures_all_successes(capsys):
    # the final failures list should be empty and should exit with status code 0
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ss = StdStreamer(test_ufopath)
        fail_result_list = []  # there were no failures included in the fail list
        ss.stream_final_failures(fail_result_list)

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufolint_stdout_stream_final_failures_singlefail(capsys):
    # the final failures list should be empty and should exit with status code 0
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ss = StdStreamer(test_ufopath)

        res = Result(test_ufopath)
        res.test_failed = True
        res.test_long_stdstream_string = "testpath.plist"

        fail_result_list = [res]  # there was a single failure included in the fail list
        ss.stream_final_failures(fail_result_list)

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert "testpath.plist" in out
    assert "Exit with status code 1" in out


def test_ufolint_stdout_stream_final_failures_multifail(capsys):
    # the final failures list should be empty and should exit with status code 0
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        ss = StdStreamer(test_ufopath)

        res1 = Result(test_ufopath)
        res1.test_failed = True
        res1.test_long_stdstream_string = "testpath.plist"

        res2 = Result(test_ufopath)
        res2.test_failed = True
        res2.test_long_stdstream_string = "secondpath.plist"

        fail_result_list = [res1, res2]  # there was a single failure included in the fail list
        ss.stream_final_failures(fail_result_list)

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert "testpath.plist" in out
    assert "secondpath.plist" in out
    assert "Exit with status code 1" in out