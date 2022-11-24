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


if sys.version_info < (3, 8):
    from typing_extensions import Literal
    from typing_extensions import SupportsIndex
else:
    from typing import Literal
    from typing import SupportsIndex

__all__ = ["zoneinfo", "resources", "SupportsIndex", "Literal"]
