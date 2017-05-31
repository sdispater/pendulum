import re
import copy

from datetime import datetime, date, time
from dateutil import parser

from ..constants import HOURS_PER_DAY, MINUTES_PER_HOUR, SECONDS_PER_MINUTE
from ..helpers import parse_iso8601, week_day, days_in_year
from .exceptions import ParserError
from .parsed import Parsed


COMMON = re.compile(
    # Date (optional)
    '^'
    '(?P<date>'
    '    (?P<classic>'  # Classic date (YYYY-MM-DD) or ordinal (YYYY-DDD)
    '        (?P<year>\d{4})'  # Year
    '        (?P<monthday>'
    '            (?P<monthsep>[-/:])?(?P<month>\d{2})'  # Month (optional)
    '            ((?P<daysep>[-/:])?(?P<day>\d{1,2}))?'  # Day (optional)
    '        )?'
    '    )'
    '    |'
    '    (?P<isocalendar>'  # Calendar date (2016-W05 or 2016-W05-5)
    '        (?P<isoyear>\d{4})'  # Year
    '        -?'  # Separator (optional)
    '        W'  # W separator
    '        (?P<isoweek>\d{2})'  # Week number
    '        -?'  # Separator (optional)
    '        (?P<isoweekday>\d)?'  # Weekday (optional)
    '    )'
    ')?'

    # Time (optional)
    '(?P<time>'
    '    (?P<timesep>T|\ )?'  # Separator (T or space)
    '    (?P<hour>\d{1,2}):?(?P<minute>\d{1,2})?:?(?P<second>\d{1,2})?'  # HH:mm:ss (optional mm and ss)
    # Subsecond part (optional)
    '    (?P<subsecondsection>'
    '        (?:\.|,)'  # Subsecond separator (optional)
    '        (?P<subsecond>\d{1,9})'  # Subsecond
    '    )?'
    # Timezone offset
    '    (?P<tz>'
    '        (?:-|\+)\d{2}:?(?:\d{2})?|Z'  # Offset (+HH:mm or +HHmm or +HH or Z)
    '    )?'
    ')?'
    '$',
    re.VERBOSE
)


DURATION = re.compile(
    '^P' # Duration P indicator
    # Years, months and days (optional)
    '(?P<w>'
    '    (?P<weeks>\d+(?:[.,]\d+)?W)'
    ')?'
    '(?P<ymd>'
    '    (?P<years>\d+(?:[.,]\d+)?Y)?'
    '    (?P<months>\d+(?:[.,]\d+)?M)?'
    '    (?P<days>\d+(?:[.,]\d+)?D)?'
    ')?'
    '(?P<hms>'
    '    (?P<timesep>T)'  # Separator (T)
    '    (?P<hours>\d+(?:[.,]\d+)?H)?'
    '    (?P<minutes>\d+(?:[.,]\d+)?M)?'
    '    (?P<seconds>\d+(?:[.,]\d+)?S)?'
    ')?'
    '$',
    re.VERBOSE
)


DEFAULT_OPTIONS = {
    'day_first': False,
    'year_first': True,
    'strict': True,
    'exact': False,
    'now': None
}


def parse(text, **options):
    """
    Parses a string with the given options.

    :param text: The string to parse.
    :type text: str

    :rtype: Parsed
    """
    _options = copy.copy(DEFAULT_OPTIONS)
    _options.update(options)

    return _normalize(_parse(text, **_options), **_options)


def _normalize(parsed, **options):
    """
    Normalizes the parsed element.

    :param parsed: The parsed elements.
    :type parsed: Parsed

    :rtype: Parsed
    """
    if options.get('exact') or parsed.is_duration or parsed.is_period:
        return parsed

    if parsed.is_time:
        now = options['now'] or datetime.now()
        parsed.year = now.year
        parsed.month = now.month
        parsed.day = now.day

    parsed.is_datetime = True
    parsed.is_time = False
    parsed.is_date = False

    return parsed


def _parse(text, **options):
    parsed = Parsed()

    if not options['day_first']:
        # Trying to parse ISO8601
        _parse_iso8601(text, parsed)

        if parsed.is_valid():
            return parsed

    _parse_duration(text, parsed, **options)
    if parsed.is_valid():
        return parsed

    _parse_common(text, parsed, **options)
    if parsed.is_valid():
        return parsed

    # We couldn't parse the string
    # so we fallback on the dateutil parser
    # If not strict
    if options.get('strict', True):
        raise ParserError(f'Unable to parse string [{text}]')

    try:
        dt = parser.parse(
            text,
            dayfirst=options['day_first'],
            yearfirst=options['year_first']
        )
    except ValueError:
        raise ParserError('Invalid date string: {}'.format(text))

    return parsed.from_datetime(dt)


def _parse_iso8601(text, parsed):
    if not parse_iso8601:
        return

    try:
        dt = parse_iso8601(text)
    except ValueError:
        return

    if isinstance(dt, time):
        return parsed.from_time(dt)
    elif isinstance(dt, date) and not isinstance(dt, datetime):
        return parsed.from_date(dt)

    return parsed.from_datetime(dt)


def _parse_common(text, parsed, **options):
    """
    Tries to parse the string as a common datetime format.

    :param text: The string to parse.
    :type text: str

    :rtype: dict or None
    """
    m = COMMON.match(text)
    ambiguous_date = False

    if m:
        if m.group('date'):
            # A date has been specified
            parsed.is_date = True

            if m.group('isocalendar'):
                # We have a ISO 8601 string defined
                # by week number
                try:
                    date = _get_iso_8601_week(
                        m.group('isoyear'),
                        m.group('isoweek'),
                        m.group('isoweekday')
                    )
                except ParserError:
                    raise
                except ValueError:
                    raise ParserError('Invalid date string: {}'.format(text))

                year = date['year']
                month = date['month']
                day = date['day']
            else:
                # We have a classic date representation
                year = int(m.group('year'))

                if not m.group('monthday'):
                    # No month and day
                    month = 1
                    day = 1
                else:
                    if m.group('month') and m.group('day'):
                        # Month and day
                        if not m.group('daysep') and len(m.group('day')) == 1:
                            # Ordinal day
                            dt = datetime.strptime(
                                '{}-{}'.format(year, m.group('month') + m.group('day')),
                                '%Y-%j'
                            )
                            month = dt.month
                            day = dt.day
                        elif options['day_first']:
                            month = int(m.group('day'))
                            day = int(m.group('month'))
                        else:
                            month = int(m.group('month'))
                            day = int(m.group('day'))
                    else:
                        # Only month
                        if not m.group('monthsep'):
                            # The date looks like 201207
                            # which is invalid for a date
                            # But it might be a time in the form hhmmss
                            ambiguous_date = True

                        month = int(m.group('month'))
                        day = 1

            parsed.year = year
            parsed.month = month
            parsed.day = day
            parsed.is_date = True

        if not m.group('time'):
            # No time has been specified
            if ambiguous_date:
                # We can "safely" assume that the ambiguous date
                # was actually a time in the form hhmmss
                hhmmss = '{}{:0>2}'.format(
                    str(parsed['year']),
                    str(parsed['month'])
                )

                parsed.hour = int(hhmmss[:2])
                parsed.minute = int(hhmmss[2:4])
                parsed.second = int(hhmmss[4:])
                parsed.is_date = False
                parsed.is_time = True

            return parsed

        if ambiguous_date:
            raise ParserError('Invalid date string: {}'.format(text))

        if parsed.is_date and not m.group('timesep'):
            raise ParserError('Invalid date string: {}'.format(text))

        if parsed.is_date:
            parsed.is_datetime = True
            parsed.is_date = False
        else:
            parsed.is_time = True

        # Grabbing hh:mm:ss
        parsed.hour = int(m.group('hour'))

        if m.group('minute'):
            parsed.minute = int(m.group('minute'))

        if m.group('second'):
            parsed.second = int(m.group('second'))

        # Grabbing subseconds, if any
        if m.group('subsecondsection'):
            # Limiting to 6 chars
            subsecond = m.group('subsecond')[:6]

            parsed.microsecond = int('{:0<6}'.format(subsecond))

        # Grabbing timezone, if any
        tz = m.group('tz')
        if tz:
            if tz == 'Z':
                offset = 0
            else:
                negative = True if tz.startswith('-') else False
                tz = tz[1:]
                if ':' not in tz:
                    if len(tz) == 2:
                        tz = '{}00'.format(tz)

                    off_hour = tz[0:2]
                    off_minute = tz[2:4]
                else:
                    off_hour, off_minute = tz.split(':')

                offset = ((int(off_hour) * 60) + int(off_minute)) * 60

                if negative:
                    offset = -1 * offset

            parsed.offset = offset

        return parsed


def _parse_duration(text, parsed, **options):
    m = DURATION.match(text)
    if not m:
        return parsed

    parsed.is_duration = True
    fractional = False

    if m.group('w'):
        # Weeks
        if m.group('ymd') or m.group('hms'):
            # Specifying anything more than weeks is not supported
            raise ParserError('Invalid duration string')

        weeks = m.group('weeks')
        if not weeks:
            raise ParserError('Invalid duration string')

        weeks = weeks.replace(',', '.').replace('W', '')
        if '.' in weeks:
            weeks, portion = weeks.split('.')
            parsed.weeks = int(weeks)
            days = int(portion) / 10 * 7
            days, hours = int(days // 1), days % 1 * HOURS_PER_DAY
            parsed.days = days
            parsed.hours = hours
        else:
            parsed.weeks = int(weeks)

    if m.group('ymd'):
        # Years, months and/or days
        years = m.group('years')
        months = m.group('months')
        days = m.group('days')

        # Checking order
        years_start = m.start('years') if years else -3
        months_start = m.start('months') if months else years_start + 1
        days_start = m.start('days') if days else months_start + 1

        # Check correct order
        if not (years_start < months_start < days_start):
            raise ParserError('Invalid duration')

        if years:
            years = years.replace(',', '.').replace('Y', '')
            if '.' in years:
                fractional = True

                parsed.years = float(years)
            else:
                parsed.years = int(years)

        if months:
            if fractional:
                raise ParserError('Invalid duration')

            months = months.replace(',', '.').replace('M', '')
            if '.' in months:
                fractional = True

                parsed.months = float(months)
            else:
                parsed.months = int(months)

        if days:
            if fractional:
                raise ParserError('Invalid duration')

            days = days.replace(',', '.').replace('D', '')

            if '.' in days:
                fractional = True

                days, _hours = days.split('.')
                parsed.days = int(days)
                parsed.hours = int(_hours) / 10 * HOURS_PER_DAY
            else:
                parsed.days = int(days)

    if m.group('hms'):
        # Hours, minutes and/or seconds
        hours = m.group('hours') or 0
        minutes = m.group('minutes') or 0
        seconds = m.group('seconds') or 0

        # Checking order
        hours_start = m.start('hours') if hours else -3
        minutes_start = m.start('minutes') if minutes else hours_start + 1
        seconds_start = m.start('seconds') if seconds else minutes_start + 1

        # Check correct order
        if not (hours_start < minutes_start < seconds_start):
            raise ParserError('Invalid duration')

        if hours:
            if fractional:
                raise ParserError('Invalid duration')

            hours = hours.replace(',', '.').replace('H', '')

            if '.' in hours:
                fractional = True

                hours, _minutes = hours.split('.')
                parsed.hours += int(hours)
                parsed.minutes += int(_minutes) / 10 * MINUTES_PER_HOUR
            else:
                parsed.hours += int(hours)

        if minutes:
            if fractional:
                raise ParserError('Invalid duration')

            minutes = minutes.replace(',', '.').replace('M', '')

            if '.' in minutes:
                fractional = True

                minutes, _seconds = hours.split('.')
                parsed.hours += int(hours)
                seconds += int(_seconds) / 10 * SECONDS_PER_MINUTE
            else:
                parsed.minutes += int(minutes)

        if seconds:
            if fractional:
                raise ParserError('Invalid duration')

            seconds = seconds.replace(',', '.').replace('S', '')

            if '.' in seconds:
                fractional = True

                seconds, microseconds = seconds.split('.')
                parsed.seconds += int(seconds)
                parsed.microseconds = int('{:0<6}'.format(microseconds[:6]))
            else:
                parsed.seconds += int(seconds)

    return parsed


def _get_iso_8601_week(year, week, weekday):
    if not weekday:
        weekday = 1
    else:
        weekday = int(weekday)

    year = int(year)
    week = int(week)

    if week > 53:
        raise ParserError('Invalid week for week date')

    if weekday > 7:
        raise ParserError('Invalid weekday for week date')

    # We can't rely on strptime directly here since
    # it does not support ISO week date
    ordinal = week * 7 + weekday - (week_day(year, 1, 4) + 3)

    if ordinal < 1:
        # Previous year
        ordinal += days_in_year(year - 1)
        year -= 1

    if ordinal > days_in_year(year):
        # Next year
        ordinal -= days_in_year(year)
        year += 1

    fmt = '%Y-%j'
    string = '{}-{}'.format(year, ordinal)

    dt = datetime.strptime(string, fmt)

    return {
        'year': dt.year,
        'month': dt.month,
        'day': dt.day,
    }
