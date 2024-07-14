from Cython.Build import cythonize  # type: ignore[import-untyped]
from setuptools import Extension, setup

extensions = [
    Extension(
        name='pylibcsv',
        sources=['src/libcsv.py'],
        include_dirs=['.', '/usr/include/python3.12'],
        libraries=['python3.12'],
    ),
]

setup(
    name='pylibcsv',
    ext_modules=cythonize(
        module_list=extensions,
        force=True,
        language_level=3,
    ),
)
