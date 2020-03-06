from datetime import date
from datetime import datetime
from datetime import time

import pytest

from pendulum.parsing import parse_iso8601


try:
    from pendulum.parsing._extension import TZFixedOffset as FixedTimezone
except ImportError:
    from pendulum.tz.timezone import FixedTimezone


def test_parse_iso8601():
    # Date
    assert date(2016, 1, 1) == parse_iso8601("2016")
    assert date(2016, 10, 1) == parse_iso8601("2016-10")
    assert date(2016, 10, 6) == parse_iso8601("2016-10-06")
    assert date(2016, 10, 6) == parse_iso8601("20161006")

    # Time
    assert time(20, 16, 10, 0) == parse_iso8601("201610")

    # Datetime
    assert datetime(2016, 10, 6, 12, 34, 56, 123456) == parse_iso8601(
        "2016-10-06T12:34:56.123456"
    )
    assert datetime(2016, 10, 6, 12, 34, 56, 123000) == parse_iso8601(
        "2016-10-06T12:34:56.123"
    )
    assert datetime(2016, 10, 6, 12, 34, 56, 123) == parse_iso8601(
        "2016-10-06T12:34:56.000123"
    )
    assert datetime(2016, 10, 6, 12, 0, 0, 0) == parse_iso8601("2016-10-06T12")
    assert datetime(2016, 10, 6, 12, 34, 56, 0) == parse_iso8601("2016-10-06T123456")
    assert datetime(2016, 10, 6, 12, 34, 56, 123456) == parse_iso8601(
        "2016-10-06T123456.123456"
    )
    assert datetime(2016, 10, 6, 12, 34, 56, 123456) == parse_iso8601(
        "20161006T123456.123456"
    )
    assert datetime(2016, 10, 6, 12, 34, 56, 123456) == parse_iso8601(
        "20161006 123456.123456"
    )

    # Datetime with offset
    assert datetime(
        2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(19800)
    ) == parse_iso8601("2016-10-06T12:34:56.123456+05:30")
    assert datetime(
        2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(19800)
    ) == parse_iso8601("2016-10-06T12:34:56.123456+0530")
    assert datetime(
        2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(-19800)
    ) == parse_iso8601("2016-10-06T12:34:56.123456-05:30")
    assert datetime(
        2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(-19800)
    ) == parse_iso8601("2016-10-06T12:34:56.123456-0530")
    assert datetime(
        2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(18000)
    ) == parse_iso8601("2016-10-06T12:34:56.123456+05")
    assert datetime(
        2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(-18000)
    ) == parse_iso8601("2016-10-06T12:34:56.123456-05")
    assert datetime(
        2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(-18000)
    ) == parse_iso8601("20161006T123456,123456-05")
    assert datetime(
        2016, 10, 6, 12, 34, 56, 123456, FixedTimezone(+19800)
    ) == parse_iso8601("2016-10-06T12:34:56.123456789+05:30")

    # Ordinal date
    assert date(2012, 1, 7) == parse_iso8601("2012-007")
    assert date(2012, 1, 7) == parse_iso8601("2012007")
    assert date(2017, 3, 20) == parse_iso8601("2017-079")

    # Week date
    assert date(2012, 1, 30) == parse_iso8601("2012-W05")
    assert date(2008, 9, 27) == parse_iso8601("2008-W39-6")
    assert date(2010, 1, 3) == parse_iso8601("2009-W53-7")
    assert date(2008, 12, 29) == parse_iso8601("2009-W01-1")

    # Week date wth time
    assert datetime(2008, 9, 27, 9, 0, 0, 0) == parse_iso8601("2008-W39-6T09")


def test_parse_ios8601_invalid():
    # Invalid month
    with pytest.raises(ValueError):
        parse_iso8601("20161306T123456")

    # Invalid day
    with pytest.raises(ValueError):
        parse_iso8601("20161033T123456")

    # Invalid day for month
    with pytest.raises(ValueError):
        parse_iso8601("20161131T123456")

    # Invalid hour
    with pytest.raises(ValueError):
        parse_iso8601("20161006T243456")

    # Invalid minute
    with pytest.raises(ValueError):
        parse_iso8601("20161006T126056")

    # Invalid second
    with pytest.raises(ValueError):
        parse_iso8601("20161006T123460")

    # Extraneous separator
    with pytest.raises(ValueError):
        parse_iso8601("20140203 04:05:.123456")
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19 14:")

    # Invalid ordinal
    with pytest.raises(ValueError):
        parse_iso8601("2009367")
    with pytest.raises(ValueError):
        parse_iso8601("2009-367")
    with pytest.raises(ValueError):
        parse_iso8601("2015-366")
    with pytest.raises(ValueError):
        parse_iso8601("2015-000")

    # Invalid date
    with pytest.raises(ValueError):
        parse_iso8601("2009-")

    # Invalid time
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19T14:3924")
    with pytest.raises(ValueError):
        parse_iso8601("2010-02-18T16.5:23.35:48")
    with pytest.raises(ValueError):
        parse_iso8601("2010-02-18T16:23.35:48.45")
    with pytest.raises(ValueError):
        parse_iso8601("2010-02-18T16:23.33.600")

    # Invalid offset
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19 14:39:22+063")
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19 14:39:22+06a00")
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-19 14:39:22+0:6:00")

    # Missing time separator
    with pytest.raises(ValueError):
        parse_iso8601("2009-05-1914:39")

    # Invalid week date
    with pytest.raises(ValueError):
        parse_iso8601("2012-W63")
    with pytest.raises(ValueError):
        parse_iso8601("2012-W12-9")
    with pytest.raises(ValueError):
        parse_iso8601("2012W12-3")  # Missing separator
    with pytest.raises(ValueError):
        parse_iso8601("2012-W123")  # Missing separator


def test_parse_ios8601_duration():
    text = "P2Y3M4DT5H6M7S"
    parsed = parse_iso8601(text)

    assert parsed.years == 2
    assert parsed.months == 3
    assert parsed.weeks == 0
    assert parsed.remaining_days == 4
    assert parsed.hours == 5
    assert parsed.minutes == 6
    assert parsed.remaining_seconds == 7
    assert parsed.microseconds == 0

    text = "P1Y2M3DT4H5M6.5S"
    parsed = parse_iso8601(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 4
    assert parsed.minutes == 5
    assert parsed.remaining_seconds == 6
    assert parsed.microseconds == 500000

    text = "P1Y2M3DT4H5M6,5S"
    parsed = parse_iso8601(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 4
    assert parsed.minutes == 5
    assert parsed.remaining_seconds == 6
    assert parsed.microseconds == 500000

    text = "P1Y2M3D"
    parsed = parse_iso8601(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1Y2M3.5D"
    parsed = parse_iso8601(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1Y2M3,5D"
    parsed = parse_iso8601(text)

    assert parsed.years == 1
    assert parsed.months == 2
    assert parsed.weeks == 0
    assert parsed.remaining_days == 3
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "PT4H54M6.5S"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 4
    assert parsed.minutes == 54
    assert parsed.remaining_seconds == 6
    assert parsed.microseconds == 500000

    text = "PT4H54M6,5S"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 4
    assert parsed.minutes == 54
    assert parsed.remaining_seconds == 6
    assert parsed.microseconds == 500000

    text = "P1Y"
    parsed = parse_iso8601(text)

    assert parsed.years == 1
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1.5Y"
    with pytest.raises(ValueError):
        parse_iso8601(text)

    text = "P1,5Y"
    with pytest.raises(ValueError):
        parse_iso8601(text)

    text = "P1M"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 1
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1.5M"
    with pytest.raises(ValueError):
        parse_iso8601(text)

    text = "P1,5M"
    with pytest.raises(ValueError):
        parse_iso8601(text)

    text = "P1W"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 1
    assert parsed.remaining_days == 0
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1.5W"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 1
    assert parsed.remaining_days == 3
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1,5W"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 1
    assert parsed.remaining_days == 3
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1D"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 1
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1.5D"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 1
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "P1,5D"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 1
    assert parsed.hours == 12
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "PT1H"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 1
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "PT1.5H"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 1
    assert parsed.minutes == 30
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    text = "PT1,5H"
    parsed = parse_iso8601(text)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 1
    assert parsed.minutes == 30
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0

    # Double digit with 0
    text = "P2Y30M4DT5H6M7S"
    parsed = parse_iso8601(text)

    assert parsed.years == 2
    assert parsed.months == 30
    assert parsed.weeks == 0
    assert parsed.remaining_days == 4
    assert parsed.hours == 5
    assert parsed.minutes == 6
    assert parsed.remaining_seconds == 7
    assert parsed.microseconds == 0

    # No P operator
    with pytest.raises(ValueError):
        parse_iso8601("2Y3M4DT5H6M7S")

    # Week and other units combined
    with pytest.raises(ValueError):
        parse_iso8601("P1Y2W")

    # Invalid units order
    with pytest.raises(ValueError):
        parse_iso8601("P1S")

    with pytest.raises(ValueError):
        parse_iso8601("P1D1S")

    with pytest.raises(ValueError):
        parse_iso8601("1Y2M3D1SPT1M")

    with pytest.raises(ValueError):
        parse_iso8601("P1Y2M3D2MT1S")

    with pytest.raises(ValueError):
        parse_iso8601("P2M3D1ST1Y1M")

    with pytest.raises(ValueError):
        parse_iso8601("P1Y2M2MT3D1S")

    with pytest.raises(ValueError):
        parse_iso8601("P1D1Y1M")

    with pytest.raises(ValueError):
        parse_iso8601("PT1S1H")

    # Invalid
    with pytest.raises(ValueError):
        parse_iso8601("P1Dasdfasdf")

    # Invalid fractional
    with pytest.raises(ValueError):
        parse_iso8601("P2Y3M4DT5.5H6M7S")
