from Cython.Build import cythonize  # type: ignore[import-untyped]
from setuptools import Extension, setup

extensions = [
    Extension(
        'libcsv',
        sources=['src/libcsv.pyx'],
        include_dirs=['.', '/usr/include/python3.12'],
        library_dirs=['/usr/lib/python3.12/config-3.12-x86_64-linux-gnu'],
        libraries=['python3.12'],
        runtime_library_dirs=['.'],
        extra_compile_args=['-std=c99'],
    ),
]

setup(
    name='libcsv_wrapper',
    ext_modules=cythonize(
        extensions,
        language_level=3,
        force=True,
        annotate=True,
    ),
    headers=['libcsv.h'],
)
