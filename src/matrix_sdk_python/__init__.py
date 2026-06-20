import inspect

from ._version import __version__
from ._generated import matrix_sdk_ffi as _ffi


def _is_public_ffi_symbol(name: str, obj: object) -> bool:
    if name.startswith("_"):
        return False
    if inspect.ismodule(obj):
        return False
    if name.endswith("Protocol"):
        return False
    module_name = getattr(obj, "__module__", "")
    return module_name.startswith("matrix_sdk_python._generated.matrix_sdk_ffi")


for _name, _obj in vars(_ffi).items():
    if _is_public_ffi_symbol(_name, _obj):
        globals()[_name] = _obj


__all__ = ["__version__", *sorted(name for name, obj in vars(_ffi).items() if _is_public_ffi_symbol(name, obj))]
