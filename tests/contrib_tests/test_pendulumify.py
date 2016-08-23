# -*- coding: utf-8 -*-

import datetime

from .. import AbstractTestCase
from pendulum.contrib.pendulumify import pendulumify, pendulumify_wrap


class PendulumifyTest(AbstractTestCase):

    def test_dictionary(self):
        d = pendulumify({
            'example': datetime.datetime.now(),
            'donottouch': 'safe',
        })

        self.assertIsInstanceOfPendulum(d.get('example'))
        self.assertEqual(d.get('donottouch'), 'safe')

        @pendulumify_wrap
        def wrapped():
            return {
                'example': datetime.datetime.now(),
                'donottouch': 'safe',
            }

        self.assertIsInstanceOfPendulum(wrapped().get('example'))
        self.assertEqual(wrapped().get('donottouch'), 'safe')

    def test_nested_dictionary(self):
        d = pendulumify({
            'inner': {
                'example': datetime.datetime.now(),
                'donottouch': 'safe',
            },
        })

        self.assertIsInstanceOfPendulum(d.get('inner').get('example'))
        self.assertEqual(d.get('inner').get('donottouch'), 'safe')

        @pendulumify_wrap
        def wrapped():
            return {
                'inner': {
                    'example': datetime.datetime.now(),
                    'donottouch': 'safe',
                },
            }

        self.assertIsInstanceOfPendulum(wrapped().get('inner').get('example'))
        self.assertEqual(wrapped().get('inner').get('donottouch'), 'safe')

    def test_list(self):
        d = pendulumify([datetime.datetime.now()])

        self.assertIsInstanceOfPendulum(d[0])

        @pendulumify_wrap
        def wrapped():
            return [datetime.datetime.now()]

        self.assertIsInstanceOfPendulum(wrapped()[0])

    def test_nested_list(self):
        d = pendulumify([[datetime.datetime.now()]])

        self.assertIsInstanceOfPendulum(d[0][0])

        @pendulumify_wrap
        def wrapped():
            return [[datetime.datetime.now()]]

        self.assertIsInstanceOfPendulum(wrapped()[0][0])

    def test_set(self):
        d = pendulumify(set([datetime.datetime.now()]))

        self.assertIsInstanceOfPendulum(d.pop())

        @pendulumify_wrap
        def wrapped():
            return set([datetime.datetime.now()])

        self.assertIsInstanceOfPendulum(wrapped().pop())

    def test_nested_set(self):
        d = pendulumify(set([frozenset([datetime.datetime.now()])]))

        self.assertIsInstanceOfPendulum(next(iter(d.pop())))

        @pendulumify_wrap
        def wrapped():
            return set([frozenset([datetime.datetime.now()])])

        self.assertIsInstanceOfPendulum(next(iter(wrapped().pop())))

    def test_function(self):
        d = pendulumify(lambda: datetime.datetime.now())

        self.assertIsInstanceOfPendulum(d())

        @pendulumify_wrap
        def wrapped():
            def inner():
                return datetime.datetime.now()

            return inner

        self.assertIsInstanceOfPendulum(wrapped()())

    def test_generator(self):
        try:
            xrange
        except NameError:
            xrange = range

        d = pendulumify((datetime.datetime.now() for x in xrange(0, 10)))

        for x in d:
            self.assertIsInstanceOfPendulum(x)

        @pendulumify_wrap
        def wrapped():
            def my_gen():
                for x in xrange(0, 10):
                    yield datetime.datetime.now()

            return my_gen()

        for x in wrapped():
            self.assertIsInstanceOfPendulum(x)

    def test_dictionary_from_generator(self):
        try:
            xrange
        except NameError:
            xrange = range

        d = pendulumify(
            ({'val': datetime.datetime.now()} for x in xrange(0, 10))
        )

        for x in d:
            self.assertIsInstanceOfPendulum(x.get('val'))

        @pendulumify_wrap
        def wrapped():
            def my_gen():
                for x in xrange(0, 10):
                    yield {'val': datetime.datetime.now()}

            return my_gen()

        for x in wrapped():
            self.assertIsInstanceOfPendulum(x.get('val'))
