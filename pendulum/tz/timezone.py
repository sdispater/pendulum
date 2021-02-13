from datetime import datetime
from datetime import timedelta
from typing import Optional
from typing import TypeVar

from pendulum.utils._compat import zoneinfo


POST_TRANSITION = "post"
PRE_TRANSITION = "pre"
TRANSITION_ERROR = "error"

_datetime = datetime
_D = TypeVar("_D", bound=datetime)


class Timezone(zoneinfo.ZoneInfo):
    """
    Represents a named timezone.

    The accepted names are those provided by the IANA time zone database.

    >>> from pendulum.tz.timezone import Timezone
    >>> tz = Timezone('Europe/Paris')
    """

    @property
    def name(self) -> str:
        return self.key

    def convert(self, dt: datetime, dst_rule: Optional[str] = None) -> _datetime:
        """
        Converts a datetime in the current timezone.

        If the datetime is naive, it will be normalized.

        >>> from datetime import datetime
        >>> from pendulum import timezone
        >>> paris = timezone('Europe/Paris')
        >>> dt = datetime(2013, 3, 31, 2, 30, fold=1)
        >>> in_paris = paris.convert(dt)
        >>> in_paris.isoformat()
        '2013-03-31T03:30:00+02:00'

        If the datetime is aware, it will be properly converted.

        >>> new_york = timezone('America/New_York')
        >>> in_new_york = new_york.convert(in_paris)
        >>> in_new_york.isoformat()
        '2013-03-30T21:30:00-04:00'
        """
        if dst_rule is not None:
            if dst_rule == PRE_TRANSITION and dt.fold != 0:
                dt = dt.replace(fold=0)
            elif dst_rule == POST_TRANSITION and dt.fold != 1:
                dt = dt.replace(fold=1)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=self)

        return dt.astimezone(self)

    def datetime(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
    ) -> _datetime:
        """
        Return a normalized datetime for the current timezone.
        """
        return datetime(
            year, month, day, hour, minute, second, microsecond, tzinfo=self, fold=1
        )


class FixedTimezone(Timezone):
    def __init__(self, offset, name=None):
        sign = "-" if offset < 0 else "+"

        minutes = offset / 60
        hour, minute = divmod(abs(int(minutes)), 60)

        if not name:
            name = "{0}{1:02d}:{2:02d}".format(sign, hour, minute)

        self._name = name
        self._offset = offset
        self._utcoffset = timedelta(seconds=offset)

    @property
    def offset(self):  # type: () -> int
        return self._offset

    def utcoffset(self, dt):  # type: (Optional[_datetime]) -> timedelta
        return self._utcoffset

    def dst(self, dt):  # type: (Optional[_datetime]) -> timedelta
        return timedelta()

    def fromutc(self, dt):  # type: (_D) -> _D
        # Use the stdlib datetime's add method to avoid infinite recursion
        return (datetime.__add__(dt, self._utcoffset)).replace(tzinfo=self)

    def tzname(self, dt):  # type: (Optional[_datetime]) -> Optional[str]
        return self._name

    def __getinitargs__(self):  # type: () -> tuple
        return self._offset, self._name


class TimezoneFile(Timezone):
    def __init__(self, path):
        tz = read_file(path)  # noqa

        self._name = ""
        self._transitions = tz.transitions
        self._hint = {True: None, False: None}


UTC = Timezone("UTC")
