# -*- coding: utf-8 -*-

import pendulum

from .. import AbstractTestCase


class ParserTestCase(AbstractTestCase):

    def test_parse(self):
        text = '2016-10-16T12:34:56.123456+01:30'

        dt = pendulum.parse(text)

        self.assertIsInstanceOfDateTime(dt)
        self.assertDateTime(dt, 2016, 10, 16, 12, 34, 56, 123456)
        self.assertEqual(5400, dt.offset)

        text = '2016-10-16'

        dt = pendulum.parse(text)

        self.assertIsInstanceOfDateTime(dt)
        self.assertDateTime(dt, 2016, 10, 16, 0, 0, 0, 0)
        self.assertEqual(0, dt.offset)

        with self.wrap_with_test_now(pendulum.create(2015, 11, 12)):
            text = '12:34:56.123456'

            dt = pendulum.parse(text)

            self.assertIsInstanceOfDateTime(dt)
            self.assertDateTime(dt, 2015, 11, 12, 12, 34, 56, 123456)
            self.assertEqual(0, dt.offset)

    def test_parse_strict(self):
        text = '2016-10-16T12:34:56.123456+01:30'

        dt = pendulum.parse(text, strict=True)

        self.assertIsInstanceOfDateTime(dt)
        self.assertDateTime(dt, 2016, 10, 16, 12, 34, 56, 123456)
        self.assertEqual(5400, dt.offset)

        text = '2016-10-16'

        dt = pendulum.parse(text, strict=True)

        self.assertIsInstanceOfDate(dt)
        self.assertDate(dt, 2016, 10, 16)

        text = '12:34:56.123456'

        dt = pendulum.parse(text, strict=True)

        self.assertIsInstanceOfTime(dt)
        self.assertTime(dt, 12, 34, 56, 123456)
