# -*- coding: utf-8 -*-

from datetime import datetime, tzinfo
from bisect import bisect_right

from .loader import Loader
from .timezone_info import TimezoneInfo, UTC
from ..helpers import local_time as _local_time
from .transition_type import TransitionType
from .exceptions import NonExistingTime, AmbiguousTime


class Timezone(tzinfo):
    """
    Represents a named timezone.

    It inherits from tzinfo in order to be passed to astimezone().
    """

    _cache = {}

    PRE_TRANSITION = 'pre'
    POST_TRANSITION = 'post'
    TRANSITION_ERROR = 'error'

    def __init__(self, name, transitions,
                 transition_types,
                 default_transition_type_index,
                 utc_transition_times):
        self._name = name
        self._transitions = transitions
        self._transition_types = transition_types
        self._tzinfos = tuple(
            map(lambda tt: TimezoneInfo(self, tt), transition_types)
        )
        self._default_transition_type_index = default_transition_type_index
        self._utc_transition_times = utc_transition_times
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
             default_transition_type_index,
             utc_transition_times) = Loader.load(name)

            zone = cls(name,
                       transitions,
                       transition_types,
                       default_transition_type_index,
                       utc_transition_times)

            cls._cache[name] = zone

        return cls._cache[name]

    def convert(self, dt, dst_rule=POST_TRANSITION):
        """
        Converts or normalizes a datetime.

        If there is no tzinfo set on the datetime, local time will be assumed
        and normalization will occur.

        Otherwise, it will convert the datetime to local time.
        """
        if dt.tzinfo is None:
            # we assume local time
            converted = self._normalize(dt, dst_rule=dst_rule)

        else:
            converted = self._convert(dt)

        if not isinstance(converted, tuple):
            return converted

        return dt.__class__(*converted)

    def _normalize(self, dt, dst_rule=POST_TRANSITION):
        # if tzinfo is set, something wrong happened
        if dt.tzinfo is not None:
            raise ValueError(
                'A datetime with a tzinfo cannot be normalized. '
                'Use _convert() instead.'
            )

        if not self._transitions:
            # Use the default offset
            offset = self._tzinfos[self._default_transition_type_index].offset
            unix_time = (dt - datetime(1970, 1, 1)).total_seconds() - offset

            return self._to_local_time(
                unix_time, self._default_transition_type_index
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

        transition_type_index = tr._transition_type_index
        if tr is begin:
            if not tr.pre_time < dt:
                # Before first transition, so use the default offset.
                offset = self._tzinfos[self._default_transition_type_index].offset
                unix_time = (dt - datetime(1970, 1, 1)).total_seconds() - offset

                return self._to_local_time(
                    unix_time, self._default_transition_type_index
                )
            else:
                # tr.pre_time < dt < tr.time
                # Skipped time
                if dst_rule == self.TRANSITION_ERROR:
                    raise NonExistingTime(dt)
                elif dst_rule == self.PRE_TRANSITION:
                    # We do not apply the transition
                    (unix_time,
                     transition_type_index) = self._get_previous_transition_time(tr, dt)
                else:
                    unix_time = tr.unix_time - (tr.pre_time - dt).total_seconds()
        elif tr is end:
            if tr.pre_time < dt:
                # After the last transition.
                unix_time = tr.unix_time + (dt - tr.time).total_seconds()
            else:
                # tr.time <= dt <= tr.pre_time
                # Repeated time
                if dst_rule == self.TRANSITION_ERROR:
                    raise AmbiguousTime(dt)
                elif dst_rule == self.PRE_TRANSITION:
                    # We do not apply the transition
                    (unix_time,
                     transition_type_index) = self._get_previous_transition_time(tr, dt)
                else:
                    unix_time = tr.unix_time + (dt - tr.time).total_seconds()
        else:
            if tr.pre_time <= dt < tr.time:
                # tr.pre_time <= dt < tr.time
                # Skipped time
                if dst_rule == self.TRANSITION_ERROR:
                    raise NonExistingTime(dt)
                elif dst_rule == self.PRE_TRANSITION:
                    # We do not apply the transition
                    (unix_time,
                     transition_type_index) = self._get_previous_transition_time(tr, dt)
                else:
                    unix_time = tr.unix_time - (tr.pre_time - dt).total_seconds()
            elif tr.time <= dt <= tr.pre_time:
                # tr.time <= dt <= tr.pre_time
                # Repeated time
                if dst_rule == self.TRANSITION_ERROR:
                    raise AmbiguousTime(dt)
                elif dst_rule == self.PRE_TRANSITION:
                    # We do not apply the transition
                    (unix_time,
                     transition_type_index) = self._get_previous_transition_time(tr, dt)
                else:
                    unix_time = tr.unix_time + (dt - tr.time).total_seconds()
            else:
                # In between transitions
                # The actual transition type is the previous transition one

                (unix_time,
                 transition_type_index) = self._get_previous_transition_time(tr, dt)

        return self._to_local_time(unix_time, transition_type_index)

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

        return dt.astimezone(self)

    def _to_local_time(self, unix_time, transition_type_index):
        tzinfo = self._tzinfos[transition_type_index]

        local_time = _local_time(
            unix_time,
            tzinfo.offset
        )

        return local_time + (tzinfo,)

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

    def _get_previous_transition_time(self, tr, dt):
        diff = (dt - tr.pre_time).total_seconds()
        if -1 < diff < 0 and tr.unix_time < 0:
            diff -= 1

        unix_time = tr.unix_time + diff

        transition_type_index = tr.pre_transition_type_index

        return unix_time, transition_type_index

    def tzname(self, dt):
        return self.abbrev

    def utcoffset(self, dt):
        if dt is None:
            return None
        elif dt.tzinfo.tz is not self:
            dt = self.convert(dt)

            return dt.adjusted_offset

        return dt.utcoffset(dt)

    def dst(self, dt):
        if dt is None:
            return None
        elif dt.tzinfo.tz is not self:
            dt = self.convert(dt)

            return dt.tzinfo.adjusted_offset

        return dt.tzinfo.dst(dt)

    def fromutc(self, dt):
        dt = dt.replace(tzinfo=None)

        idx = self._find_utc_index(dt)
        tr = self._transitions[idx]
        tzinfo = self._tzinfos[tr._transition_type_index]

        return (dt + tzinfo.adjusted_offset).replace(tzinfo=tzinfo)

    def _find_utc_index(self, dt):
        lo, hi = 0, len(self._utc_transition_times)
        hint = self._local_hint.get('_utc')
        if hint:
            if dt == hint[0]:
                return hint[1]
            elif dt < hint[0]:
                hi = hint[1] + 1
            else:
                lo = hint[1]

        idx = max(0, bisect_right(self._utc_transition_times, dt, lo, hi) - 1)

        self._local_hint['_utc'] = (dt, idx)

        return idx

    def __repr__(self):
        return '<Timezone [{}]>'.format(self._name)


class FixedTimezone(Timezone):
    """
    A timezone that has a fixed offset to UTC.
    """

    def __init__(self, offset, name=None, transition_type=None):
        """
        :param offset: offset to UTC in seconds.
        :type offset: int
        """
        sign = '-' if offset < 0 else '+'

        minutes = offset / 60
        hour, minute = divmod(abs(int(minutes)), 60)

        if not name:
            name = '{0}{1:02d}:{2:02d}'.format(sign, hour, minute)

        if not transition_type:
            transition_type = TransitionType(int(offset), False, '')

        super(FixedTimezone, self).__init__(name, [], [], 0, (datetime(1970, 1, 1),))

        self._tzinfos = (TimezoneInfo(self, transition_type),)
        self._tzinfo = self._tzinfos[0]

    def _normalize(self, dt, dst_rule=Timezone.POST_TRANSITION):
        return dt.replace(tzinfo=self._tzinfo)

    def utcoffset(self, dt):
        if dt is None:
            return None

        return self._tzinfo.utcoffset(dt)

    def dst(self, dt):
        if dt is None:
            return None

        return self._tzinfo.dst(dt)

    def fromutc(self, dt):
        dt = dt.replace(tzinfo=None)

        return (dt + self._tzinfo.adjusted_offset).replace(tzinfo=self._tzinfo)


class _UTC(FixedTimezone):

    def __init__(self):
        super(_UTC, self).__init__(0, 'UTC', TransitionType(0, False, 'GMT'))

        UTC._tz = self

    def fromutc(self, dt):
        return dt.replace(tzinfo=UTC)

UTCTimezone = _UTC()
