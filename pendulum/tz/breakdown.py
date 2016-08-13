# -*- coding: utf-8 -*-

try:
    from .._extensions.tz.cbreakdown import local_time
except ImportError:
    from .._extensions.tz.breakdown import local_time

__all__ = [
    'local_time'
]

