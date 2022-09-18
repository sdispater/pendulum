from __future__ import annotations

import sys

from pendulum.tz.local_timezone import get_local_timezone
from pendulum.tz.local_timezone import set_local_timezone
from pendulum.tz.local_timezone import test_local_timezone
from pendulum.tz.timezone import UTC
from pendulum.tz.timezone import FixedTimezone
from pendulum.tz.timezone import Timezone

if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources

PRE_TRANSITION = "pre"
POST_TRANSITION = "post"
TRANSITION_ERROR = "error"

_timezones = None

_tz_cache: dict[int, FixedTimezone] = {}


def timezones() -> tuple[str, ...]:
    global _timezones

    if _timezones is None:
        with resources.files("tzdata").joinpath("zones").open() as f:
            _timezones = tuple(tz.strip() for tz in f.readlines())

    return _timezones


def timezone(name: str | int) -> Timezone | FixedTimezone:
    """
    Return a Timezone instance given its name.
    """
    if isinstance(name, int):
        return fixed_timezone(name)

    if name.lower() == "utc":
        return UTC

    return Timezone(name)


def fixed_timezone(offset: int) -> FixedTimezone:
    """
    Return a Timezone instance given its offset in seconds.
    """
    if offset in _tz_cache:
        return _tz_cache[offset]

    tz = FixedTimezone(offset)
    _tz_cache[offset] = tz

    return tz


def local_timezone() -> Timezone | FixedTimezone:
    """
    Return the local timezone.
    """
    return get_local_timezone()


__all__ = [
    "UTC",
    "Timezone",
    "FixedTimezone",
    "set_local_timezone",
    "get_local_timezone",
    "test_local_timezone",
    "timezone",
    "fixed_timezone",
    "local_timezone",
    "timezones",
]
