import pendulum


locale = 'ko'


def test_diff_for_humans():
    with pendulum.test(pendulum.create(2016, 8, 29)):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == '1 초 전'

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == '2 초 전'

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == '1 분 전'

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == '2 분 전'

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == '1 시간 전'

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == '2 시간 전'

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == '1 일 전'

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == '2 일 전'

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == '1 주일 전'

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == '2 주일 전'

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == '1 개월 전'

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == '2 개월 전'

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == '1 년 전'

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == '2 년 전'

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == '1 초 후'

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == '1 초 뒤'
    assert d2.diff_for_humans(d, locale=locale) == '1 초 앞'

    assert d.diff_for_humans(d2, True, locale=locale) == '1 초'
    assert d2.diff_for_humans(d.add(seconds=1), True,
                              locale=locale) == '2 초'
