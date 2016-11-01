# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


class Transition(object):
    """
    Represents a Timezone transition time.

    It stores
        - the unix timestamp of the transition (in UTC),
        - the index of the TimezoneInfo (UTC offset,
                                         DST or not,
                                         timezone abbreviation),
        - the local time before the transition
        - the local time after the transition
        - the index of the previous TimezoneInfo
    """

    _epoch = datetime.utcfromtimestamp(0)

    def __init__(self, unix_time,
                 tzinfo_index, pre_time, time,
                 pre_tzinfo_index):
        """
        Constructor.

        :param unix_time: unix timestamp of the transition.
        :type unix_time: int

        :param tzinfo_index: The index of the timezone info
        :type tzinfo_index: int

        :param pre_time: The local time before the transition
        :type pre_time: datetime

        :param time: The local time after the transition
        :type time: datetime

        :param pre_tzinfo_index: The previous TimezoneInfo index
        :type pre_tzinfo_index: int
        """
        self._unix_time = unix_time
        self._tzinfo_index = tzinfo_index
        self._pre_time = pre_time
        self._time = time
        # We can't directly make datetime.utcfromtimestamp(unix_time)
        # since it will fail on Windows for negative timestamps.
        self._utc_time = self._epoch + timedelta(seconds=unix_time)
        self._pre_tzinfo_index = pre_tzinfo_index

    @property
    def unix_time(self):
        return self._unix_time

    @property
    def tzinfo_index(self):
        return self._tzinfo_index

    @property
    def pre_tzinfo_index(self):
        return self._pre_tzinfo_index

    @property
    def pre_time(self):
        return self._pre_time

    @property
    def time(self):
        return self._time

    @property
    def utc_time(self):
        return self._utc_time

    def __repr__(self):
        return '<Transition [{} UTC, {} -> {}]>'.format(
            self._utc_time,
            self._pre_time,
            self.time
        )
