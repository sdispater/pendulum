from __future__ import annotations

import pendulum

locale = "fo"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1 sekund síðan"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "2 sekund síðan"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 minutt síðan"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 minuttir síðan"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 tími síðan"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 tímar síðan"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 dagur síðan"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 dagar síðan"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 vika síðan"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 vikur síðan"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 mánað síðan"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 mánaðir síðan"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 ár síðan"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 ár síðan"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "um 1 sekund"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1 sekund aftaná"
    assert d2.diff_for_humans(d, locale=locale) == "1 sekund áðrenn"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 sekund"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 sekundir"
