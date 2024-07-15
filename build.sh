#!/bin/sh
apk add --no-cache gcc musl-dev py3-pip python3-dev

python3 -m venv /app/.venv
source /app/.venv/bin/activate

pip install --upgrade pip
pip install --no-cache-dir cython setuptools pytest PyYAML

python3 setup.py build_ext --inplace

gcc -shared -o libcsv.so src/main.c -lpython3.12 -I/usr/include/python3.12
