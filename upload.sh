#!/usr/bin/env bash

python3 setup.py sdist && twine upload dist/
