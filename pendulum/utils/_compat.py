from __future__ import annotations

import sys

PYPY = hasattr(sys, "pypy_version_info")
PY38 = sys.version_info[:2] >= (3, 8)

if sys.version_info < (3, 9):
    from backports import zoneinfo
else:
    import zoneinfo

__all__ = ["zoneinfo"]
