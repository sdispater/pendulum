import os
import pytest

from pendulum.tz.loader import Loader


def test_load_bad_timezone():
    with pytest.raises(ValueError):
        Loader.load('---NOT A TIMEZONE---')


def test_load_valid():
    assert Loader.load('America/Toronto')


def test_load_from_file():
    local_path = os.path.join(os.path.split(__file__)[0], '..')
    tz_file = os.path.join(local_path, 'fixtures', 'tz', 'Paris')
    (transitions,
     transition_types,
     default_transition_type,
     utc_transition_times) = Loader.load_from_file(tz_file)

    assert len(transitions) > 0
    assert len(transition_types) > 0
    assert len(utc_transition_times) > 0
    assert default_transition_type is not None


def test_load_from_file_invalid():
    local_path = os.path.join(os.path.split(__file__)[0], '..')
    tz_file = os.path.join(local_path, 'fixtures', 'tz', 'NOT_A_TIMEZONE')

    with pytest.raises(ValueError):
        Loader.load_from_file(tz_file)


def test_set_transitions_for_no_transition_database_file():
    tz = Loader.load('Etc/UTC')

    assert len(tz[0]) == 1
    assert len(tz[1]) == 1
