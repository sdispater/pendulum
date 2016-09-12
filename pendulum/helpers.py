# -*- coding: utf-8 -*-

try:
    from ._extensions._helpers import local_time
except ImportError:
    from ._extensions.helpers import local_time
