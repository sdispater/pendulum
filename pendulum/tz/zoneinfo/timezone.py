from typing import List

from .transition import Transition


class Timezone:

    def __init__(self, transitions: List[Transition], tz_rule=None):
        self._tz_rule = tz_rule
        self._transitions = transitions

    @property
    def transitions(self) -> List[Transition]:
        return self._transitions

    @property
    def tz_rule(self):
        return self._tz_rule
