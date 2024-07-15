"""Setuptools setup file for pylibcsv.

This file is used to build the pylibcsv package using Cython.
"""

from Cython.Build import cythonize  # type: ignore[import-untyped]
from setuptools import Extension, setup

extensions = [
    Extension(
        name='pylibcsv',
        sources=['src/libcsv.py'],
    ),
]

setup(
    name='pylibcsv',
    ext_modules=cythonize(
        module_list=extensions,
        language_level=3,
    ),
)
