# -*- coding: utf-8 -*-

translations = {
    # Days
    'days': {
        0: 'Sondag',
        1: 'Maandag',
        2: 'Dinsdag',
        3: 'Woensdag',
        4: 'Donderdag',
        5: 'Vrydag',
        6: 'Saterdag'
    },
    'days_abbrev': {
        0: 'Son',
        1: 'Maa',
        2: 'Din',
        3: 'Woe',
        4: 'Don',
        5: 'Vry',
        6: 'Sat'
    },

    # Months
    'months': {
        1: 'Januarie',
        2: 'Februarie',
        3: 'Maart',
        4: 'April',
        5: 'Mei',
        6: 'Junie',
        7: 'Julie',
        8: 'Augustus',
        9: 'September',
        10: 'Oktober',
        11: 'November',
        12: 'Desember',
    },
    'months_abbrev': {
        1: 'Jan',
        2: 'Feb',
        3: 'Mrt',
        4: 'Apr',
        5: 'Mei',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Okt',
        11: 'Nov',
        12: 'Des',
    },

    # Units of time
    'year': ['1 jaar', '{count} jare'],
    'month': ['1 maand', '{count} maande'],
    'week': ['1 week', '{count} weke'],
    'day': ['1 dag', '{count} dae'],
    'hour': ['1 uur', '{count} ure'],
    'minute': ['1 minuut', '{count} minute'],
    'second': ['1 sekond', '{count} sekondes'],

    # Relative time
    'ago': '{time} terug',
    'from_now': '{time} van nou af',
    'after': '{time} na',
    'before': '{time} voor',

    # Meridians
    'meridian': lambda hour: 'VM' if 0 <= hour < 12 else 'NM',
}

