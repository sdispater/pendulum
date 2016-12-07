# -*- coding: utf-8 -*-

from pendulum import Time
from .. import AbstractTestCase


class DiffTest(AbstractTestCase):

    def test_diff_in_hours_positive(self):
        dt = Time(12, 34, 56)
        self.assertEqual(3, dt.diff(dt.add(hours=2).add(seconds=3672)).in_hours())

    def test_diff_in_hours_negative_with_sign(self):
        dt = Time(12, 34, 56)
        self.assertEqual(-1, dt.diff(dt.subtract(hours=2).add(seconds=3600), False).in_hours())

    def test_diff_in_hours_negative_no_sign(self):
        dt = Time(12, 34, 56)
        self.assertEqual(1, dt.diff(dt.subtract(hours=2).add(seconds=3600)).in_hours())

    def test_diff_in_hours_vs_default_now(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual(2, Time.now().subtract(hours=2).diff().in_hours())

    def test_diff_in_hours_ensure_is_truncated(self):
        dt = Time(12, 34, 56)
        self.assertEqual(3, dt.diff(dt.add(hours=2).add(seconds=5401)).in_hours())

    def test_diff_in_minutes_positive(self):
        dt = Time(12, 34, 56)
        self.assertEqual(62, dt.diff(dt.add(hours=1).add(minutes=2)).in_minutes())

    def test_diff_in_minutes_positive_big(self):
        dt = Time(12, 34, 56)
        self.assertEqual(62, dt.diff(dt.add(hours=25).add(minutes=2)).in_minutes())

    def test_diff_in_minutes_negative_with_sign(self):
        dt = Time(12, 34, 56)
        self.assertEqual(-58, dt.diff(dt.subtract(hours=1).add(minutes=2), False).in_minutes())

    def test_diff_in_minutes_negative_no_sign(self):
        dt = Time(12, 34, 56)
        self.assertEqual(58, dt.diff(dt.subtract(hours=1).add(minutes=2)).in_minutes())

    def test_diff_in_minutes_vs_default_now(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual(60, Time.now().subtract(hours=1).diff().in_minutes())

    def test_diff_in_minutes_ensure_is_truncated(self):
        dt = Time(12, 34, 56)
        self.assertEqual(1, dt.diff(dt.add(minutes=1).add(seconds=59)).in_minutes())

    def test_diff_in_seconds_positive(self):
        dt = Time(12, 34, 56)
        self.assertEqual(62, dt.diff(dt.add(minutes=1).add(seconds=2)).in_seconds())

    def test_diff_in_seconds_positive_big(self):
        dt = Time(12, 34, 56)
        self.assertEqual(7202, dt.diff(dt.add(hours=2).add(seconds=2)).in_seconds())

    def test_diff_in_seconds_negative_with_sign(self):
        dt = Time(12, 34, 56)
        self.assertEqual(-58, dt.diff(dt.subtract(minutes=1).add(seconds=2), False).in_seconds())

    def test_diff_in_seconds_negative_no_sign(self):
        dt = Time(12, 34, 56)
        self.assertEqual(58, dt.diff(dt.subtract(minutes=1).add(seconds=2)).in_seconds())

    def test_diff_in_seconds_vs_default_now(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual(3600, Time.now().subtract(hours=1).diff().in_seconds())

    def test_diff_in_seconds_ensure_is_truncated(self):
        dt = Time(12, 34, 56)
        self.assertEqual(1, dt.diff(dt.add(seconds=1.9)).in_seconds())

    def test_diff_for_humans_now_and_second(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 second ago', Time.now().diff_for_humans())

    def test_diff_for_humans_now_and_seconds(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 seconds ago', Time.now().subtract(seconds=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_minute(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('59 seconds ago', Time.now().subtract(seconds=59).diff_for_humans())

    def test_diff_for_humans_now_and_minute(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 minute ago', Time.now().subtract(minutes=1).diff_for_humans())

    def test_diff_for_humans_now_and_minutes(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 minutes ago', Time.now().subtract(minutes=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_hour(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('59 minutes ago', Time.now().subtract(minutes=59).diff_for_humans())

    def test_diff_for_humans_now_and_hour(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 hour ago', Time.now().subtract(hours=1).diff_for_humans())

    def test_diff_for_humans_now_and_hours(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 hours ago', Time.now().subtract(hours=2).diff_for_humans())

    def test_diff_for_humans_now_and_future_second(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 second from now', Time.now().add(seconds=1).diff_for_humans())

    def test_diff_for_humans_now_and_future_seconds(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 seconds from now', Time.now().add(seconds=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_future_minute(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('59 seconds from now', Time.now().add(seconds=59).diff_for_humans())

    def test_diff_for_humans_now_and_future_minute(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 minute from now', Time.now().add(minutes=1).diff_for_humans())

    def test_diff_for_humans_now_and_future_minutes(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 minutes from now', Time.now().add(minutes=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_future_hour(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('59 minutes from now', Time.now().add(minutes=59).diff_for_humans())

    def test_diff_for_humans_now_and_future_hour(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 hour from now', Time.now().add(hours=1).diff_for_humans())

    def test_diff_for_humans_now_and_future_hours(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 hours from now', Time.now().add(hours=2).diff_for_humans())

    def test_diff_for_humans_other_and_second(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 second before', Time.now().diff_for_humans(Time.now().add(seconds=1)))

    def test_diff_for_humans_other_and_seconds(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 seconds before', Time.now().diff_for_humans(Time.now().add(seconds=2)))

    def test_diff_for_humans_other_and_nearly_minute(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('59 seconds before', Time.now().diff_for_humans(Time.now().add(seconds=59)))

    def test_diff_for_humans_other_and_minute(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 minute before', Time.now().diff_for_humans(Time.now().add(minutes=1)))

    def test_diff_for_humans_other_and_minutes(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 minutes before', Time.now().diff_for_humans(Time.now().add(minutes=2)))

    def test_diff_for_humans_other_and_nearly_hour(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('59 minutes before', Time.now().diff_for_humans(Time.now().add(minutes=59)))

    def test_diff_for_humans_other_and_hour(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 hour before', Time.now().diff_for_humans(Time.now().add(hours=1)))

    def test_diff_for_humans_other_and_hours(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 hours before', Time.now().diff_for_humans(Time.now().add(hours=2)))

    def test_diff_for_humans_other_and_future_second(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 second after', Time.now().diff_for_humans(Time.now().subtract(seconds=1)))

    def test_diff_for_humans_other_and_future_seconds(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 seconds after', Time.now().diff_for_humans(Time.now().subtract(seconds=2)))

    def test_diff_for_humans_other_and_nearly_future_minute(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('59 seconds after', Time.now().diff_for_humans(Time.now().subtract(seconds=59)))

    def test_diff_for_humans_other_and_future_minute(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 minute after', Time.now().diff_for_humans(Time.now().subtract(minutes=1)))

    def test_diff_for_humans_other_and_future_minutes(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 minutes after', Time.now().diff_for_humans(Time.now().subtract(minutes=2)))

    def test_diff_for_humans_other_and_nearly_future_hour(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('59 minutes after', Time.now().diff_for_humans(Time.now().subtract(minutes=59)))

    def test_diff_for_humans_other_and_future_hour(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('1 hour after', Time.now().diff_for_humans(Time.now().subtract(hours=1)))

    def test_diff_for_humans_other_and_future_hours(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('2 hours after', Time.now().diff_for_humans(Time.now().subtract(hours=2)))

    def test_diff_for_humans_absolute_seconds(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('59 seconds', Time.now().diff_for_humans(Time.now().subtract(seconds=59), True))
            self.assertEqual('59 seconds', Time.now().diff_for_humans(Time.now().add(seconds=59), True))

    def test_diff_for_humans_absolute_minutes(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('30 minutes', Time.now().diff_for_humans(Time.now().subtract(minutes=30), True))
            self.assertEqual('30 minutes', Time.now().diff_for_humans(Time.now().add(minutes=30), True))

    def test_diff_for_humans_absolute_hours(self):
        with Time.test(Time(12, 34, 56)):
            self.assertEqual('3 hours', Time.now().diff_for_humans(Time.now().subtract(hours=3), True))
            self.assertEqual('3 hours', Time.now().diff_for_humans(Time.now().add(hours=3), True))
