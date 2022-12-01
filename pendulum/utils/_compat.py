from __future__ import annotations

import sys

PYPY = hasattr(sys, "pypy_version_info")
PY38 = sys.version_info[:2] >= (3, 8)

if sys.version_info < (3, 9):
    import importlib_resources as resources

    from backports import zoneinfo
else:
    import zoneinfo

    from importlib import resources

__all__ = ["resources", "zoneinfo"]
