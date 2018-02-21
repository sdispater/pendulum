# -*- coding: utf-8 -*-

from datetime import tzinfo, timedelta


class TimezoneInfo(tzinfo):

    def __init__(self, tz, utc_offset, is_dst, dst, abbrev):
        """
        :param tz: The parent timezone.
        :type tz: Timezone

        :param utc_offset: Offset from UTC (in seconds).
        :type utc_offset: int

        :param is_dst: Whether DST is in effect or not.
        :type is_dst: bool

        :param dst: Transition time value (if any).
        :type dst: timedelta or None

        :param abbrev: Timezone name abbreviation (CET, CEST, ...)
        :type abbrev: str
        """
        self._tz = tz
        self._utc_offset = utc_offset
        self._adjusted_offset = timedelta(seconds=round(utc_offset / 60) * 60)
        self._is_dst = is_dst
        self._dst = dst
        self._abbrev = abbrev

    @property
    def tz(self):
        return self._tz

    @property
    def name(self):
        return self._tz._name

    @property
    def offset(self):
        return self._utc_offset

    @property
    def is_dst(self):
        return self._is_dst

    @property
    def abbrev(self):
        return self._abbrev

    @property
    def adjusted_offset(self):
        return self._adjusted_offset

    @property
    def dst_(self):
        return self._dst

    def tzname(self, dt):
        if dt is None:
            return self._abbrev
        elif dt.tzinfo is not self:
            dt = self.tz.convert(dt)

            return dt.tzinfo.abbrev
        else:
            return self._abbrev

    def utcoffset(self, dt):
        if dt is None:
            return None
        elif dt.tzinfo is not self:
            dt = self.tz.convert(dt)

            return dt.tzinfo.adjusted_offset
        else:
            return self._adjusted_offset

    def dst(self, dt):
        if not self.is_dst:
            return None

        if dt is None:
            return None
        elif dt.tzinfo is not self:
            dt = self.tz.convert(dt)

            offset = dt.tzinfo._dst
        else:
            offset = self._dst

        return offset

    def fromutc(self, dt):
        dt = dt.replace(tzinfo=None)

        idx = max(0, self._tz._find_transition_index(dt, '_utc_time') - 1)
        tzinfo = self._tz._tzinfos[self._tz._transitions[idx]._tzinfo_index]

        return (dt + tzinfo.adjusted_offset).replace(tzinfo=tzinfo)

    def __repr__(self):
        return '<TimezoneInfo [{}, {}, {}{}, {}]>'.format(
            self.name,
            self.abbrev,
            '+' if self.offset >= 0 else '',
            '{:02d}:{:02d}:{:02d}'.format(
                self.offset // 3600,
                self.offset % 3600 // 60,
                self.offset % 60
            ),
            'DST' if self.is_dst else 'STD',
        )

    def __getinitargs__(self):
        return self._tz, self._utc_offset, self._is_dst, self._dst, self._abbrev

class _UTC(TimezoneInfo):

    def __init__(self):
        super(_UTC, self).__init__(None, 0, False, None, 'GMT')

    @property
    def name(self):
        return 'UTC'

    def utcoffset(self, dt):
        return self._adjusted_offset

    def dst(self, dt):
        return None

    def fromutc(self, dt):
        return dt.replace(tzinfo=self)

    def __getinitargs__(self):
        return ()


UTC = _UTC()
