# -*- coding: utf-8 -*-
import math

from ..constants import (
    EPOCH_YEAR,
    SECS_PER_DAY,
    SECS_PER_400_YEARS,
    SECS_PER_100_YEARS,
    SECS_PER_4_YEARS,
    SECS_PER_YEAR,
    SECS_PER_HOUR,
    SECS_PER_MIN,
    MONTHS_OFFSETS,
    TM_DECEMBER,
    TM_JANUARY
)


def local_time(unix_time, utc_offset, microseconds):
    """
    Returns a UNIX time as a broken down time
    for a particular transition type.

    :type unix_time: int
    :type utc_offset: int
    :type microseconds: int

    :rtype: tuple
    """
    year = EPOCH_YEAR
    seconds = int(math.floor(unix_time))

    # Shift to a base year that is 400-year aligned.
    if seconds >= 0:
        seconds -= 10957 * SECS_PER_DAY
        year += 30  # == 2000
    else:
        seconds += (146097 - 10957) * SECS_PER_DAY
        year -= 370  # == 1600

    seconds += utc_offset

    # Handle years in chunks of 400/100/4/1
    year += 400 * (seconds // SECS_PER_400_YEARS)
    seconds %= SECS_PER_400_YEARS
    if seconds < 0:
        seconds += SECS_PER_400_YEARS
        year -= 400

    leap_year = 1  # 4-century aligned

    sec_per_100years = SECS_PER_100_YEARS[leap_year]
    while seconds >= sec_per_100years:
        seconds -= sec_per_100years
        year += 100
        leap_year = 0  # 1-century, non 4-century aligned
        sec_per_100years = SECS_PER_100_YEARS[leap_year]

    sec_per_4years = SECS_PER_4_YEARS[leap_year]
    while seconds >= sec_per_4years:
        seconds -= sec_per_4years
        year += 4
        leap_year = 1  # 4-year, non century aligned
        sec_per_4years = SECS_PER_4_YEARS[leap_year]

    sec_per_year = SECS_PER_YEAR[leap_year]
    while seconds >= sec_per_year:
        seconds -= sec_per_year
        year += 1
        leap_year = 0  # non 4-year aligned
        sec_per_year = SECS_PER_YEAR[leap_year]

    # Handle months and days
    month = TM_DECEMBER + 1
    day = seconds // SECS_PER_DAY + 1
    seconds %= SECS_PER_DAY
    while month != TM_JANUARY + 1:
        month_offset = MONTHS_OFFSETS[leap_year][month]
        if day > month_offset:
            day -= month_offset
            break

        month -= 1

    # Handle hours, minutes, seconds and microseconds
    hour = seconds // SECS_PER_HOUR
    seconds %= SECS_PER_HOUR
    minute = seconds // SECS_PER_MIN
    second = seconds % SECS_PER_MIN

    return (
        year, month, day,
        hour, minute, second, microseconds
    )
