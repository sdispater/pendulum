import pytzdata

from typing import Union

from .timezone import Timezone, FixedTimezone, UTC
from .local_timezone import LocalTimezone


timezones = pytzdata.timezones


def timezone(name: Union[str, int]) -> Timezone:
    """
    Loads a Timezone instance by name.
    """
    if isinstance(name, int):
        return FixedTimezone.load(name)

    return Timezone.load(name)


def local_timezone() -> Timezone:
    """
    Loads the local timezone.
    """
    return LocalTimezone.get()


def test_local_timezone(mock: Union[Timezone, str, None]):
    """
    Context manager to temporarily set the local_timezone value.
    """
    return LocalTimezone.test(mock)


def set_local_timezone(timezone: Union[Timezone, str, None] = None) -> None:
    """
    Set the the local timezone to a given one.
    """
    LocalTimezone.set(timezone)
