# -*- coding: utf-8 -*-

from pendulum import PendulumInterval

from .. import AbstractTestCase


class ForHumansTest(AbstractTestCase):

    def setUp(self):
        super(ForHumansTest, self).setUp()

        PendulumInterval.set_locale('en')

    def test_week(self):
        self.assertEqual('52 weeks', PendulumInterval(days=364).in_words())
        self.assertEqual('1 week', PendulumInterval(days=7).in_words())

    def test_week_to_string(self):
        self.assertEqual('52 weeks', str(PendulumInterval(days=364)))
        self.assertEqual('1 week', str(PendulumInterval(days=7)))

    def test_weeks_and_day(self):
        self.assertEqual('52 weeks 1 day', PendulumInterval(days=365).in_words())

    def test_all(self):
        pi = PendulumInterval(days=1177, seconds=7284, microseconds=1000000)
        self.assertEqual(
            '168 weeks 1 day 2 hours 1 minute 25 seconds',
            pi.in_words()
        )

    def test_in_french(self):
        pi = PendulumInterval(days=1177, seconds=7284, microseconds=1000000)
        self.assertEqual(
            '168 semaines 1 jour 2 heures 1 minute 25 secondes',
            pi.in_words(locale='fr')
        )

    def test_repr(self):
        pi = PendulumInterval(days=1177, seconds=7284, microseconds=1000000)
        self.assertEqual(
            '168 weeks 1 day 2 hours 1 minute 25 seconds',
            repr(pi)
        )
