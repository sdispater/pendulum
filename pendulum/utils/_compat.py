from __future__ import annotations

import sys

PYPY = hasattr(sys, "pypy_version_info")
PY38 = sys.version_info[:2] >= (3, 8)

try:
    from backports import zoneinfo
except ImportError:
    import zoneinfo  # type: ignore[no-redef]

__all__ = ["zoneinfo"]
