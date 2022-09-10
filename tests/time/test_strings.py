from __future__ import annotations

from pendulum import Time


def test_to_string():
    d = Time(1, 2, 3)
    assert str(d) == "01:02:03"
    d = Time(1, 2, 3, 123456)
    assert str(d) == "01:02:03.123456"


def test_repr():
    d = Time(1, 2, 3)
    assert repr(d) == "Time(1, 2, 3)"

    d = Time(1, 2, 3, 123456)
    assert repr(d) == "Time(1, 2, 3, 123456)"


def test_format_with_locale():
    d = Time(14, 15, 16)
    assert d.format("hh:mm:ss A", locale="fr") == "02:15:16 PM"


def test_strftime():
    d = Time(14, 15, 16)
    assert d.strftime("%H") == "14"


def test_for_json():
    d = Time(14, 15, 16)
    assert d.for_json() == "14:15:16"


def test_format():
    d = Time(14, 15, 16)
    assert f"{d}" == "14:15:16"
    assert f"{d:mm}" == "15"
