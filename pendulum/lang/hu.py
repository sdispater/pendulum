# -*- coding: utf-8 -*-

translations = {
    # Days
    'days': {
        0: 'vasárnap',
        1: 'hétfő',
        2: 'kedd',
        3: 'szerda',
        4: 'csütörtök',
        5: 'péntek',
        6: 'szombat'
    },
    'days_abbrev': {
        0: 'vas',
        1: 'hét',
        2: 'kedd',
        3: 'szer',
        4: 'csüt',
        5: 'pént',
        6: 'szom'
    },

    # Months
    'months': {
        1: 'január',
        2: 'február',
        3: 'március',
        4: 'április',
        5: 'május',
        6: 'június',
        7: 'július',
        8: 'augusztus',
        9: 'szeptember',
        10: 'október',
        11: 'november',
        12: 'december',
    },
    'months_abbrev': {
        1: 'jan',
        2: 'febr',
        3: 'márc',
        4: 'ápr',
        5: 'máj',
        6: 'jún',
        7: 'júl',
        8: 'aug',
        9: 'szept',
        10: 'okt',
        11: 'nov',
        12: 'dec',
    },

    # Units of time
    'year': '{count} év',
    'month': '{count} hónap',
    'week': '{count} hét',
    'day': '{count} nap',
    'hour': '{count} óra',
    'minute': '{count} perc',
    'second': '{count} másodperc',

    # Relative time
    'ago': '{time}',
    'from_now': '{time} múlva',
    'after': '{time} később',
    'before': '{time} korábban',

    'year_ago': '{count} éve',
    'month_ago': '{count} hónapja',
    'week_ago': '{count} hete',
    'day_ago': '{count} napja',
    'hour_ago': '{count} órája',
    'minute_ago': '{count} perce',
    'second_ago': '{count} másodperce',

    'year_after': '{count} évvel',
    'month_after': '{count} hónappal',
    'week_after': '{count} héttel',
    'day_after': '{count} nappal',
    'hour_after': '{count} órával',
    'minute_after': '{count} perccel',
    'second_after': '{count} másodperccel',

    'year_before': '{count} évvel',
    'month_before': '{count} hónappal',
    'week_before': '{count} héttel',
    'day_before': '{count} nappal',
    'hour_before': '{count} órával',
    'minute_before': '{count} perccel',
    'second_before': '{count} másodperccel',

    # Meridians
    'meridian': lambda time: 'DE' if 0 <= time[0] < 12 else 'DU',

    # Date formats
    'date_formats': {
        'LTS': 'H:mm:ss',
        'LT': 'H:mm',
        'LLLL': 'YYYY. MMMM D., dddd H:mm',
        'LLL': 'YYYY. MMMM D. H:mm',
        'LL': 'YYYY. MMMM D.',
        'L': 'YYYY.MM.DD.',
    },
}
