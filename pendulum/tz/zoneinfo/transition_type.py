from datetime import timedelta


class TransitionType:
    def __init__(self, offset, is_dst, abbr):
        self._offset = offset
        self._is_dst = is_dst
        self._abbr = abbr

        self._utcoffset = timedelta(seconds=offset)

    @property
    def offset(self):  # type: () -> int
        return self._offset

    @property
    def abbreviation(self):  # type: () -> str
        return self._abbr

    def is_dst(self):  # type: () -> bool
        return self._is_dst

    def utcoffset(self):  # type: () -> timedelta
        return self._utcoffset

    def __repr__(self):  # type: () -> str
        return "TransitionType({}, {}, {})".format(
            self._offset, self._is_dst, self._abbr
        )
