# -*- coding: utf-8 -*-

import pytzdata

from .timezone import Timezone, FixedTimezone, UTC
from .local_timezone import LocalTimezone


timezones = pytzdata.timezones


def timezone(name):
    """
    Loads a Timezone instance by name.

    :param name: The name of the timezone.
    :type name: str or int

    :rtype: Timezone
    """
    return Timezone.load(name)


def local_timezone():
    """
    Loads the local timezone.

    :rtype: Timezone
    """
    return LocalTimezone.get()
