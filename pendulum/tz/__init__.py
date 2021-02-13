import os

from typing import Tuple
from typing import Union

import tzdata

from .local_timezone import get_local_timezone
from .local_timezone import set_local_timezone
from .local_timezone import test_local_timezone
from .timezone import UTC
from .timezone import FixedTimezone as _FixedTimezone
from .timezone import Timezone as _Timezone


PRE_TRANSITION = "pre"
POST_TRANSITION = "post"
TRANSITION_ERROR = "error"

_timezones = None


_tz_cache = {}


def timezones():
    global _timezones

    if _timezones is None:
        with open(os.path.join(os.path.dirname(tzdata.__file__), "zones")) as f:
            _timezones = tuple(tz.strip() for tz in f.readlines())

    return _timezones


def timezone(name: str) -> _Timezone:
    """
    Return a Timezone instance given its name.
    """
    if isinstance(name, int):
        return fixed_timezone(name)

    if name.lower() == "utc":
        return UTC

    return _Timezone(name)


def fixed_timezone(offset):  # type: (int) -> _FixedTimezone
    """
    Return a Timezone instance given its offset in seconds.
    """
    if offset in _tz_cache:
        return _tz_cache[offset]  # type: ignore

    tz = _FixedTimezone(offset)
    _tz_cache[offset] = tz

    return tz


def local_timezone():  # type: () -> _Timezone
    """
    Return the local timezone.
    """
    return get_local_timezone()
