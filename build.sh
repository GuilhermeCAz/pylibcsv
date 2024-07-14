#!/bin/sh
apk add --no-cache python3-dev build-base py3-pip

python3 -m venv /app/.venv
source /app/.venv/bin/activate

pip install --upgrade pip
pip install --no-cache-dir cython setuptools

python3 setup.py build_ext --inplace

gcc -shared -o libcsv.so src/main.c -lpython3.12 -I/usr/include/python3.12 -L/usr/lib/python3.8/config-3.12-x86_64-linux-gnu
