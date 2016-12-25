# -*- coding: utf-8 -*-

import pendulum
from .. import AbstractTestCase

from pendulum.formatting import register_formatter, Formatter


class ModuleTestCase(AbstractTestCase):

    def test_register_formatter(self):
        register_formatter('test', TestFormatter())

        self.assertEqual('foo', pendulum.now().format('', formatter='test'))

    def test_register_formatter_existing_name(self):
        self.assertRaises(ValueError, register_formatter, 'classic', TestFormatter())

    def test_register_formatter_not_formatter_instance(self):
        self.assertRaises(ValueError, register_formatter, 'test', FooFormatter())


class TestFormatter(Formatter):

    def format(self, dt, fmt, locale=None):
        return 'foo'


class FooFormatter(object):

    def format(self, dt, fmt, locale=None):
        return 'foo'


