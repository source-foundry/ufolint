#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pytest

from ufolint.app import main


ufo3_test_success_path = os.path.join('tests', 'testfiles', 'ufo', 'passes', 'UFO3-Pass.ufo')


def test_ufolint_app_main_function_missing_args(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.argv = ['ufolint']
        main()
    out, err = capsys.readouterr()
    assert '[ufolint] ERROR:' in err
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufolint_app_main_function_help_request(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.argv = ['ufolint', '--help']
        main()
    out, err = capsys.readouterr()
    assert len(out) > 1
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufolint_app_main_function_version_request(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.argv = ['ufolint', '--version']
        main()
    out, err = capsys.readouterr()
    assert 'ufolint v' in out
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufolint_app_main_function_usage_request(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.argv = ['ufolint', '--usage']
        main()
    out, err = capsys.readouterr()
    assert 'ufolint' in out
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufolint_app_main_function_mainrunner():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        sys.argv = ['ufolint', ufo3_test_success_path]
        main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

