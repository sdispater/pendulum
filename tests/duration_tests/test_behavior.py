import pickle
import pendulum
from .. import AbstractTestCase


class BehaviorTest(AbstractTestCase):

    def test_pickle(self):
        it = pendulum.duration(days=3, seconds=2456, microseconds=123456)
        s = pickle.dumps(it)
        it2 = pickle.loads(s)

        self.assertEqual(it, it2)
