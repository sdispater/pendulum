import os

import pytest

from pendulum.tz.zoneinfo.exceptions import InvalidTimezone
from pendulum.tz.zoneinfo.exceptions import InvalidZoneinfoFile
from pendulum.tz.zoneinfo.reader import Reader
from pendulum.tz.zoneinfo.timezone import Timezone


def test_read_for_bad_timezone():
    reader = Reader()
    with pytest.raises(InvalidTimezone):
        reader.read_for("---NOT A TIMEZONE---")


def test_read_for_valid():
    reader = Reader()

    tz = reader.read_for("America/Toronto")
    assert isinstance(tz, Timezone)


def test_read():
    reader = Reader()
    local_path = os.path.join(os.path.split(__file__)[0], "..", "..")
    tz_file = os.path.join(local_path, "fixtures", "tz", "Paris")
    tz = reader.read(tz_file)

    assert len(tz.transitions) > 0


def test_read_invalid():
    reader = Reader()
    local_path = os.path.join(os.path.split(__file__)[0], "..")
    tz_file = os.path.join(local_path, "fixtures", "tz", "NOT_A_TIMEZONE")

    with pytest.raises(InvalidZoneinfoFile):
        reader.read(tz_file)


def test_set_transitions_for_no_transition_database_file():
    reader = Reader()
    tz = reader.read_for("Etc/UTC")

    assert len(tz.transitions) == 1
