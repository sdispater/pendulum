from .timezone import Timezone, FixedTimezone, UTC
from .local_timezone import LocalTimezone


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

    :rtype: Timezone
    """
    return LocalTimezone.get()
