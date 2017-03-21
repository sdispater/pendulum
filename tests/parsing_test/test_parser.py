# -*- coding: utf-8 -*-

import pendulum

from .. import AbstractTestCase
from pendulum.parsing.parser import Parser, ParserError


class ParserTest(AbstractTestCase):

    def test_y(self):
        text = '2016'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_ym(self):
        text = '2016-10'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

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
        self.assertEqual(123456, parsed['subsecond'])
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
        self.assertEqual(123456, parsed['subsecond'])
        self.assertEqual(19800, parsed['offset'])

        text = '2016-10-06T12:34:56.000123+05:30'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(6, parsed['day'])
        self.assertEqual(12, parsed['hour'])
        self.assertEqual(34, parsed['minute'])
        self.assertEqual(56, parsed['second'])
        self.assertEqual(123, parsed['subsecond'])
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
        self.assertEqual(123456, parsed['subsecond'])
        self.assertEqual(19800, parsed['offset'])

    def test_iso_8601_date(self):
        text = '2012'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2012-05-03'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(5, parsed['month'])
        self.assertEqual(3, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '20120503'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(5, parsed['month'])
        self.assertEqual(3, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2012-05'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(5, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_iso8601_datetime(self):
        text = '2016-10-01T14'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(14, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2016-10-01T14:30'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(14, parsed['hour'])
        self.assertEqual(30, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '20161001T14'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(14, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '20161001T1430'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(14, parsed['hour'])
        self.assertEqual(30, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '20161001T1430+0530'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(14, parsed['hour'])
        self.assertEqual(30, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(19800, parsed['offset'])

        text = '20161001T1430,4+0530'

        parsed = Parser().parse(text)
        self.assertEqual(2016, parsed['year'])
        self.assertEqual(10, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(14, parsed['hour'])
        self.assertEqual(30, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(400000, parsed['subsecond'])
        self.assertEqual(19800, parsed['offset'])

        text = '2008-09-03T20:56:35.450686+01'

        parsed = Parser().parse(text)
        self.assertEqual(2008, parsed['year'])
        self.assertEqual(9, parsed['month'])
        self.assertEqual(3, parsed['day'])
        self.assertEqual(20, parsed['hour'])
        self.assertEqual(56, parsed['minute'])
        self.assertEqual(35, parsed['second'])
        self.assertEqual(450686, parsed['subsecond'])
        self.assertEqual(3600, parsed['offset'])

    def test_iso8601_week_number(self):
        text = '2012-W05'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(30, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2012W05'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(30, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2012-W05-5'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(2, parsed['month'])
        self.assertEqual(3, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2012W055'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(2, parsed['month'])
        self.assertEqual(3, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2009-W53-7'
        parsed = Parser().parse(text)
        self.assertEqual(2010, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(3, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2009-W01-1'
        parsed = Parser().parse(text)
        self.assertEqual(2008, parsed['year'])
        self.assertEqual(12, parsed['month'])
        self.assertEqual(29, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_iso8601_week_number_with_time(self):
        text = '2012-W05T09'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(30, parsed['day'])
        self.assertEqual(9, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2012W05T09'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(30, parsed['day'])
        self.assertEqual(9, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2012-W05-5T09'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(2, parsed['month'])
        self.assertEqual(3, parsed['day'])
        self.assertEqual(9, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2012W055T09'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(2, parsed['month'])
        self.assertEqual(3, parsed['day'])
        self.assertEqual(9, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_iso8601_ordinal(self):
        text = '2012-007'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(7, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '2012007'

        parsed = Parser().parse(text)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(7, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_iso8601_time(self):
        now = pendulum.create(2015, 11, 12)

        text = '201205'

        parsed = Parser(now=now).parse(text)
        self.assertEqual(2015, parsed['year'])
        self.assertEqual(11, parsed['month'])
        self.assertEqual(12, parsed['day'])
        self.assertEqual(20, parsed['hour'])
        self.assertEqual(12, parsed['minute'])
        self.assertEqual(5, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '20:12:05'

        parsed = Parser(now=now).parse(text)
        self.assertEqual(2015, parsed['year'])
        self.assertEqual(11, parsed['month'])
        self.assertEqual(12, parsed['day'])
        self.assertEqual(20, parsed['hour'])
        self.assertEqual(12, parsed['minute'])
        self.assertEqual(5, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '20:12:05.123456'

        parsed = Parser(now=now).parse(text)
        self.assertEqual(2015, parsed['year'])
        self.assertEqual(11, parsed['month'])
        self.assertEqual(12, parsed['day'])
        self.assertEqual(20, parsed['hour'])
        self.assertEqual(12, parsed['minute'])
        self.assertEqual(5, parsed['second'])
        self.assertEqual(123456, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_iso8601_ordinal_invalid(self):
        text = '2012-007-05'

        self.assertRaises(ParserError, Parser().parse, text)

    def test_strict(self):
        text = '2012'

        parsed = Parser(strict=True).parse(text)
        self.assertEqual(len(parsed), 3)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(1, parsed['day'])

        text = '2012-03'

        parsed = Parser(strict=True).parse(text)
        self.assertEqual(len(parsed), 3)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(3, parsed['month'])
        self.assertEqual(1, parsed['day'])

        text = '2012-03-13'

        parsed = Parser(strict=True).parse(text)
        self.assertEqual(len(parsed), 3)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(3, parsed['month'])
        self.assertEqual(13, parsed['day'])

        text = '2012W055'

        parsed = Parser(strict=True).parse(text)
        self.assertEqual(len(parsed), 3)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(2, parsed['month'])
        self.assertEqual(3, parsed['day'])

        text = '2012007'

        parsed = Parser(strict=True).parse(text)
        self.assertEqual(len(parsed), 3)
        self.assertEqual(2012, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(7, parsed['day'])

        text = '20:12:05'

        parsed = Parser(strict=True).parse(text)
        self.assertEqual(len(parsed), 5)
        self.assertEqual(20, parsed['hour'])
        self.assertEqual(12, parsed['minute'])
        self.assertEqual(5, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])

    def test_edge_cases(self):
        text = '2013-11-1'

        parsed = Parser().parse(text)
        self.assertEqual(2013, parsed['year'])
        self.assertEqual(11, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '10-01-01'

        parsed = Parser().parse(text)
        self.assertEqual(2010, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '31-01-01'

        parsed = Parser().parse(text)
        self.assertEqual(2031, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

        text = '32-01-01'

        parsed = Parser().parse(text)
        self.assertEqual(2032, parsed['year'])
        self.assertEqual(1, parsed['month'])
        self.assertEqual(1, parsed['day'])
        self.assertEqual(0, parsed['hour'])
        self.assertEqual(0, parsed['minute'])
        self.assertEqual(0, parsed['second'])
        self.assertEqual(0, parsed['subsecond'])
        self.assertEqual(None, parsed['offset'])

    def test_invalid(self):
        text = '201610T'

        self.assertRaises(ParserError, Parser().parse, text)

        text = '2012-W54'

        self.assertRaises(ParserError, Parser().parse, text)

        text = '2012-W13-8'

        self.assertRaises(ParserError, Parser().parse, text)

    def test_exif_edge_case(self):
        text = '2016:12:26 15:45:28'

        parsed = Parser().parse(text)

        self.assertEqual(2016, parsed['year'])
        self.assertEqual(12, parsed['month'])
        self.assertEqual(26, parsed['day'])
        self.assertEqual(15, parsed['hour'])
        self.assertEqual(45, parsed['minute'])
        self.assertEqual(28, parsed['second'])
