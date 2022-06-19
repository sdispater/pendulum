from __future__ import annotations

import pendulum

locale = "sk"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "pred 1 sekundou"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "o 1 sekundu"

    d = pendulum.now().add(seconds=2)
    assert d.diff_for_humans(locale=locale) == "o 2 sekundy"

    d = pendulum.now().add(seconds=5)
    assert d.diff_for_humans(locale=locale) == "o 5 sekúnd"

    d = pendulum.now().subtract(seconds=20)
    assert d.diff_for_humans(locale=locale) == "pred 20 sekundami"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "pred 1 minútou"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "pred 2 minútami"

    d = pendulum.now().add(minutes=5)
    assert d.diff_for_humans(locale=locale) == "o 5 minút"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "pred 1 hodinou"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "pred 2 hodinami"

    d = pendulum.now().subtract(hours=5)
    assert d.diff_for_humans(locale=locale) == "pred 5 hodinami"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "pred 1 dňom"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "pred 2 dňami"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "pred 1 týždňom"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "pred 2 týždňami"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "pred 1 mesiacom"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "pred 2 mesiacmi"

    d = pendulum.now().subtract(months=5)
    assert d.diff_for_humans(locale=locale) == "pred 5 mesiacmi"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "pred 1 rokom"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "pred 2 rokmi"

    d = pendulum.now().subtract(years=5)
    assert d.diff_for_humans(locale=locale) == "pred 5 rokmi"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1 sekunda po"
    assert d2.diff_for_humans(d, locale=locale) == "1 sekunda pred"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 sekunda"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 sekundy"

    d = pendulum.now().add(seconds=20)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "20 sekúnd po"
    assert d2.diff_for_humans(d, locale=locale) == "20 sekúnd pred"

    d = pendulum.now().add(seconds=10)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, True, locale=locale) == "10 sekúnd"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "11 sekúnd"


def test_format():
    d = pendulum.datetime(2016, 8, 29, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "pondelok"
    assert d.format("ddd", locale=locale) == "po"
    assert d.format("MMMM", locale=locale) == "augusta"
    assert d.format("MMM", locale=locale) == "aug"
    assert d.format("A", locale=locale) == "AM"
    assert d.format("Qo", locale=locale) == "3"
    assert d.format("Mo", locale=locale) == "8"
    assert d.format("Do", locale=locale) == "29"

    assert d.format("LT", locale=locale) == "07:03"
    assert d.format("LTS", locale=locale) == "07:03:06"
    assert d.format("L", locale=locale) == "29.08.2016"
    assert d.format("LL", locale=locale) == "29. augusta 2016"
    assert d.format("LLL", locale=locale) == "29. augusta 2016 07:03"
    assert d.format("LLLL", locale=locale) == "pondelok, 29. augusta 2016 07:03"
