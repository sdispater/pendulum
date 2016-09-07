# -*- coding: utf-8 -*-

from datetime import tzinfo

from .transition_type import TransitionType


class TimezoneInfo(tzinfo):

    def __init__(self, tz, transition_type):
        """
        :type tz: Timezone

        :type transition_type: TransitionType

        :type is_dst: bool
        """
        self._tz = tz
        self._transition_type = transition_type

    @classmethod
    def create(cls, tz, utc_offset, is_dst, abbrev):
        return cls(tz, TransitionType(utc_offset, is_dst, abbrev))

    @property
    def tz(self):
        return self._tz

    @property
    def name(self):
        return self._tz._name

    @property
    def offset(self):
        return self._transition_type.utc_offset

    @property
    def is_dst(self):
        return self._transition_type.is_dst

    @property
    def abbrev(self):
        return self._transition_type.abbrev

    @property
    def adjusted_offset(self):
        return self._transition_type.adjusted_offset

    def tzname(self, dt):
        return self.abbrev

    def utcoffset(self, dt):
        if dt is None:
            return None
        elif dt.tzinfo is not self:
            dt = self.tz.convert(dt)

            return dt.tzinfo.adjusted_offset
        else:
            return self._transition_type.adjusted_offset

    def dst(self, dt):
        if not self.is_dst:
            return None

        if dt is None:
            return None
        elif dt.tzinfo is not self:
            dt = self.tz.convert(dt)

            offset = dt.tzinfo._transition_type.adjusted_offset
        else:
            offset = self._transition_type.adjusted_offset

        return offset

    def fromutc(self, dt):
        dt = dt.replace(tzinfo=None)

        idx = max(0, self._tz._find_transition_index(dt, '_utc_time') - 1)
        tzinfo = self._tz._tzinfos[self._tz._transitions[idx]._transition_type_index]

        return (dt + tzinfo.adjusted_offset).replace(tzinfo=tzinfo)

    def __repr__(self):
        return '<TimezoneInfo [{}, {}, {}]>'.format(
            self.name,
            self.offset,
            self.is_dst
        )


class _UTC(TimezoneInfo):

    def __init__(self):
        super(_UTC, self).__init__(None, TransitionType(0, False, 'GMT'))

    @property
    def name(self):
        return 'UTC'

    def utcoffset(self, dt):
        return self._transition_type.adjusted_offset

    def dst(self, dt):
        return None

    def fromutc(self, dt):
        return dt.replace(tzinfo=self)

UTC = _UTC()
