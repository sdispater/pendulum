from __future__ import annotations

import pendulum

locale = "fa"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1 ثانیه پیش"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "2 ثانیه پیش"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 دقیقه پیش"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 دقیقه پیش"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 ساعت پیش"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 ساعت پیش"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 روز پیش"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 روز پیش"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 هفته پیش"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 هفته پیش"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 ماه پیش"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 ماه پیش"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 سال پیش"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 سال پیش"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1 ثانیه بعد"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1 ثانیه پس از"
    assert d2.diff_for_humans(d, locale=locale) == "1 ثانیه پیش از"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 ثانیه"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 ثانیه"
