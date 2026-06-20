from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
BUILD_DIR = DOCS_DIR / "_build" / "html"
GENERATED_API_DIR = DOCS_DIR / "_generated_api"
BINDINGS_SCRIPT = ROOT / "scripts" / "build_bindings.py"
GENERATED_PACKAGE_DIR = ROOT / "src" / "matrix_sdk_python" / "_generated"
PACKAGE_DIR = ROOT / "src" / "matrix_sdk_python"


def run(command: list[str], *, cwd: Path) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, check=True)


def write_generated_api_index() -> None:
    module_files = sorted(
        path.stem
        for path in GENERATED_API_DIR.glob("*.rst")
        if path.stem not in {"modules", "matrix_sdk_python"}
    )

    entries = "\n".join(f"   {name}" for name in module_files)
    content = (
        "Generated module reference\n"
        "==========================\n\n"
        "This section documents the complete generated modules under ``matrix_sdk_python._generated``.\n\n"
        ".. toctree::\n"
        "   :maxdepth: 2\n\n"
        f"{entries}\n"
    )
    (GENERATED_API_DIR / "generated_index.rst").write_text(content, encoding="utf-8")


def main() -> int:
    profile = os.environ.get("MATRIX_SDK_PYTHON_DOCS_PROFILE", "reldev")

    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    if GENERATED_API_DIR.exists():
        shutil.rmtree(GENERATED_API_DIR)

    run([sys.executable, str(BINDINGS_SCRIPT), "--profile", profile, "--clean"], cwd=ROOT)
    run(
        [
            "sphinx-apidoc",
            "-f",
            "-e",
            "-M",
            "--remove-old",
            "--implicit-namespaces",
            "-o",
            str(GENERATED_API_DIR),
            str(PACKAGE_DIR),
            str(PACKAGE_DIR / "__init__.py"),
            str(PACKAGE_DIR / "_version.py"),
        ],
        cwd=ROOT,
    )
    write_generated_api_index()
    run(["sphinx-build", "-b", "html", "docs", str(BUILD_DIR)], cwd=ROOT)

    print(f"Built documentation into {BUILD_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
