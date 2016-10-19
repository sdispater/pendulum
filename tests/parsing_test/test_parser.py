# -*- coding: utf-8 -*-

from .. import AbstractTestCase
from pendulum.parsing.parser import Parser


class ParserTest(AbstractTestCase):

    def test_ymd(self):
        text = '2016-10-06'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(6, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_ymd_one_character(self):
        text = '2016-2-6'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(2, parsed['month'])
        self.assertEqual(6, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_ymd_day_first(self):
        text = '2016-02-06'

        parsed = Parser(day_first=True).parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(6, parsed['month'])
        self.assertEqual(2, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_ymd_hms(self):
        text = '2016-10-06 12:34:56'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(6, parsed['day'])
        self.assertEqual(12, parsed['hour'])
        self.assertEqual(34, parsed['minute'])
        self.assertEqual(56, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2016-10-06 12:34:56.123456'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(6, parsed['day'])
        self.assertEqual(12, parsed['hour'])
        self.assertEqual(34, parsed['minute'])
        self.assertEqual(56, parsed['second'])
        self.assertEqual(123456000, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_rfc_3339(self):
        text = '2016-10-06T12:34:56+05:30'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(6, parsed['day'])
        self.assertEqual(12, parsed['hour'])
        self.assertEqual(34, parsed['minute'])
        self.assertEqual(56, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(19800, parsed['offset'])

    def test_rfc_3339_extended(self):
        text = '2016-10-06T12:34:56.123456+05:30'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(6, parsed['day'])
        self.assertEqual(12, parsed['hour'])
        self.assertEqual(34, parsed['minute'])
        self.assertEqual(56, parsed['second'])
        self.assertEqual(123456000, parsed['subsecond'])
        self.assertEqual(19800, parsed['offset'])

        text = '2016-10-06T12:34:56.000123+05:30'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(6, parsed['day'])
        self.assertEqual(12, parsed['hour'])
        self.assertEqual(34, parsed['minute'])
        self.assertEqual(56, parsed['second'])
        self.assertEqual(123000, parsed['subsecond'])
        self.assertEqual(19800, parsed['offset'])

    def test_rfc_3339_extended_nanoseconds(self):
        text = '2016-10-06T12:34:56.123456789+05:30'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(6, parsed['day'])
        self.assertEqual(12, parsed['hour'])
        self.assertEqual(34, parsed['minute'])
        self.assertEqual(56, parsed['second'])
        self.assertEqual(123456789, parsed['subsecond'])
        self.assertEqual(19800, parsed['offset'])
