from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUBMODULE_ROOT = ROOT / "matrix-rust-sdk"
TARGET_CRATE = "matrix-sdk-ffi"
GENERATED_DIR = ROOT / "src" / "matrix_sdk_python" / "_generated"
GENERATED_MODULES = [
    "matrix_sdk.py",
    "matrix_sdk_base.py",
    "matrix_sdk_common.py",
    "matrix_sdk_contentscanner.py",
    "matrix_sdk_crypto.py",
    "matrix_sdk_ffi.py",
    "matrix_sdk_ui.py",
]
NATIVE_LIB_PATTERNS = [
    "matrix_sdk_ffi.dll",
    "libmatrix_sdk_ffi.so",
    "libmatrix_sdk_ffi.dylib",
]


def run(command: list[str], *, cwd: Path) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


def resolve_library(profile: str) -> Path:
    profile_dir = "debug" if profile == "dev" else profile
    target_dir = SUBMODULE_ROOT / "target" / profile_dir

    for pattern in NATIVE_LIB_PATTERNS:
        candidate = target_dir / pattern
        if candidate.exists():
            return candidate

    available = sorted(path.name for path in target_dir.glob("*")) if target_dir.exists() else []
    raise FileNotFoundError(
        f"Could not locate built {TARGET_CRATE} native library in {target_dir}. Available files: {available}"
    )


def clean_generated_dir() -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    for name in GENERATED_MODULES + NATIVE_LIB_PATTERNS + ["__init__.py"]:
        path = GENERATED_DIR / name
        if path.exists():
            path.unlink()


def write_generated_package_init() -> None:
    (GENERATED_DIR / "__init__.py").write_text(
        "# Generated UniFFI Python bindings live in this package.\n",
        encoding="utf-8",
    )


def build_rust_library(profile: str) -> Path:
    features = "sentry,experimental-element-recent-emojis"
    run(
        [
            "cargo",
            "build",
            "-p",
            TARGET_CRATE,
            "--profile",
            profile,
            "--features",
            features,
        ],
        cwd=SUBMODULE_ROOT,
    )
    return resolve_library(profile)


def generate_python_bindings(library_path: Path) -> None:
    run(
        [
            "cargo",
            "run",
            "-p",
            "uniffi-bindgen",
            "--",
            "generate",
            "--library",
            str(library_path),
            "--language",
            "python",
            "--out-dir",
            str(GENERATED_DIR),
        ],
        cwd=SUBMODULE_ROOT,
    )


def copy_native_library(library_path: Path) -> None:
    destination = GENERATED_DIR / library_path.name
    shutil.copy2(library_path, destination)


def main() -> int:
    profile = "reldev"
    clean = False

    args = sys.argv[1:]
    idx = 0
    while idx < len(args):
        arg = args[idx]
        if arg == "--profile":
            idx += 1
            if idx >= len(args):
                raise SystemExit("--profile requires a value")
            profile = args[idx]
        elif arg == "--clean":
            clean = True
        else:
            raise SystemExit(f"Unknown argument: {arg}")
        idx += 1

    if not SUBMODULE_ROOT.exists():
        raise SystemExit(f"Expected submodule at {SUBMODULE_ROOT}")

    if clean:
        clean_generated_dir()
    else:
        GENERATED_DIR.mkdir(parents=True, exist_ok=True)

    library_path = build_rust_library(profile)
    generate_python_bindings(library_path)
    copy_native_library(library_path)
    write_generated_package_init()

    print(f"Generated bindings into {GENERATED_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
