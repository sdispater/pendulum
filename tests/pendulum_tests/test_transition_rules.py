# -*- coding: utf-8 -*-

import pendulum
from .. import AbstractTestCase


class TransitionRulesTest(AbstractTestCase):

    def test_set(self):
        pendulum.set_transition_rule(pendulum.PRE_TRANSITION)
        self.assertEqual(pendulum.PRE_TRANSITION, pendulum.get_transition_rule())

    def test_set_invalid(self):
        self.assertRaises(ValueError, pendulum.set_transition_rule, 'invalid')
