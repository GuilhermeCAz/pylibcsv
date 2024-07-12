#!/bin/sh
apk add --no-cache python3-dev build-base py3-pip

python3 -m venv /app/.venv
source /app/.venv/bin/activate

pip install --upgrade pip
pip install --no-cache-dir cython setuptools

python3 setup.py build_ext --inplace

mv libcsv*.so libcsv.so

export PYTHONPATH=.
