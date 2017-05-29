import pytest
import pendulum

from pendulum.parsing import parse, ParserError


def test_y():
    text = '2016'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 1 == parsed['month']
    assert 1 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

def test_ym():
    text = '2016-10'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 1 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

def test_ymd():
    text = '2016-10-06'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 6 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

def test_ymd_one_character():
    text = '2016-2-6'

    parsed = parse(text, strict=False)
    assert 2016 == parsed['year']
    assert 2 == parsed['month']
    assert 6 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

def test_ymd_day_first():
    text = '2016-02-06'

    parsed = parse(text, day_first=True)
    assert 2016 == parsed['year']
    assert 6 == parsed['month']
    assert 2 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

def test_ymd_hms():
    text = '2016-10-06 12:34:56'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 6 == parsed['day']
    assert 12 == parsed['hour']
    assert 34 == parsed['minute']
    assert 56 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2016-10-06 12:34:56.123456'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 6 == parsed['day']
    assert 12 == parsed['hour']
    assert 34 == parsed['minute']
    assert 56 == parsed['second']
    assert 123456 == parsed['subsecond']
    assert None == parsed['offset']

def test_rfc_3339():
    text = '2016-10-06T12:34:56+05:30'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 6 == parsed['day']
    assert 12 == parsed['hour']
    assert 34 == parsed['minute']
    assert 56 == parsed['second']
    assert 0 == parsed['subsecond']
    assert 19800 == parsed['offset']

def test_rfc_3339_extended():
    text = '2016-10-06T12:34:56.123456+05:30'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 6 == parsed['day']
    assert 12 == parsed['hour']
    assert 34 == parsed['minute']
    assert 56 == parsed['second']
    assert 123456 == parsed['subsecond']
    assert 19800 == parsed['offset']

    text = '2016-10-06T12:34:56.000123+05:30'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 6 == parsed['day']
    assert 12 == parsed['hour']
    assert 34 == parsed['minute']
    assert 56 == parsed['second']
    assert 123 == parsed['subsecond']
    assert 19800 == parsed['offset']

def test_rfc_3339_extended_nanoseconds():
    text = '2016-10-06T12:34:56.123456789+05:30'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 6 == parsed['day']
    assert 12 == parsed['hour']
    assert 34 == parsed['minute']
    assert 56 == parsed['second']
    assert 123456 == parsed['subsecond']
    assert 19800 == parsed['offset']

def test_iso_8601_date():
    text = '2012'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 1 == parsed['month']
    assert 1 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2012-05-03'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 5 == parsed['month']
    assert 3 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '20120503'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 5 == parsed['month']
    assert 3 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2012-05'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 5 == parsed['month']
    assert 1 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

def test_iso8601_datetime():
    text = '2016-10-01T14'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 1 == parsed['day']
    assert 14 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2016-10-01T14:30'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 1 == parsed['day']
    assert 14 == parsed['hour']
    assert 30 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '20161001T14'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 1 == parsed['day']
    assert 14 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '20161001T1430'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 1 == parsed['day']
    assert 14 == parsed['hour']
    assert 30 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '20161001T1430+0530'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 1 == parsed['day']
    assert 14 == parsed['hour']
    assert 30 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert 19800 == parsed['offset']

    text = '20161001T1430,4+0530'

    parsed = parse(text)
    assert 2016 == parsed['year']
    assert 10 == parsed['month']
    assert 1 == parsed['day']
    assert 14 == parsed['hour']
    assert 30 == parsed['minute']
    assert 0 == parsed['second']
    assert 400000 == parsed['subsecond']
    assert 19800 == parsed['offset']

    text = '2008-09-03T20:56:35.450686+01'

    parsed = parse(text)
    assert 2008 == parsed['year']
    assert 9 == parsed['month']
    assert 3 == parsed['day']
    assert 20 == parsed['hour']
    assert 56 == parsed['minute']
    assert 35 == parsed['second']
    assert 450686 == parsed['subsecond']
    assert 3600 == parsed['offset']

def test_iso8601_week_number():
    text = '2012-W05'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 1 == parsed['month']
    assert 30 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2012W05'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 1 == parsed['month']
    assert 30 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2012-W05-5'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 2 == parsed['month']
    assert 3 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2012W055'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 2 == parsed['month']
    assert 3 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2009-W53-7'
    parsed = parse(text)
    assert 2010 == parsed['year']
    assert 1 == parsed['month']
    assert 3 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2009-W01-1'
    parsed = parse(text)
    assert 2008 == parsed['year']
    assert 12 == parsed['month']
    assert 29 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

def test_iso8601_week_number_with_time():
    text = '2012-W05T09'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 1 == parsed['month']
    assert 30 == parsed['day']
    assert 9 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2012W05T09'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 1 == parsed['month']
    assert 30 == parsed['day']
    assert 9 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2012-W05-5T09'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 2 == parsed['month']
    assert 3 == parsed['day']
    assert 9 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2012W055T09'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 2 == parsed['month']
    assert 3 == parsed['day']
    assert 9 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

def test_iso8601_ordinal():
    text = '2012-007'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 1 == parsed['month']
    assert 7 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '2012007'

    parsed = parse(text)
    assert 2012 == parsed['year']
    assert 1 == parsed['month']
    assert 7 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

def test_iso8601_time():
    now = pendulum.create(2015, 11, 12)

    text = '201205'

    parsed = parse(text, now=now)
    assert 2015 == parsed['year']
    assert 11 == parsed['month']
    assert 12 == parsed['day']
    assert 20 == parsed['hour']
    assert 12 == parsed['minute']
    assert 5 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '20:12:05'

    parsed = parse(text, now=now)
    assert 2015 == parsed['year']
    assert 11 == parsed['month']
    assert 12 == parsed['day']
    assert 20 == parsed['hour']
    assert 12 == parsed['minute']
    assert 5 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '20:12:05.123456'

    parsed = parse(text, now=now)
    assert 2015 == parsed['year']
    assert 11 == parsed['month']
    assert 12 == parsed['day']
    assert 20 == parsed['hour']
    assert 12 == parsed['minute']
    assert 5 == parsed['second']
    assert 123456 == parsed['subsecond']
    assert None == parsed['offset']

def test_iso8601_ordinal_invalid():
    text = '2012-007-05'

    with pytest.raises(ParserError):
        parse(text)

def test_exact():
    text = '2012'

    parsed = parse(text, exact=True)
    assert len(parsed) == 3
    assert 2012 == parsed['year']
    assert 1 == parsed['month']
    assert 1 == parsed['day']

    text = '2012-03'

    parsed = parse(text, exact=True)
    assert len(parsed) == 3
    assert 2012 == parsed['year']
    assert 3 == parsed['month']
    assert 1 == parsed['day']

    text = '2012-03-13'

    parsed = parse(text, exact=True)
    assert len(parsed) == 3
    assert 2012 == parsed['year']
    assert 3 == parsed['month']
    assert 13 == parsed['day']

    text = '2012W055'

    parsed = parse(text, exact=True)
    assert len(parsed) == 3
    assert 2012 == parsed['year']
    assert 2 == parsed['month']
    assert 3 == parsed['day']

    text = '2012007'

    parsed = parse(text, exact=True)
    assert len(parsed) == 3
    assert 2012 == parsed['year']
    assert 1 == parsed['month']
    assert 7 == parsed['day']

    text = '20:12:05'

    parsed = parse(text, exact=True)
    assert len(parsed) == 5
    assert 20 == parsed['hour']
    assert 12 == parsed['minute']
    assert 5 == parsed['second']
    assert 0 == parsed['subsecond']

def test_edge_cases():
    text = '2013-11-1'

    parsed = parse(text, strict=False)
    assert 2013 == parsed['year']
    assert 11 == parsed['month']
    assert 1 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '10-01-01'

    parsed = parse(text, strict=False)
    assert 2010 == parsed['year']
    assert 1 == parsed['month']
    assert 1 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '31-01-01'

    parsed = parse(text, strict=False)
    assert 2031 == parsed['year']
    assert 1 == parsed['month']
    assert 1 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']

    text = '32-01-01'

    parsed = parse(text, strict=False)
    assert 2032 == parsed['year']
    assert 1 == parsed['month']
    assert 1 == parsed['day']
    assert 0 == parsed['hour']
    assert 0 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']


def test_strict():
    text = '4 Aug 2015 - 11:20 PM'

    with pytest.raises(ParserError):
        parse(text)

    parsed = parse(text, strict=False)
    assert 2015 == parsed['year']
    assert 8 == parsed['month']
    assert 4 == parsed['day']
    assert 23 == parsed['hour']
    assert 20 == parsed['minute']
    assert 0 == parsed['second']
    assert 0 == parsed['subsecond']
    assert None == parsed['offset']


def test_invalid():
    text = '201610T'

    with pytest.raises(ParserError):
        parse(text)

    text = '2012-W54'

    with pytest.raises(ParserError):
        parse(text)

    text = '2012-W13-8'

    with pytest.raises(ParserError):
        parse(text)

def test_exif_edge_case():
    text = '2016:12:26 15:45:28'

    parsed = parse(text)

    assert 2016 == parsed['year']
    assert 12 == parsed['month']
    assert 26 == parsed['day']
    assert 15 == parsed['hour']
    assert 45 == parsed['minute']
    assert 28 == parsed['second']
