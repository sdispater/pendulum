# -*- coding: utf-8 -*-

translations = {
    # Days
    'days': {
        0: 'dimanĉo',
        1: 'lundo',
        2: 'mardo',
        3: 'merkredo',
        4: 'ĵaŭdo',
        5: 'vendredo',
        6: 'sabato'
    },
    'days_abbrev': {
        0: 'dim',
        1: 'lun',
        2: 'mar',
        3: 'mer',
        4: 'ĵaŭ',
        5: 'ven',
        6: 'sab'
    },

    # Months
    'months': {
        1: 'januaro',
        2: 'februaro',
        3: 'marto',
        4: 'aprilo',
        5: 'majo',
        6: 'junio',
        7: 'julio',
        8: 'aŭgusto',
        9: 'septembro',
        10: 'oktobro',
        11: 'novembro',
        12: 'decembro',
    },
    'months_abbrev': {
        1: 'jan',
        2: 'feb',
        3: 'mar',
        4: 'apr',
        5: 'maj',
        6: 'jun',
        7: 'jul',
        8: 'aŭg',
        9: 'sep',
        10: 'okt',
        11: 'nov',
        12: 'dec',
    },

    # Units of time
    'year': ['{count} jaro', '{count} jaroj'],
    'month': ['{count} monato', '{count} monatoj'],
    'week': ['{count} semajno', '{count} semajnoj'],
    'day': ['{count} tago', '{count} tagoj'],
    'hour': ['{count} horo', '{count} horoj'],
    'minute': ['{count} minuto', '{count} minutoj'],
    'second': ['{count} sekundo', '{count} sekundoj'],

    # Relative time
    'ago': 'antaŭ {time}',
    'from_now': 'je {time}',
    'after': '{time} poste',
    'before': '{time} antaŭe',

    # Meridians
    'meridian': lambda time: 'ATM' if 0 <= time[0] < 12 else 'PTM',

    # Date formats
    'date_formats': {
        'LTS': 'HH:mm:ss',
        'LT': 'HH:mm',
        'LLLL': 'dddd, [la] D[-an de] MMMM, YYYY HH:mm',
        'LLL': 'D[-an de] MMMM, YYYY HH:mm',
        'LL': 'D[-an de] MMMM, YYYY',
        'L': 'YYYY-MM-DD',
    },
}
