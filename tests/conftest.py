import pendulum
import pytest


@pytest.fixture(autouse=True)
def setup():
    pendulum.set_local_timezone(pendulum.timezone("America/Toronto"))

    yield

    pendulum.set_test_now()
    pendulum.set_locale("en")
    pendulum.set_local_timezone()
    pendulum.week_starts_at(pendulum.MONDAY)
    pendulum.week_ends_at(pendulum.SUNDAY)


def assert_datetime(
    d, year, month, day, hour=None, minute=None, second=None, microsecond=None
):
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


def assert_date(d, year, month, day):
    assert year == d.year
    assert month == d.month
    assert day == d.day


def assert_time(t, hour, minute, second, microsecond=None):
    assert hour == t.hour
    assert minute == t.minute
    assert second == t.second

    if microsecond is not None:
        assert microsecond == t.microsecond


def assert_duration(
    dur,
    years=None,
    months=None,
    weeks=None,
    days=None,
    hours=None,
    minutes=None,
    seconds=None,
    microseconds=None,
):
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
