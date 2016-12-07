# -*- coding: utf-8 -*-

import pickle
import pendulum
from datetime import datetime, date, time, timedelta
from pendulum import Pendulum, timezone
from .. import AbstractTestCase


class BehaviorTest(AbstractTestCase):

    def setUp(self):
        super(BehaviorTest, self).setUp()

        self.p = Pendulum(2016, 8, 27, 12, 34, 56, 123456, 'Europe/Paris')
        self.p1 = self.p.in_tz('America/New_York')
        self.tz = timezone('Europe/Paris')
        self.d = self.tz.convert(datetime(2016, 8, 27, 12, 34, 56, 123456))

    def test_timetuple(self):
        self.assertEqual(self.d.timetuple(), self.p.timetuple())

    def test_utctimetuple(self):
        self.assertEqual(self.d.utctimetuple(), self.p.utctimetuple())

    def test_date(self):
        self.assertEqual(self.d.date(), self.p.date())

    def test_time(self):
        self.assertEqual(self.p.time(), self.d.time())

    def test_timetz(self):
        self.assertEqual(self.d.timetz(), self.p.timetz())

    def test_astimezone(self):
        self.assertEqual(self.d.astimezone(self.p1.tzinfo), self.p.astimezone(self.p1.tzinfo))

    def test_ctime(self):
        self.assertEqual(self.d.ctime(), self.p.ctime())

    def test_isoformat(self):
        self.assertEqual(self.d.isoformat(), self.p.isoformat())

    def test_utcoffset(self):
        self.assertEqual(self.d.utcoffset(), self.p.utcoffset())

    def test_tzname(self):
        self.assertEqual(self.d.tzname(), self.p.tzname())

    def test_dst(self):
        self.assertEqual(self.d.dst(), self.p.dst())

    def test_toordinal(self):
        self.assertEqual(self.d.toordinal(), self.p.toordinal())

    def test_weekday(self):
        self.assertEqual(self.d.weekday(), self.p.weekday())

    def test_isoweekday(self):
        self.assertEqual(self.d.isoweekday(), self.p.isoweekday())

    def test_isocalendar(self):
        self.assertEqual(self.d.isocalendar(), self.p.isocalendar())

    def test_fromtimestamp(self):
        self.assertEqual(datetime.fromtimestamp(0, pendulum.UTC), pendulum.fromtimestamp(0, pendulum.UTC))

    def test_utcfromtimestamp(self):
        self.assertEqual(datetime.utcfromtimestamp(0), pendulum.utcfromtimestamp(0))

    def test_fromordinal(self):
        self.assertEqual(datetime.fromordinal(730120), pendulum.fromordinal(730120))

    def test_combine(self):
        self.assertEqual(
            datetime.combine(date(2016, 1, 1), time(1, 2, 3, 123456)),
            pendulum.combine(date(2016, 1, 1), time(1, 2, 3, 123456))
        )

    def test_hash(self):
        dt1 = Pendulum(2016, 8, 27, 12, 34, 56, 123456, 'Europe/Paris')
        dt2 = Pendulum(2016, 8, 27, 12, 34, 56, 123456, 'Europe/Paris')
        dt3 = Pendulum(2016, 8, 27, 12, 34, 56, 123456, 'America/Toronto')

        self.assertEqual(hash(dt1), hash(dt2))
        self.assertNotEqual(hash(dt1), hash(dt3))

    def test_pickle(self):
        dt1 = Pendulum(2016, 8, 27, 12, 34, 56, 123456, 'Europe/Paris')
        s = pickle.dumps(dt1)
        dt2 = pickle.loads(s)

        self.assertEqual(dt1, dt2)

    def test_pickle_with_integer_tzinfo(self):
        dt1 = Pendulum(2016, 8, 27, 12, 34, 56, 123456, 0)
        s = pickle.dumps(dt1)
        dt2 = pickle.loads(s)

        self.assertEqual(dt1, dt2)

    def test_proper_dst(self):
        dt = pendulum.create(1941, 7, 1, tz='Europe/Amsterdam')

        self.assertEqual(timedelta(0, 6000), dt.dst())
