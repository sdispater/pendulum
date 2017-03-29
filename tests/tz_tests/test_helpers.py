import pytest

from pendulum.tz import timezone, Timezone, FixedTimezone


def test_timezone_with_name():
    tz = timezone('Europe/Paris')

    assert isinstance(tz, Timezone)
    assert tz.name == 'Europe/Paris'


def test_timezone_with_invalid_name():
    with pytest.raises(ValueError):
        timezone('Invalid')


def test_timezone_with_offset():
    tz = timezone(-19800)

    assert isinstance(tz, FixedTimezone)
    assert tz.name == '-05:30'
