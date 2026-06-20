# matrix-sdk-python

Python bindings for `matrix-rust-sdk` built from the existing `matrix-sdk-ffi` UniFFI layer.

## Overview

This repository packages the upstream Rust FFI bindings as a Python distribution:

- Rust FFI source lives in `matrix-rust-sdk/bindings/matrix-sdk-ffi`
- Python packaging lives in this repository root
- `uv` manages the Python project and developer workflows
- GitHub Actions builds platform wheels and publishes them to PyPI and GitHub Releases

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- Rust toolchain
- Git with submodule support

## Development

Sync dependencies:

```bash
uv sync
```

Generate Python bindings and copy the native library into the package tree:

```bash
uv run python scripts/build_bindings.py --profile reldev
```

Use the package through the top-level public API, for example:

```python
from matrix_sdk_python import MediaSource, matrix_to_user_permalink
```

Build the Sphinx API documentation locally:

```bash
uv run python scripts/build_docs.py
```

Run smoke tests:

```bash
uv run pytest
```

Build wheel and sdist metadata locally:

```bash
uv build
```

## Notes

- The generated UniFFI Python modules are treated as build artifacts and are not checked in.
- Wheels are platform-specific because they bundle the native `matrix-sdk-ffi` shared library.
- The first release path is optimized for wheel publication; source installs are not the primary target.
- The Sphinx docs build exports the full generated Python API surface by running `sphinx-apidoc` over `src/matrix_sdk_python` after bindings have been generated.
