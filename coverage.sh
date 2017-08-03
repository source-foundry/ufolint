#!/bin/sh

coverage run --source ufolint -m py.test
coverage report -m
coverage html

coverage xml
codecov --token=$CODECOV_UFOLINT
