# -*- coding: utf-8 -*-

translations = {
    # Days
    'days': {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
    },
    'days_abbrev': {
        0: 'Sun',
        1: 'Mon',
        2: 'Tue',
        3: 'Wed',
        4: 'Thu',
        5: 'Fri',
        6: 'Sat'
    },

    # Months
    'months': {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December',
    },
    'months_abbrev': {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec',
    },

    # Units of time
    'year': ['{count} year', '{count} years'],
    'month': ['{count} month', '{count} months'],
    'week': ['{count} week', '{count} weeks'],
    'day': ['{count} day', '{count} days'],
    'hour': ['{count} hour', '{count} hours'],
    'minute': ['{count} minute', '{count} minutes'],
    'second': ['{count} second', '{count} seconds'],

    # Relative time
    'ago': '{time} ago',
    'from_now': '{time} from now',
    'after': '{time} after',
    'before': '{time} before',

    # Ordinals
    'ordinal': lambda x: 'th' if 10 <= x % 100 < 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(x % 10, "th"),

    # Meridians
    # [time] is a (hour, minute) tuple
    'meridian': lambda time: 'AM' if 0 <= time[0] < 12 else 'PM',

    # Date formats
    'date_formats': {
        'LTS': 'h:mm:ss A',
        'LT': 'h:mm A',
        'L': 'MM/DD/YYYY',
        'LL': 'MMMM D, YYYY',
        'LLL': 'MMMM D, YYYY h:mm A',
        'LLLL': 'dddd, MMMM D, YYYY h:mm A',
    },
}
