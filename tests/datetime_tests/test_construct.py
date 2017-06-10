import os
import pytz
from datetime import datetime, timedelta
from dateutil import tz
from pendulum import DateTime, PRE_TRANSITION, POST_TRANSITION
from pendulum.tz import timezone
from pendulum.tz.timezone_info import TimezoneInfo
from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def tearDown(self):
        super(ConstructTest, self).tearDown()

        if os.getenv('TZ'):
            del os.environ['TZ']

    def test_creates_an_instance_default_to_utcnow(self):
        now = DateTime.utcnow()
        p = DateTime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.assertIsInstanceOfDateTime(p)
        self.assertEqual(p.timezone_name, now.timezone_name)

        self.assertDateTime(p, now.year, now.month, now.day, now.hour, now.minute, now.second)

    def test_setting_timezone(self):
        tz = 'Europe/London'
        dtz = timezone(tz)
        dt = datetime.utcnow()
        offset = dtz.convert(dt).tzinfo.offset / 3600

        p = DateTime(dt.year, dt.month, dt.day, tzinfo=dtz)
        self.assertEqual(tz, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_setting_timezone_with_string(self):
        tz = 'Europe/London'
        dtz = timezone(tz)
        dt = datetime.utcnow()
        offset = dtz.convert(dt).tzinfo.offset / 3600

        p = DateTime(dt.year, dt.month, dt.day, tzinfo=tz)
        self.assertEqual(tz, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_today(self):
        today = DateTime.today()
        self.assertIsInstanceOfDateTime(today)

    def test_tomorrow(self):
        now = DateTime.now().start_of('day')
        tomorrow = DateTime.tomorrow()
        self.assertIsInstanceOfDateTime(tomorrow)
        self.assertEqual(1, now.diff(tomorrow).in_days())

    def test_yesterday(self):
        now = DateTime.now().start_of('day')
        yesterday = DateTime.yesterday()
        self.assertIsInstanceOfDateTime(yesterday)
        self.assertEqual(-1, now.diff(yesterday, False).in_days())

    def test_instance_naive_datetime_defaults_to_utc(self):
        now = DateTime.instance(datetime.now())
        self.assertEqual('UTC', now.timezone_name)

    def test_instance_timezone_aware_datetime(self):
        now = DateTime.instance(
            datetime.now(TimezoneInfo(timezone('Europe/Paris'), 7200, True, timedelta(0, 3600), 'EST'))
        )
        self.assertEqual('Europe/Paris', now.timezone_name)

    def test_instance_timezone_aware_datetime_pytz(self):
        now = DateTime.instance(
            datetime.now(pytz.timezone('Europe/Paris'))
        )
        self.assertEqual('Europe/Paris', now.timezone_name)

    def test_instance_timezone_aware_datetime_any_tzinfo(self):
        dt = datetime(2016, 8, 7, 12, 34, 56, tzinfo=tz.gettz('Europe/Paris'))
        now = DateTime.instance(dt)
        self.assertEqual('+02:00', now.timezone_name)

    def test_now(self):
        now = DateTime.now('America/Toronto')
        in_paris = DateTime.now('Europe/Paris')

        self.assertNotEqual(now.hour, in_paris.hour)

    def test_now_with_fixed_offset(self):
        now = DateTime.now(6)

        self.assertEqual(now.timezone_name, '+06:00')

    def test_create(self):
        with self.wrap_with_test_now(DateTime(2016, 8, 7, 12, 34, 56)):
            now = DateTime.now()
            d = DateTime.create()
            self.assertDateTime(d, now.year, now.month, now.day, 0, 0, 0, 0)

            d = DateTime.create(year=1975)
            self.assertDateTime(d, 1975, now.month, now.day, 0, 0, 0, 0)

            d = DateTime.create(month=11)
            self.assertDateTime(d, now.year, 11, now.day, 0, 0, 0, 0)

            d = DateTime.create(day=27)
            self.assertDateTime(d, now.year, now.month, 27, 0, 0, 0, 0)

            d = DateTime.create(hour=12)
            self.assertDateTime(d, now.year, now.month, now.day, 12, 0, 0, 0)

            d = DateTime.create(minute=12)
            self.assertDateTime(d, now.year, now.month, now.day, 0, 12, 0, 0)

            d = DateTime.create(second=12)
            self.assertDateTime(d, now.year, now.month, now.day, 0, 0, 12, 0)

            d = DateTime.create(microsecond=123456)
            self.assertDateTime(d, now.year, now.month, now.day, 0, 0, 0, 123456)

    def test_create_with_not_transition_timezone(self):
        dt = DateTime.create(tz='Etc/UTC')

        self.assertEqual('Etc/UTC', dt.timezone_name)

    def test_create_maintains_microseconds(self):
        d = DateTime.create(2016, 11, 12, 2, 9, 39, 594000, 'America/Panama')
        self.assertDateTime(d, 2016, 11, 12, 2, 9, 39, 594000)

        d = DateTime.create(2316, 11, 12, 2, 9, 39, 857, 'America/Panama')
        self.assertDateTime(d, 2316, 11, 12, 2, 9, 39, 857)

    def test_init_fold_is_honored_if_explicit(self):
        d = DateTime(2013, 3, 31, 2, 30, tzinfo='Europe/Paris')
        # Default value of None for DateTime instances
        # so default rule will be applied
        self.assertDateTime(d, 2013, 3, 31, 3, 30)

        DateTime.set_transition_rule(PRE_TRANSITION)

        d = DateTime(2013, 3, 31, 2, 30, tzinfo='Europe/Paris')
        self.assertDateTime(d, 2013, 3, 31, 1, 30)

        DateTime.set_transition_rule(POST_TRANSITION)

        d = DateTime(2013, 3, 31, 2, 30, tzinfo='Europe/Paris', fold=0)
        self.assertDateTime(d, 2013, 3, 31, 1, 30)
        self.assertEqual(d.fold, 0)

        d = DateTime(2013, 3, 31, 2, 30, tzinfo='Europe/Paris', fold=1)
        self.assertDateTime(d, 2013, 3, 31, 3, 30)
        self.assertEqual(d.fold, 1)
