# -*- coding: utf-8 -*-

from .constants import SECONDS_PER_HOUR, SECONDS_PER_MINUTE


def day_ordinal(y, m, d):
    """
    Returns the number of days before/after 1970-01-01.

    :rtype: integer
    """
    if m <= 2:
        y -= 1

    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy

    return era * 146097 + doe - 719468


def timestamp(year, month, day, hour, minute, second, microsecond, tzinfo):
    days_in_seconds = day_ordinal(year, month, day) * 86400

    return (
        days_in_seconds
        + hour * SECONDS_PER_HOUR
        + minute * SECONDS_PER_MINUTE
        + second
        + microsecond / 1e6
        - tzinfo.offset
    )
