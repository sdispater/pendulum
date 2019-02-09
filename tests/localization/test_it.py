# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pendulum


locale = "it"


def test_diff_for_humans():
    with pendulum.test(pendulum.datetime(2016, 8, 29)):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "qualche secondo fa"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "qualche secondo fa"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 minuto fa"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 minuti fa"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 ora fa"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 ore fa"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 giorno fa"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 giorni fa"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 settimana fa"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 settimane fa"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 mese fa"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 mesi fa"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 anno fa"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 anni fa"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "tra qualche secondo"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "qualche secondo dopo"
    assert d2.diff_for_humans(d, locale=locale) == "qualche secondo prima"

    assert d.diff_for_humans(d2, True, locale=locale) == "qualche secondo"
    assert (
        d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "qualche secondo"
    )
