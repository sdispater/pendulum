# -*- coding: utf-8 -*-

import time as _time
from datetime import datetime

from .loader import Loader
from .timezone_info import TimezoneInfo, UTC
from .breakdown import local_time as _local_time
from .transition_type import TransitionType


class Timezone(object):

    _cache = {}

    def __init__(self, name, transitions,
                 transition_types, default_transition_type):
        self._name = name
        self._transitions = transitions
        self._transition_types = transition_types
        self._default_transition_type = default_transition_type
        self._local_hint = {}

    @property
    def name(self):
        return self._name

    @property
    def transitions(self):
        return self._transitions

    @classmethod
    def load(cls, name):
        """
        Loads a timezone with the given name or
        returns it from the cache.

        :param name: The name of the timezone
        :type name: str

        :rtype: Timezone
        """
        # Shortcut to UTC
        if name.upper() == 'UTC':
            return UTCTimezone

        if name not in cls._cache:
            (transitions,
             transition_types,
             default_transition_type) = Loader.load(name)

            zone = cls(name,
                       transitions,
                       transition_types,
                       default_transition_type)

            cls._cache[name] = zone

        return cls._cache[name]

    def convert(self, dt):
        """
        Converts or normalizes a datetime.

        If there is no tzinfo set on the datetime, local time will be assumed
        and normalization will occur.

        Otherwise, it will convert the datetime to local time.
        """
        if dt.tzinfo is None:
            # we assume local time
            converted = self._normalize(dt)

        else:
            converted = self._convert(dt)

        if not isinstance(converted, tuple):
            return converted

        return dt.__class__(*converted)

    def _normalize(self, dt):
        # if tzinfo is set, something wrong happened
        if dt.tzinfo is not None:
            raise ValueError(
                'A datetime with a tzinfo cannot be normalized. '
                'Use _convert() instead.'
            )

        if not self._transitions:
            # Use the default offset
            offset = self._default_transition_type.utc_offset
            unix_time = (dt - datetime(1970, 1, 1)).total_seconds() - offset

            return self._to_local_time(
                unix_time, self._default_transition_type
            )

        # Find the first transition after our target date/time
        begin = self._transitions[0]
        end = self._transitions[-1]

        if dt < begin.time:
            tr = begin
        elif not dt < end.time:
            tr = end
        else:
            idx = self._find_transition_index(dt)
            tr = self._transitions[idx]

            if idx > 0:
                pre_tr = self._transitions[idx - 1]

                # DST -> No DST
                if dt <= pre_tr.pre_time:
                    tr = pre_tr

        transition_type = tr._transition_type
        if tr is begin:
            if not tr.pre_time < dt:
                # Before first transition, so use the default offset.
                offset = self._default_transition_type.utc_offset
                unix_time = (dt - datetime(1970, 1, 1)).total_seconds() - offset

                return self._to_local_time(
                    unix_time, self._default_transition_type
                )
            else:
                # tr.pre_time < dt < tr.time
                # Skipped time
                unix_time = tr.unix_time - (tr.pre_time - dt).total_seconds()
        elif tr is end:
            if tr.pre_time < dt:
                # After the last transition.
                unix_time = tr.unix_time + (dt - tr.time).total_seconds()
            else:
                # tr.time <= dt <= tr.pre_time
                # Repeated time
                unix_time = tr.unix_time + (dt - tr.time).total_seconds()
        else:
            if tr.pre_time <= dt < tr.time:
                # tr.pre_time <= dt < tr.time
                # Skipped time
                unix_time = tr.unix_time - (tr.pre_time - dt).total_seconds()
            elif tr.time <= dt <= tr.pre_time:
                # tr.time <= dt <= tr.pre_time
                # Repeated time
                unix_time = tr.unix_time + (dt - tr.time).total_seconds()
            else:
                # In between transitions
                # The actual transition type is the previous transition one

                # Fix for negative microseconds for negative timestamps
                diff = (dt - tr.pre_time).total_seconds()
                if -1 < diff < 0 and tr.unix_time < 0:
                    diff -= 1

                unix_time = tr.unix_time + diff

                transition_type = tr.pre_transition_type

        return self._to_local_time(unix_time, transition_type)

    def _convert(self, dt):
        """
        Converts a timezone-aware datetime to local time.

        :param dt: The datetime to convert.
        :type dt: datetime
        """
        # if tzinfo is not set, something wrong happened
        if dt.tzinfo is None:
            raise ValueError(
                'A datetime without a tzinfo cannot be converted. '
                'Use _normalize() instead.'
            )

        unix_time = self._get_timestamp(dt)

        if not self._transitions:
            transition_type = self._default_transition_type
        else:
            idx = max(0, self._find_transition_index(unix_time, '_unix_time') - 1)
            tr = self._transitions[idx]
            transition_type = tr.transition_type

        return self._to_local_time(unix_time, transition_type)

    def _to_local_time(self, unix_time, transition_type):
        local_time = _local_time(
            unix_time,
            transition_type
        )

        tzinfo = TimezoneInfo(
            self,
            transition_type
        )

        return local_time[:7] + (tzinfo,)

    def _get_timestamp(self, dt):
        if hasattr(dt, 'float_timestamp'):
            return dt.float_timestamp

        t = (dt - datetime(1970, 1, 1, tzinfo=UTC)).total_seconds()

        if dt.microsecond > 0 and t < 0:
            t -= 1

        return t

    def _find_transition_index(self, dt, prop='_time'):
        lo, hi = 0, len(self._transitions)
        hint = self._local_hint.get(prop)
        if hint:
            if dt == hint[0]:
                return hint[1]
            elif dt < hint[0]:
                hi = hint[1]
            else:
                lo = hint[1]

        while lo < hi:
            mid = (lo + hi) // 2
            if dt < getattr(self._transitions[mid], prop):
                hi = mid
            else:
                lo = mid + 1

        self._local_hint[prop] = (dt, lo)

        return lo

    def __repr__(self):
        return '<Timezone [{}]>'.format(self._name)


class FixedTimezone(Timezone):
    """
    A timezone that has a fixed offset to UTC.
    """

    def __init__(self, offset):
        """
        :param offset: offset to UTC in seconds.
        :type offset: int
        """
        sign = '-' if offset < 0 else '+'

        minutes = offset / 60
        hour, minute = divmod(abs(int(minutes)), 60)

        name = '{0}{1:02d}:{2:02d}'.format(sign, hour, minute)

        transition_type = TransitionType(int(offset), False, '')

        super(FixedTimezone, self).__init__(name, [], [], transition_type)


class _UTC(Timezone):

    def __init__(self):
        super(_UTC, self).__init__('UTC', [], [], TransitionType(0, False, 'GMT'))

        UTC._tz = self
        self._tzinfo = UTC

    @property
    def tzinfo(self):
        return self._tzinfo

UTCTimezone = _UTC()
