import os
import pytz

import pendulum
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
        now = pendulum.utcnow()
        p = pendulum.create(
            now.year, now.month, now.day,
            now.hour, now.minute, now.second
        )
        self.assertIsInstanceOfDateTime(p)
        self.assertEqual(p.timezone_name, now.timezone_name)

        self.assertDateTime(p, now.year, now.month, now.day, now.hour, now.minute, now.second)

    def test_setting_timezone(self):
        tz = 'Europe/London'
        dtz = timezone(tz)
        dt = datetime.utcnow()
        offset = dtz.convert(dt).tzinfo.offset / 3600

        p = pendulum.create(dt.year, dt.month, dt.day, tz=dtz)
        self.assertEqual(tz, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_setting_timezone_with_string(self):
        tz = 'Europe/London'
        dtz = timezone(tz)
        dt = datetime.utcnow()
        offset = dtz.convert(dt).tzinfo.offset / 3600

        p = pendulum.create(dt.year, dt.month, dt.day, tz=tz)
        self.assertEqual(tz, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_today(self):
        today = DateTime.today()
        self.assertIsInstanceOfDateTime(today)

    def test_tomorrow(self):
        now = pendulum.now().start_of('day')
        tomorrow = DateTime.tomorrow()
        self.assertIsInstanceOfDateTime(tomorrow)
        self.assertEqual(1, now.diff(tomorrow).in_days())

    def test_yesterday(self):
        now = pendulum.now().start_of('day')
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
        now = pendulum.now('America/Toronto')
        in_paris = pendulum.now('Europe/Paris')

        self.assertNotEqual(now.hour, in_paris.hour)

    def test_now_with_fixed_offset(self):
        now = pendulum.now(6)

        self.assertEqual(now.timezone_name, '+06:00')

    def test_create(self):
        with self.wrap_with_test_now(DateTime(2016, 8, 7, 12, 34, 56)):
            now = pendulum.now()
            d = pendulum.create()
            self.assertDateTime(d, now.year, now.month, now.day, 0, 0, 0, 0)

            d = pendulum.create(year=1975)
            self.assertDateTime(d, 1975, now.month, now.day, 0, 0, 0, 0)

            d = pendulum.create(month=11)
            self.assertDateTime(d, now.year, 11, now.day, 0, 0, 0, 0)

            d = pendulum.create(day=27)
            self.assertDateTime(d, now.year, now.month, 27, 0, 0, 0, 0)

            d = pendulum.create(hour=12)
            self.assertDateTime(d, now.year, now.month, now.day, 12, 0, 0, 0)

            d = pendulum.create(minute=12)
            self.assertDateTime(d, now.year, now.month, now.day, 0, 12, 0, 0)

            d = pendulum.create(second=12)
            self.assertDateTime(d, now.year, now.month, now.day, 0, 0, 12, 0)

            d = pendulum.create(microsecond=123456)
            self.assertDateTime(d, now.year, now.month, now.day, 0, 0, 0, 123456)

    def test_create_with_not_transition_timezone(self):
        dt = pendulum.create(tz='Etc/UTC')

        self.assertEqual('Etc/UTC', dt.timezone_name)

    def test_create_maintains_microseconds(self):
        d = pendulum.create(2016, 11, 12, 2, 9, 39, 594000, 'America/Panama')
        self.assertDateTime(d, 2016, 11, 12, 2, 9, 39, 594000)

        d = pendulum.create(2316, 11, 12, 2, 9, 39, 857, 'America/Panama')
        self.assertDateTime(d, 2316, 11, 12, 2, 9, 39, 857)

    def test_second_inaccuracy_on_past_datetimes(self):
        dt = pendulum.create(1901, 12, 13, 0, 0, 0, 555555, tz='US/Central')

        self.assertDateTime(dt, 1901, 12, 13, 0, 0, 0, 555555)
