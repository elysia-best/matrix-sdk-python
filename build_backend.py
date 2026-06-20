from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from setuptools.build_meta import *  # noqa: F401,F403
from setuptools.build_meta import build_sdist as _build_sdist
from setuptools.build_meta import build_wheel as _build_wheel

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "scripts" / "build_bindings.py"


def _run_build_bindings(profile: str) -> None:
    if os.environ.get("MATRIX_SDK_PYTHON_SKIP_BUILD") == "1":
        return

    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("MATRIX_SDK_PYTHON_SKIP_BUILD", "1")
    command = [sys.executable, str(SCRIPT), "--profile", profile]
    subprocess.run(command, cwd=ROOT, env=env, check=True)


def _default_profile() -> str:
    return os.environ.get("MATRIX_SDK_PYTHON_RUST_PROFILE", "dist")


def build_wheel(wheel_directory: str, config_settings=None, metadata_directory=None) -> str:
    _run_build_bindings(_default_profile())
    return _build_wheel(
        wheel_directory,
        config_settings=config_settings,
        metadata_directory=metadata_directory,
    )


def build_sdist(sdist_directory: str, config_settings=None) -> str:
    return _build_sdist(sdist_directory, config_settings=config_settings)


def get_requires_for_build_wheel(config_settings=None):
    return []


def get_requires_for_build_sdist(config_settings=None):
    return []
