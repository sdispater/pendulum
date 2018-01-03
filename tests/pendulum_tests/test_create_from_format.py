# -*- coding: utf-8 -*-

import pytest
import pendulum

from pendulum import Pendulum, timezone
from .. import AbstractTestCase


class CreateFromFormatTest(AbstractTestCase):

    def test_create_from_format_returns_pendulum(self):
        d = Pendulum.create_from_format('1975-05-21 22:32:11', '%Y-%m-%d %H:%M:%S')
        self.assertPendulum(d, 1975, 5, 21, 22, 32, 11)
        self.assertIsInstanceOfPendulum(d)
        self.assertEqual('UTC', d.timezone_name)

    def test_create_from_format_with_timezone_string(self):
        d = Pendulum.create_from_format('1975-05-21 22:32:11', '%Y-%m-%d %H:%M:%S', 'Europe/London')
        self.assertPendulum(d, 1975, 5, 21, 22, 32, 11)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_format_with_timezone(self):
        d = Pendulum.create_from_format(
            '1975-05-21 22:32:11', '%Y-%m-%d %H:%M:%S', timezone('Europe/London')
        )
        self.assertPendulum(d, 1975, 5, 21, 22, 32, 11)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_format_with_millis(self):
        d = Pendulum.create_from_format(
            '1975-05-21 22:32:11.123456', '%Y-%m-%d %H:%M:%S.%f'
        )
        self.assertPendulum(d, 1975, 5, 21, 22, 32, 11)
        self.assertEqual(123456, d.microsecond)

    def test_strptime_is_create_from_format(self):
        d = Pendulum.strptime('1975-05-21 22:32:11', '%Y-%m-%d %H:%M:%S')
        self.assertPendulum(d, 1975, 5, 21, 22, 32, 11)
        self.assertIsInstanceOfPendulum(d)
        self.assertEqual('UTC', d.timezone_name)


@pytest.mark.parametrize('text,fmt,expected', [
    ('2014-4', 'YYYY-Q', '2014-10-01T00:00:00+00:00'),
    ('12-02-1999', 'MM-DD-YYYY', '1999-12-02T00:00:00+00:00'),
    ('12-02-1999', 'DD-MM-YYYY', '1999-02-12T00:00:00+00:00'),
    ('12/02/1999', 'DD/MM/YYYY', '1999-02-12T00:00:00+00:00'),
    ('12_02_1999', 'DD_MM_YYYY', '1999-02-12T00:00:00+00:00'),
    ('12:02:1999', 'DD:MM:YYYY', '1999-02-12T00:00:00+00:00'),
    ('2-2-99', 'D-M-YY', '1999-02-02T00:00:00+00:00'),
    ('99', 'YY', '1999-01-01T00:00:00+00:00'),
    ('300-1999', 'DDD-YYYY', '1999-10-27T00:00:00+00:00'),
    ('12-02-1999 2:45:10', 'DD-MM-YYYY h:m:s', '1999-02-12T02:45:10+00:00'),
    ('12-02-1999 12:45:10', 'DD-MM-YYYY h:m:s', '1999-02-12T12:45:10+00:00'),
    ('12:00:00', 'HH:mm:ss', '2015-11-12T12:00:00+00:00'),
    ('12:30:00', 'HH:mm:ss', '2015-11-12T12:30:00+00:00'),
    ('00:00:00', 'HH:mm:ss', '2015-11-12T00:00:00+00:00'),
    ('00:30:00 1', 'HH:mm:ss S', '2015-11-12T00:30:00.100000+00:00'),
    ('00:30:00 12', 'HH:mm:ss SS', '2015-11-12T00:30:00.120000+00:00'),
    ('00:30:00 123', 'HH:mm:ss SSS', '2015-11-12T00:30:00.123000+00:00'),
    ('1234567890', 'X', '2009-02-13T23:31:30+00:00'),
    ('1234567890123', 'x', '2009-02-13T23:31:30.123000+00:00'),
    ('2016-10-06', 'YYYY-MM-DD', '2016-10-06T00:00:00+00:00'),
    ('2016|10|06', 'YYYY|MM|DD', '2016-10-06T00:00:00+00:00'),
    ('2016(10|06)', 'YYYY(MM|DD)', '2016-10-06T00:00:00+00:00'),
])
def test_from_format(text, fmt, expected):
    with pendulum.test(pendulum.create(2015, 11, 12)):
        assert pendulum.from_format(text, fmt, formatter='alternative').isoformat() == expected
