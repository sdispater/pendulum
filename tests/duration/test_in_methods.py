import pytest

import pendulum


def test_in_weeks():
    it = pendulum.duration(days=17)
    assert it.in_weeks() == 2


def test_in_days():
    it = pendulum.duration(days=3)
    assert it.in_days() == 3


def test_in_hours():
    it = pendulum.duration(days=3, minutes=72)
    assert it.in_hours() == 73


def test_in_minutes():
    it = pendulum.duration(minutes=6, seconds=72)
    assert it.in_minutes() == 7


def test_in_seconds():
    it = pendulum.duration(seconds=72)
    assert it.in_seconds() == 72


@pytest.mark.parametrize("month", range(1, 13))
def test_in_months_one_year_less_a_day(month):
    start = pendulum.datetime(2022, month, 2).date()
    end = pendulum.datetime(2023, month, 1).date()  # One year less a day
    assert (end - start).in_months() == 11


@pytest.mark.parametrize("month", range(1, 13))
def test_in_months_one_year(month):
    start = pendulum.datetime(2022, month, 1).date()
    end = pendulum.datetime(2023, month, 1).date()  # One year exactly
    assert (end - start).in_months() == 12


@pytest.mark.parametrize("day", range(1, 29))
def test_in_months_february(day):
    start = pendulum.datetime(2022, 2, 4).date()
    end_1 = pendulum.datetime(2023, 2, day).date()
    end_2 = end_1.add(days=1)
    m_diff_1 = (end_1 - start).in_months()
    m_diff_2 = (end_2 - start).in_months()
    assert m_diff_1 <= m_diff_2
