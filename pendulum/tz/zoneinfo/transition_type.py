from datetime import timedelta


class TransitionType:

    def __init__(self, offset, is_dst, abbr):
        self._offset = offset
        self._is_dst = is_dst
        self._abbr = abbr

        self._utcoffset = timedelta(seconds=offset)

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def abbreviation(self) -> str:
        return self._abbr

    def is_dst(self) -> bool:
        return self._is_dst

    def utcoffset(self) -> timedelta:
        return self._utcoffset

    def __repr__(self):
        return f'TransitionType({self._offset}, {self._is_dst}, {self._abbr})'
