from .reader import Reader
from .timezone import Timezone

_reader = Reader()


def read(name):  # type: (str) -> Timezone
    """
    Read the zoneinfo structure for a given timezone name.
    """
    return _reader.read_for(name)


def read_file(path):  # type: (str) -> Timezone:
    """
    Read the zoneinfo structure for a given path.
    """
    return _reader.read(path)
