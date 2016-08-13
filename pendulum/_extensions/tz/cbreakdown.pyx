# -*- coding: utf-8 -*-

from cpython cimport bool
from datetime import datetime


cdef long EPOCH_YEAR = 1970

cdef long DAYS_PER_N_YEAR = 365
cdef long DAYS_PER_L_YEAR = 366

cdef long USECS_PER_SEC = 1000000

cdef long SECS_PER_MIN = 60
cdef long SECS_PER_HOUR = 60 * SECS_PER_MIN
cdef long SECS_PER_DAY = SECS_PER_HOUR * 24

# 400-year chunks always have 146097 days (20871 weeks).
cdef long DAYS_PER_400_YEARS = 146097
cdef long SECS_PER_400_YEARS = DAYS_PER_400_YEARS * SECS_PER_DAY

# The number of seconds in an aligned 100-year chunk, for those that
# do not begin with a leap year and those that do respectively.
cdef list SECS_PER_100_YEARS = [
    (76 * DAYS_PER_N_YEAR + 24 * DAYS_PER_L_YEAR) * SECS_PER_DAY,
    (75 * DAYS_PER_N_YEAR + 25 * DAYS_PER_L_YEAR) * SECS_PER_DAY,
]

# The number of seconds in an aligned 4-year chunk, for those that
# do not begin with a leap year and those that do respectively.
cdef list SECS_PER_4_YEARS = [
    (4 * DAYS_PER_N_YEAR + 0 * DAYS_PER_L_YEAR) * SECS_PER_DAY,
    (3 * DAYS_PER_N_YEAR + 1 * DAYS_PER_L_YEAR) * SECS_PER_DAY,
]

# The number of seconds in non-leap and leap years respectively.
cdef list SECS_PER_YEAR = [
    DAYS_PER_N_YEAR * SECS_PER_DAY,
    DAYS_PER_L_YEAR * SECS_PER_DAY,
]

cdef long MONTHS_PER_YEAR = 12

# The month lengths in non-leap and leap years respectively.
cdef list DAYS_PER_MONTHS = [
    [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    [-1, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
]

# The day offsets of the beginning of each (1-based) month in non-leap
# and leap years respectively.
# For example, in a leap year there are 335 days before December.
cdef list MONTHS_OFFSETS = [
    [-1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365],
    [-1, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
]

cdef int TM_SUNDAY = 0
cdef int TM_MONDAY = 1
cdef int TM_TUESDAY = 2
cdef int TM_WEDNESDAY = 3
cdef int TM_THURSDAY = 4
cdef int TM_FRIDAY = 5
cdef int TM_SATURDAY = 6

cdef int TM_JANUARY = 0
cdef int TM_FEBRUARY = 1
cdef int TM_MARCH = 2
cdef int TM_APRIL = 3
cdef int TM_MAY = 4
cdef int TM_JUNE = 5
cdef int TM_JULY = 6
cdef int TM_AUGUST = 7
cdef int TM_SEPTEMBER = 8
cdef int TM_OCTOBER = 9
cdef int TM_NOVEMBER = 10
cdef int TM_DECEMBER = 11


cdef tuple _local_time(unix_time, int utc_offset, bool is_dst, str abbrev):
    cdef long year
    cdef long microsecond
    cdef long seconds
    cdef long leap_year
    cdef long sec_per_100years
    cdef long sec_per_4years
    cdef long sec_per_year
    cdef long month
    cdef long day
    cdef long month_offset
    cdef long hour
    cdef long minute
    cdef long second

    year = EPOCH_YEAR
    microsecond = int(round(unix_time % 1, 6) * 1e6)
    seconds = int(unix_time)

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
        hour, minute, second, microsecond,
        utc_offset, is_dst, abbrev
    )


def local_time(unix_time, ttype):
    return _local_time(unix_time, ttype.utc_offset, ttype.is_dst, ttype.abbrev)
