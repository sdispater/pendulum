from datetime import timedelta
from typing import Union

from .transition_type import TransitionType


class Transition:

    def __init__(self, at: int, ttype: TransitionType,
                 previous: Union['Transition', None]):
        self._at = at

        if previous:
            self._local = at + previous.ttype.offset
        else:
            self._local = at + ttype.offset

        self._ttype = ttype
        self._previous = previous

        if self.previous:
            self._fix = self._ttype.offset - self.previous.ttype.offset
        else:
            self._fix = 0

        self._to = self._local + self._fix
        self._to_utc = self._at + self._fix
        self._utcoffset = timedelta(seconds=ttype.offset)

    @property
    def at(self) -> int:
        return self._at

    @property
    def local(self) -> int:
        return self._local
    
    @property
    def to(self) -> int:
        return self._to

    @property
    def to_utc(self) -> int:
        return self._to

    @property
    def ttype(self) -> TransitionType:
        return self._ttype

    @property
    def previous(self):
        return self._previous

    @property
    def fix(self):
        return self._fix

    def is_ambiguous(self, stamp: int) -> bool:
        return self._to <= stamp < self._local

    def is_missing(self, stamp: int) -> bool:
        return self._local <= stamp < self._to

    def utcoffset(self) -> timedelta:
        return self._utcoffset

    def __contains__(self, stamp):
        return self.previous.local <= stamp < self.local

    def __repr__(self):
        return f'Transition({self._local} -> {self._to}, {self._ttype})'
