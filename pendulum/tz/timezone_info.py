# -*- coding: utf-8 -*-

from datetime import tzinfo, timedelta


class TimezoneInfo(tzinfo):

    def __init__(self, tz, offset, is_dst, abbrev):
        """
        :type tz: Timezone

        :type offset: int

        :type is_dst: bool
        """
        self._tz = tz
        self._name = tz.name
        self._offset = offset
        self._is_dst = is_dst
        self._abbrev = abbrev

    @property
    def tz(self):
        return self._tz

    @property
    def name(self):
        return self._name

    @property
    def offset(self):
        return self._offset

    @property
    def is_dst(self):
        return self._is_dst

    @property
    def abbrev(self):
        return self._abbrev

    def tzname(self, dt):
        return self._abbrev

    def utcoffset(self, dt):
        if dt is None:
            return None
        elif dt.tzinfo is not self:
            dt = self.tz.convert(dt)

            return dt.tzinfo.offset
        else:
            return timedelta(seconds=self.offset)

    def dst(self, dt):
        if not self.is_dst:
            return None

        if dt is None:
            return None
        elif dt.tzinfo is not self:
            dt = self.tz.convert(dt)

            offset = dt.tzinfo.offset
        else:
            offset = self.offset

        return timedelta(seconds=offset)

    def __repr__(self):
        return '<TimezoneInfo [{}, {}, {}]>'.format(
            self.name,
            self.offset,
            self.is_dst
        )
