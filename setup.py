import setuptools  # type: ignore[reportMissingImports]
from Cython.Build import cythonize  # type: ignore[reportMissingImports]

setuptools.setup(
    ext_modules=cythonize(
        setuptools.Extension(
            'libcsv',
            sources=['libcsv.pyx'],
            extra_link_args=['-lpython3.12'],
        ),
        language_level=3,
    ),
    headers=['libcsv.h'],
)
