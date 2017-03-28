# -*- coding: utf-8 -*-

from pendulum import DateTime

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class KoTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'ko'

    def diff_for_humans(self):
        d = DateTime.now().subtract(seconds=1)
        self.assertEqual('1 초 전', d.diff_for_humans())

        d = DateTime.now().subtract(seconds=2)
        self.assertEqual('2 초 전', d.diff_for_humans())

        d = DateTime.now().subtract(minutes=1)
        self.assertEqual('1 분 전', d.diff_for_humans())

        d = DateTime.now().subtract(minutes=2)
        self.assertEqual('2 분 전', d.diff_for_humans())

        d = DateTime.now().subtract(hours=1)
        self.assertEqual('1 시간 전', d.diff_for_humans())

        d = DateTime.now().subtract(hours=2)
        self.assertEqual('2 시간 전', d.diff_for_humans())

        d = DateTime.now().subtract(days=1)
        self.assertEqual('1 일 전', d.diff_for_humans())

        d = DateTime.now().subtract(days=2)
        self.assertEqual('2 일 전', d.diff_for_humans())

        d = DateTime.now().subtract(weeks=1)
        self.assertEqual('1 주일 전', d.diff_for_humans())

        d = DateTime.now().subtract(weeks=2)
        self.assertEqual('2 주일 전', d.diff_for_humans())

        d = DateTime.now().subtract(months=1)
        self.assertEqual('1 개월 전', d.diff_for_humans())

        d = DateTime.now().subtract(months=2)
        self.assertEqual('2 개월 전', d.diff_for_humans())

        d = DateTime.now().subtract(years=1)
        self.assertEqual('1 년 전', d.diff_for_humans())

        d = DateTime.now().subtract(years=2)
        self.assertEqual('2 년 전', d.diff_for_humans())

        d = DateTime.now().add(seconds=1)
        self.assertEqual('1 초 후', d.diff_for_humans())

        d = DateTime.now().add(seconds=1)
        d2 = DateTime.now()
        self.assertEqual('1 초 뒤', d.diff_for_humans(d2))
        self.assertEqual('1 초 앞', d2.diff_for_humans(d))

        self.assertEqual('1 초', d.diff_for_humans(d2, True))
        self.assertEqual('2 초', d2.diff_for_humans(d.add(seconds=1), True))
