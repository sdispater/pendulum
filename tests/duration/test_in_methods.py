import pendulum
import pytest


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
    start = pendulum.parse(f"2022-{str(month).zfill(2)}-02")
    end = pendulum.parse(f"2023-{str(month).zfill(2)}-01")  # One year less a day
    assert (end - start).in_months() == 11


@pytest.mark.parametrize("month", range(1, 13))
def test_in_months_one_year(month):
    start = pendulum.parse(f"2022-{str(month).zfill(2)}-01")
    end = pendulum.parse(f"2023-{str(month).zfill(2)}-01")  # One year exactly
    assert (end - start).in_months() == 12


@pytest.mark.parametrize("day", range(1, 29))
def test_in_months_february(day):
    start = pendulum.parse(f"2022-02-04")
    end_1 = pendulum.parse(f"2023-02-{str(day).zfill(2)}")
    end_2 = end_1.add(days=1)
    m_diff_1 = (end_1 - start).in_months()
    m_diff_2 = (end_2 - start).in_months()
    assert m_diff_1 <= m_diff_2