from __future__ import annotations

from collections import namedtuple
from datetime import date
from datetime import datetime

def days_in_year(year: int) -> int: ...
def is_leap(year: int) -> bool: ...
def is_long_year(year: int) -> bool: ...
def local_time(
    unix_time: int, utc_offset: int, microseconds: int
) -> tuple[int, int, int, int, int, int, int]: ...

class PreciseDiff(
    namedtuple(
        "PreciseDiff",
        "years months days " "hours minutes seconds microseconds " "total_days",
    )
):
    years: int
    months: int
    days: int
    hours: int
    minutes: int
    seconds: int
    microseconds: int
    total_days: int

def precise_diff(d1: datetime | date, d2: datetime | date) -> PreciseDiff: ...
def timestamp(dt: datetime) -> int: ...
def week_day(year: int, month: int, day: int) -> int: ...
