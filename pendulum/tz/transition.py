# -*- coding: utf-8 -*-

from datetime import datetime


class Transition(object):
    """
    Represents a Timezone transition time.

    It stores
        - the unix timestamp of the transition (in UTC),
        - the type of the transition (UTC offset,
                                      DST or not,
                                      timezone abbreviation),
        - the local time before the transition
        - the local time after the transition.
    """

    def __init__(self, unix_time,
                 transition_type_index, pre_time, time,
                 pre_transition_type_index):
        """
        Constructor.

        :param unix_time: unix timestamp of the transition.
        :type unix_time: int

        :param transition_type_index: The index of the transition type
        :type transition_type_index: int

        :param pre_time: The local time before the transition
        :type pre_time: datetime

        :param time: The local time after the transition
        :type time: datetime

        :param pre_transition_type_index: The previous TransitionType index
        :type pre_transition_type_index: int
        """
        self._unix_time = unix_time
        self._transition_type_index = transition_type_index
        self._pre_time = pre_time
        self._time = time
        self._utc_time = datetime.utcfromtimestamp(unix_time)
        self._pre_transition_type_index = pre_transition_type_index

    @property
    def unix_time(self):
        return self._unix_time

    @property
    def transition_type_index(self):
        return self._transition_type_index

    @property
    def pre_transition_type_index(self):
        return self._pre_transition_type_index

    @property
    def pre_time(self):
        return self._pre_time

    @property
    def time(self):
        return self._time

    def __eq__(self, other):
        own, other = self._get_comparables(other)

        return own == other

    def __ne__(self, other):
        own, other = self._get_comparables(other)

        return own != other

    def __lt__(self, other):
        own, other = self._get_comparables(other)

        return own < other

    def __le__(self, other):
        own, other = self._get_comparables(other)

        return own <= other

    def __gt__(self, other):
        own, other = self._get_comparables(other)

        return own > other

    def __ge__(self, other):
        own, other = self._get_comparables(other)

        return own >= other

    def _get_comparables(self, other):
        if isinstance(other, Transition):
            own = self._unix_time
            other = other._unix_time
        elif isinstance(other, datetime):
            own = self._time
        else:
            own = self._unix_time

        return own, other

    def __repr__(self):
        return '<Transition [{} UTC, {} -> {}]>'.format(
            self._utc_time,
            self._pre_time,
            self.time
        )
