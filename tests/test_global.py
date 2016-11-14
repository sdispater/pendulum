# -*- coding: utf-8 -*-

import pendulum
from . import AbstractTestCase


class GlobalTest(AbstractTestCase):

    def test_set_test_now_is_global(self):
        now = pendulum.create(2000, 11, 10, 12, 34, 56, 123456)
        pendulum.set_test_now(now)

        self.assertEqual(now, pendulum.get_test_now())
        self.assertEqual(now, pendulum.Pendulum.get_test_now())
        self.assertEqual(now.date(), pendulum.Date.get_test_now())
        self.assertEqual(now.time(), pendulum.Time.get_test_now())

        self.assertPendulum(
            pendulum.Pendulum.now(),
            2000, 11, 10, 12, 34, 56, 123456
        )
        self.assertDate(
            pendulum.Date.today(),
            2000, 11, 10
        )
        self.assertTime(
            pendulum.Time.now(),
            12, 34, 56, 123456
        )

    def test_set_test_now_can_be_overridden(self):
        now = pendulum.create(2000, 11, 10, 12, 34, 56, 123456)
        pendulum.set_test_now(now)

        dt = pendulum.create(2001, 12, 11, 1, 2, 3, 987654)
        pendulum.Pendulum.set_test_now(dt)
        pendulum.Date.set_test_now(dt)
        pendulum.Time.set_test_now(dt)

        self.assertEqual(now, pendulum.get_test_now())
        self.assertEqual(dt, pendulum.Pendulum.get_test_now())
        self.assertEqual(dt.date(), pendulum.Date.get_test_now())
        self.assertEqual(dt.time(), pendulum.Time.get_test_now())

        self.assertPendulum(
            pendulum.Pendulum.now(),
            2001, 12, 11, 1, 2, 3, 987654
        )
        self.assertDate(
            pendulum.Date.today(),
            2001, 12, 11
        )
        self.assertTime(
            pendulum.Time.now(),
            1, 2, 3, 987654
        )

    def test_set_formatter_is_global(self):
        dt = pendulum.create(2000, 11, 10, 12, 34, 56, 123456)
        pendulum.set_formatter('alternative')

        self.assertEqual(pendulum.Pendulum.get_formatter(), 'alternative')
        self.assertEqual(pendulum.Date.get_formatter(), 'alternative')
        self.assertEqual(pendulum.Time.get_formatter(), 'alternative')

        self.assertEqual(
            dt.format('YYYY-MM-DD HH:mm:ss.SSSSSSZZ'),
            '2000-11-10 12:34:56.123456+00:00'
        )
        self.assertEqual(
            dt.date().format('YYYY-MM-DD'),
            '2000-11-10'
        )
        self.assertEqual(
            dt.time().format('HH:mm:ss.SSSSSS'),
            '12:34:56.123456'
        )

    def test_set_formatter_can_be_overridien(self):
        dt = pendulum.create(2000, 11, 10, 12, 34, 56, 123456)
        pendulum.set_formatter('alternative')

        pendulum.Pendulum.set_formatter()
        pendulum.Date.set_formatter()
        pendulum.Time.set_formatter()

        self.assertEqual(pendulum.Pendulum.get_formatter(), 'classic')
        self.assertEqual(pendulum.Date.get_formatter(), 'classic')
        self.assertEqual(pendulum.Time.get_formatter(), 'classic')

        self.assertEqual(
            dt.format('YYYY-MM-DD HH:mm:ss.SSSSSSZZ'),
            'YYYY-MM-DD HH:mm:ss.SSSSSSZZ'
        )
        self.assertEqual(
            dt.date().format('YYYY-MM-DD'),
            'YYYY-MM-DD'
        )
        self.assertEqual(
            dt.time().format('HH:mm:ss.SSSSSS'),
            'HH:mm:ss.SSSSSS'
        )

    def test_set_locale_is_global(self):
        dt = pendulum.create(2000, 11, 10, 12, 34, 56, 123456)
        pendulum.set_formatter('alternative')
        pendulum.set_locale('fr')

        self.assertEqual(pendulum.Pendulum.get_locale(), 'fr')
        self.assertEqual(pendulum.Date.get_locale(), 'fr')
        self.assertEqual(pendulum.Time.get_locale(), 'fr')

        self.assertEqual(
            dt.format('MMMM'),
            'novembre'
        )
        self.assertEqual(
            dt.date().format('MMMM'),
            'novembre'
        )

    def test_set_locale_can_be_overridden(self):

        dt = pendulum.create(2000, 11, 10, 12, 34, 56, 123456)
        pendulum.set_formatter('alternative')
        pendulum.set_locale('fr')

        pendulum.Pendulum.set_locale('en')
        pendulum.Date.set_locale('en')
        pendulum.Time.set_locale('en')

        self.assertEqual(pendulum.Pendulum.get_locale(), 'en')
        self.assertEqual(pendulum.Date.get_locale(), 'en')
        self.assertEqual(pendulum.Time.get_locale(), 'en')

        self.assertEqual(
            dt.format('MMMM'),
            'November'
        )
        self.assertEqual(
            dt.date().format('MMMM'),
            'November'
        )
