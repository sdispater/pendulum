from pendulum import Duration

from .. import AbstractTestCase


class ForHumansTest(AbstractTestCase):

    def test_week(self):
        self.assertEqual('52 weeks', Duration(days=364).in_words())
        self.assertEqual('1 week', Duration(days=7).in_words())

    def test_week_to_string(self):
        self.assertEqual('52 weeks', str(Duration(days=364)))
        self.assertEqual('1 week', str(Duration(days=7)))

    def test_weeks_and_day(self):
        self.assertEqual('52 weeks 1 day', Duration(days=365).in_words())

    def test_all(self):
        pi = Duration(days=1177, seconds=7284, microseconds=1000000)
        self.assertEqual(
            '168 weeks 1 day 2 hours 1 minute 25 seconds',
            pi.in_words()
        )

    def test_in_french(self):
        pi = Duration(days=1177, seconds=7284, microseconds=1000000)
        self.assertEqual(
            '168 semaines 1 jour 2 heures 1 minute 25 secondes',
            pi.in_words(locale='fr')
        )

    def test_repr(self):
        pi = Duration(days=1177, seconds=7284, microseconds=1000000)
        self.assertEqual(
            '<Duration [168 weeks 1 day 2 hours 1 minute 25 seconds]>',
            repr(pi)
        )

    def test_singluar_negative_values(self):
        pi = Duration(days=-1)
        self.assertEqual(
            '-1 day',
            pi.in_words()
        )

    def test_separator(self):
        pi = Duration(days=1177, seconds=7284, microseconds=1000000)
        self.assertEqual(
            '168 weeks, 1 day, 2 hours, 1 minute, 25 seconds',
            pi.in_words(separator=', ')
        )

    def test_subseconds(self):
        pi = Duration(microseconds=123456)

        self.assertEqual(
            '0.12 second',
            pi.in_words()
        )

    def test_subseconds_with_seconds(self):
        pi = Duration(seconds=12, microseconds=123456)

        self.assertEqual(
            '12 seconds',
            pi.in_words()
        )
