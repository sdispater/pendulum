# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pendulum


locale = 'id'


def test_diff_for_humans():
    with pendulum.test(pendulum.datetime(2016, 8, 29)):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == 'beberapa menit lalu'

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == 'beberapa menit lalu'

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == '1 menit yang lalu'

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == '2 menit yang lalu'

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == '1 jam yang lalu'

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == '2 jam yang lalu'

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == '1 hari yang lalu'

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == '2 hari yang lalu'

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == '1 minggu yang lalu'

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == '2 minggu yang lalu'

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == '1 bulan yang lalu'

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == '2 bulan yang lalu'

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == '1 tahun yang lalu'

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == '2 tahun yang lalu'

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == 'dalam beberapa menit'

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == 'beberapa menit kemudian'
    assert d2.diff_for_humans(d, locale=locale) == 'beberapa menit yang lalu'

    assert d.diff_for_humans(d2, True, locale=locale) == 'beberapa menit'
    assert d2.diff_for_humans(d.add(seconds=1), True,
                              locale=locale) == 'beberapa menit'
