# -*- coding: utf-8 -*-

from datetime import datetime, date, time
from pendulum.helpers import precise_diff, parse_iso8601
from pendulum.tz.timezone import FixedTimezone

from . import AbstractTestCase


class HelpersTestCase(AbstractTestCase):

    def test_precise_diff(self):
        dt1 = datetime(2003, 3, 1, 0, 0, 0)
        dt2 = datetime(2003, 1, 31, 23, 59, 59)

        diff = precise_diff(dt1, dt2)
        self.assert_diff(diff, months=-1, seconds=-1)

        diff = precise_diff(dt2, dt1)
        self.assert_diff(diff, months=1, seconds=1)

        dt1 = datetime(2012, 3, 1, 0, 0, 0)
        dt2 = datetime(2012, 1, 31, 23, 59, 59)

        diff = precise_diff(dt1, dt2)
        self.assert_diff(diff, months=-1, seconds=-1)

        diff = precise_diff(dt2, dt1)
        self.assert_diff(diff, months=1, seconds=1)

        dt1 = datetime(2001, 1, 1)
        dt2 = datetime(2003, 9, 17, 20, 54, 47, 282310)

        diff = precise_diff(dt1, dt2)
        self.assert_diff(
            diff,
            years=2, months=8, days=16,
            hours=20, minutes=54, seconds=47, microseconds=282310
        )

        dt1 = datetime(2017, 2, 17, 16, 5, 45, 123456)
        dt2 = datetime(2018, 2, 17, 16, 5, 45, 123256)

        diff = precise_diff(dt1, dt2)
        self.assert_diff(
            diff,
            months=11, days=30, hours=23, minutes=59, seconds=59, microseconds=999800
        )

    def test_parse_iso8601(self):
        if not parse_iso8601:
            self.skipTest('parse_iso8601 is only supported with C extensions.')

        from pendulum._extensions._helpers import TZFixedOffset

        # Date
        self.assertEqual(date(2016, 1, 1), parse_iso8601('2016'))
        self.assertEqual(date(2016, 10, 1), parse_iso8601('2016-10'))
        self.assertEqual(date(2016, 10, 6), parse_iso8601('2016-10-06'))
        self.assertEqual(date(2016, 10, 6), parse_iso8601('20161006'))

        # Time
        self.assertEqual(time(20, 16, 10, 0), parse_iso8601('201610'))

        # Datetime
        self.assertEqual(datetime(2016, 10, 6, 12, 34, 56, 123456), parse_iso8601('2016-10-06T12:34:56.123456'))
        self.assertEqual(datetime(2016, 10, 6, 12, 34, 56, 123000), parse_iso8601('2016-10-06T12:34:56.123'))
        self.assertEqual(datetime(2016, 10, 6, 12, 34, 56, 123), parse_iso8601('2016-10-06T12:34:56.000123'))
        self.assertEqual(datetime(2016, 10, 6, 12, 0, 0, 0), parse_iso8601('2016-10-06T12'))
        self.assertEqual(datetime(2016, 10, 6, 12, 34, 56, 0), parse_iso8601('2016-10-06T123456'))
        self.assertEqual(datetime(2016, 10, 6, 12, 34, 56, 123456), parse_iso8601('2016-10-06T123456.123456'))
        self.assertEqual(datetime(2016, 10, 6, 12, 34, 56, 123456), parse_iso8601('20161006T123456.123456'))
        self.assertEqual(datetime(2016, 10, 6, 12, 34, 56, 123456), parse_iso8601('20161006 123456.123456'))

        # Datetime with offset
        self.assertEqual(
            datetime(2016, 10, 6, 12, 34, 56, 123456, TZFixedOffset(19800)),
            parse_iso8601('2016-10-06T12:34:56.123456+05:30')
        )
        self.assertEqual(
            datetime(2016, 10, 6, 12, 34, 56, 123456, TZFixedOffset(19800)),
            parse_iso8601('2016-10-06T12:34:56.123456+0530')
        )
        self.assertEqual(
            datetime(2016, 10, 6, 12, 34, 56, 123456, TZFixedOffset(-19800)),
            parse_iso8601('2016-10-06T12:34:56.123456-05:30')
        )
        self.assertEqual(
            datetime(2016, 10, 6, 12, 34, 56, 123456, TZFixedOffset(-19800)),
            parse_iso8601('2016-10-06T12:34:56.123456-0530')
        )
        self.assertEqual(
            datetime(2016, 10, 6, 12, 34, 56, 123456, TZFixedOffset(18000)),
            parse_iso8601('2016-10-06T12:34:56.123456+05')
        )
        self.assertEqual(
            datetime(2016, 10, 6, 12, 34, 56, 123456, TZFixedOffset(-18000)),
            parse_iso8601('2016-10-06T12:34:56.123456-05')
        )
        self.assertEqual(
            datetime(2016, 10, 6, 12, 34, 56, 123456, TZFixedOffset(-18000)),
            parse_iso8601('20161006T123456,123456-05')
        )
        self.assertEqual(
            datetime(2016, 10, 6, 12, 34, 56, 123456, TZFixedOffset(+19800)),
            parse_iso8601('2016-10-06T12:34:56.123456789+05:30')
        )

        # Ordinal date
        self.assertEqual(date(2012, 1, 7), parse_iso8601('2012-007'))
        self.assertEqual(date(2012, 1, 7), parse_iso8601('2012007'))
        self.assertEqual(date(2017, 3, 20), parse_iso8601('2017-079'))

        # Week date
        self.assertEqual(date(2012, 1, 30), parse_iso8601('2012-W05'))
        self.assertEqual(date(2008, 9, 27), parse_iso8601('2008-W39-6'))
        self.assertEqual(date(2010, 1, 3), parse_iso8601('2009-W53-7'))
        self.assertEqual(date(2008, 12, 29), parse_iso8601('2009-W01-1'))

        # Week date wth time
        self.assertEqual(datetime(2008, 9, 27, 9, 0, 0, 0), parse_iso8601('2008-W39-6T09'))

    def test_parse_ios8601_invalid(self):
        if not parse_iso8601:
            self.skipTest('parse_iso8601 is only supported with C extensions.')

        # Invalid month
        self.assertRaises(ValueError, parse_iso8601, '20161306T123456')

        # Invalid day
        self.assertRaises(ValueError, parse_iso8601, '20161033T123456')

        # Invalid day for month
        self.assertRaises(ValueError, parse_iso8601, '20161131T123456')

        # Invalid hour
        self.assertRaises(ValueError, parse_iso8601, '20161006T243456')

        # Invalid minute
        self.assertRaises(ValueError, parse_iso8601, '20161006T126056')

        # Invalid second
        self.assertRaises(ValueError, parse_iso8601, '20161006T123460')

        # Extraneous separator
        self.assertRaises(ValueError, parse_iso8601, '20140203 04:05:.123456')
        self.assertRaises(ValueError, parse_iso8601, '2009-05-19 14:')

        # Invalid ordinal
        self.assertRaises(ValueError, parse_iso8601, '2009367')
        self.assertRaises(ValueError, parse_iso8601, '2009-367')
        self.assertRaises(ValueError, parse_iso8601, '2015-366')
        self.assertRaises(ValueError, parse_iso8601, '2015-000')

        # Invalid date
        self.assertRaises(ValueError, parse_iso8601, '2009-')

        # Invalid time
        self.assertRaises(ValueError, parse_iso8601, '2009-05-19T14:3924')
        self.assertRaises(ValueError, parse_iso8601, '2010-02-18T16.5:23.35:48')
        self.assertRaises(ValueError, parse_iso8601, '2010-02-18T16:23.35:48.45')
        self.assertRaises(ValueError, parse_iso8601, '2010-02-18T16:23.33.600')

        # Invalid offset
        self.assertRaises(ValueError, parse_iso8601, '2009-05-19 14:39:22+063')
        self.assertRaises(ValueError, parse_iso8601, '2009-05-19 14:39:22+06a00')
        self.assertRaises(ValueError, parse_iso8601, '2009-05-19 14:39:22+0:6:00')

        # Missing time separator
        self.assertRaises(ValueError, parse_iso8601, '2009-05-1914:39')

        # Invalid week date
        self.assertRaises(ValueError, parse_iso8601, '2012-W63')
        self.assertRaises(ValueError, parse_iso8601, '2012-W12-9')
        self.assertRaises(ValueError, parse_iso8601, '2012W12-3')  # Missing separator
        self.assertRaises(ValueError, parse_iso8601, '2012-W123')  # Missing separator

    def assert_diff(self, diff,
                    years=0, months=0, days=0,
                    hours=0, minutes=0, seconds=0, microseconds=0):
        self.assertEqual(diff['years'], years)
        self.assertEqual(diff['months'], months)
        self.assertEqual(diff['days'], days)
        self.assertEqual(diff['hours'], hours)
        self.assertEqual(diff['minutes'], minutes)
        self.assertEqual(diff['seconds'], seconds)
        self.assertEqual(diff['microseconds'], microseconds)
