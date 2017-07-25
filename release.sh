#!/usr/bin/env bash

python3 setup.py sdist bdist_wheel
twine upload dist/{{project}}-0.1.0*
