from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import pendulum


if TYPE_CHECKING:
    from collections.abc import Iterator


@pytest.fixture(autouse=True)
def setup() -> Iterator[None]:
    pendulum.set_local_timezone(pendulum.timezone("America/Toronto"))

    yield

    pendulum.set_locale("en")
    pendulum.set_local_timezone()
    pendulum.week_starts_at(pendulum.WeekDay.MONDAY)
    pendulum.week_ends_at(pendulum.WeekDay.SUNDAY)


def assert_datetime(
    d: pendulum.DateTime,
    year: int,
    month: int,
    day: int,
    hour: int | None = None,
    minute: int | None = None,
    second: int | None = None,
    microsecond: int | None = None,
) -> None:
    assert year == d.year
    assert month == d.month
    assert day == d.day

    if hour is not None:
        assert hour == d.hour

    if minute is not None:
        assert minute == d.minute

    if second is not None:
        assert second == d.second

    if microsecond is not None:
        assert microsecond == d.microsecond


def assert_date(d: pendulum.Date, year: int, month: int, day: int) -> None:
    assert year == d.year
    assert month == d.month
    assert day == d.day


def assert_time(
    t: pendulum.Time,
    hour: int,
    minute: int,
    second: int,
    microsecond: int | None = None,
) -> None:
    assert hour == t.hour
    assert minute == t.minute
    assert second == t.second

    if microsecond is not None:
        assert microsecond == t.microsecond


def assert_duration(
    dur: pendulum.Duration,
    years: int | None = None,
    months: int | None = None,
    weeks: int | None = None,
    days: int | None = None,
    hours: int | None = None,
    minutes: int | None = None,
    seconds: int | None = None,
    microseconds: int | None = None,
) -> None:
    expected = {}
    actual = {}

    if years is not None:
        expected["years"] = dur.years
        actual["years"] = years

    if months is not None:
        expected["months"] = dur.months
        actual["months"] = months

    if weeks is not None:
        expected["weeks"] = dur.weeks
        actual["weeks"] = weeks

    if days is not None:
        expected["days"] = dur.remaining_days
        actual["days"] = days

    if hours is not None:
        expected["hours"] = dur.hours
        actual["hours"] = hours

    if minutes is not None:
        expected["minutes"] = dur.minutes
        actual["minutes"] = minutes

    if seconds is not None:
        expected["seconds"] = dur.remaining_seconds
        actual["seconds"] = seconds

    if microseconds is not None:
        expected["microseconds"] = dur.microseconds
        actual["microseconds"] = microseconds

    assert expected == actual
