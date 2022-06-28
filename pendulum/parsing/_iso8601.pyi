from __future__ import annotations

from datetime import date
from datetime import datetime
from datetime import time

class Duration:

    years: int = 0
    months: int = 0
    weeks: int = 0
    days: int = 0
    remaining_days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    remaining_seconds: int = 0
    microseconds: int = 0

def parse_iso8601(
    text: str,
) -> datetime | date | time | Duration: ...
