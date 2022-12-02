from __future__ import annotations

import pendulum

locale = "he"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "לפני כמה שניות"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "לפני כמה שניות"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "לפני דקה"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "לפני שתי דקות"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "לפני שעה"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "לפני שעתיים"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "לפני יום 1"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "לפני יומיים"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "לפני שבוע"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "לפני שבועיים"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "לפני חודש"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "לפני חודשיים"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "לפני שנה"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "לפני שנתיים"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "תוך כמה שניות"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "בעוד כמה שניות"
    assert d2.diff_for_humans(d, locale=locale) == "כמה שניות קודם"

    assert d.diff_for_humans(d2, True, locale=locale) == "כמה שניות"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "כמה שניות"
