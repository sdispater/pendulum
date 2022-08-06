from __future__ import annotations

import pendulum


def test_to_string():
    d = pendulum.Date(2016, 10, 16)
    assert str(d) == "2016-10-16"


def test_to_date_string():
    d = pendulum.Date(1975, 12, 25)
    assert d.to_date_string() == "1975-12-25"


def test_to_formatted_date_string():
    d = pendulum.Date(1975, 12, 25)
    assert d.to_formatted_date_string() == "Dec 25, 1975"


def test_repr():
    d = pendulum.Date(1975, 12, 25)

    assert repr(d) == "Date(1975, 12, 25)"
    assert d.__repr__() == "Date(1975, 12, 25)"


def test_format_with_locale():
    d = pendulum.Date(1975, 12, 25)
    expected = "jeudi 25e jour de décembre 1975"
    assert d.format("dddd Do [jour de] MMMM YYYY", locale="fr") == expected


def test_strftime():
    d = pendulum.Date(1975, 12, 25)
    assert d.strftime("%d") == "25"


def test_for_json():
    d = pendulum.Date(1975, 12, 25)
    assert d.for_json() == "1975-12-25"


def test_format():
    d = pendulum.Date(1975, 12, 25)
    assert f"{d}" == "1975-12-25"
    assert f"{d:YYYY}" == "1975"
    assert f"{d:%Y}" == "1975"
