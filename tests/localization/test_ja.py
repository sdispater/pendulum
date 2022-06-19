from __future__ import annotations

import pendulum

locale = "ja"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "数秒 前に"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "数秒 前に"

    d = pendulum.now().subtract(seconds=21)
    assert d.diff_for_humans(locale=locale) == "21 秒前"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 分前"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 分前"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 時間前"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 時間前"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 日前"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 日前"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 週間前"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 週間前"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 か月前"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 か月前"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 年前"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 年前"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "今から 数秒"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "数秒 後"
    assert d2.diff_for_humans(d, locale=locale) == "数秒 前"

    assert d.diff_for_humans(d2, True, locale=locale) == "数秒"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "数秒"
