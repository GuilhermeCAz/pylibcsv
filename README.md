# libcsv

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FGuilhermeCAz%2Fshurl_django%2Fmain%2Fpyproject.toml&logo=python&label=Python)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-white?logo=pytest&logoColor=%230A9EDC)](https://github.com/pytest-dev/pytest)
[![Docker](https://img.shields.io/badge/Docker-%232496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Make](https://img.shields.io/badge/Make-%236D00CC?logo=make)](https://www.gnu.org/software/make/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

## Overview

This project demonstrates an efficient integration of Python and C (using Cython) for building a shared library for CSV processing, developed as part of a code challenge in a recruitment process.

The original challenge contained the [Dockerfile](Dockerfile), [libcsv.h](libcsv.h) and `test_libcsv` files. These files should not be modified. Instead, the [build.sh](build.sh) script should contain the steps to build a shared object, containing functions declared in [libcsv.h](libcsv.h).

`test_libcsv` was an ELF executable containing a single test to verify if the shared object was loaded correctly. The company requested not to share it (nor the challenge requirements) for security reasons. As such, the original `docker run` command is now invalid.

## Installation and Execution

1. Build the Docker image `(make build)`:

   ```bash
   docker build -t libcsv .
   ```

2. Run the Docker image (no longer valid) `(make run)`:

   ```bash
   docker run -it libcsv
   ```

3. Execute Python tests `(make tests)`:

   ```bash
   docker run -it libcsv /bin/sh -c "source /app/.venv/bin/activate && pytest"
   ```
