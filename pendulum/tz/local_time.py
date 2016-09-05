# -*- coding: utf-8 -*-

try:
    from .._extensions.tz._local_time import local_time
except ImportError:
    from .._extensions.tz.local_time import local_time
