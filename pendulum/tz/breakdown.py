# -*- coding: utf-8 -*-

try:
    from .._extensions.tz.cbreakdown import Breakdown
except ImportError as e:
    from .._extensions.tz.breakdown import Breakdown

__all__ = [
    'Breakdown'
]
