import pytzdata

from .timezone import Timezone, FixedTimezone, UTC
from .local_timezone import LocalTimezone


timezones = pytzdata.timezones


def timezone(name):
    """
    Loads a Timezone instance by name.

    :param name: The name of the timezone or its offset in seconds.
    :type name: str or int

    :rtype: Timezone
    """
    if isinstance(name, int):
        return FixedTimezone.load(name)

    return Timezone.load(name)


def local_timezone():
    """
    Loads the local timezone.

    :rtype: LocalTimezone
    """
    return LocalTimezone.get()


def test_local_timezone(mock):
    """
    Context manager to temporarily set the local_timezone value.

    :type mock: pendulum.tz.timezone.Timezone or str
    """
    return LocalTimezone.test(mock)


def set_local_timezone(timezone=None):
    """
    Set the the local timezone to a given one.

    :type mock: pendulum.tz.timezone.Timezone or str or None
    """
    LocalTimezone.set(timezone)
