import pytest
import pendulum
from pendulum.tz import LocalTimezone


@pytest.fixture(scope='session', autouse=True)
def setup():
    LocalTimezone.set_local_timezone(pendulum.timezone('America/Toronto'))

    yield

    pendulum.set_test_now()
    pendulum.set_formatter()
    pendulum.set_locale('en')
    LocalTimezone.set_local_timezone()
    pendulum.datetime.reset_to_string_format()
    pendulum.date.reset_to_string_format()
    pendulum.time.reset_to_string_format()
    pendulum.datetime.set_transition_rule(pendulum.POST_TRANSITION)


def assert_datetime(d, year, month, day,
                    hour=None, minute=None, second=None, microsecond=None):
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
