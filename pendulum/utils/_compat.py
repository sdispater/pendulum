import sys


PYPY = hasattr(sys, "pypy_version_info")


try:
    from backports import zoneinfo
except ImportError:
    import zoneinfo


__all__ = ["zoneinfo"]
