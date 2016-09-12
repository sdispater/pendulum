# -*- coding: utf-8 -*-

translations = {
    # Days
    'days': {
        0: 'یکشنبه',
        1: 'دو شنبه',
        2: 'سه شنبه',
        3: 'چهارشنبه',
        4: 'پنجشنبه',
        5: 'جمعه',
        6: 'شنبه'
    },
    'days_abbrev': {
        0: 'یکشنبه',
        1: 'دوشنبه',
        2: 'سهشنبه',
        3: 'چهارشنبه',
        4: 'پنجشنبه',
        5: 'جمعه',
        6: 'شنبه'
    },

    # Months
    'months': {
        1: 'ژانویه',
        2: 'فوریه',
        3: 'مارس',
        4: 'آوریل',
        5: 'مه',
        6: 'ژوئن',
        7: 'ژوئیه',
        8: 'اوت',
        9: 'سپتامبر',
        10: 'اکتبر',
        11: 'نوامبر',
        12: 'دسامبر'
    },
    'months_abbrev': {
        1: 'ژانویه',
        2: 'فوریه',
        3: 'مارس',
        4: 'آوریل',
        5: 'مه',
        6: 'ژوئن',
        7: 'ژوئیه',
        8: 'اوت',
        9: 'سپتامبر',
        10: 'اکتبر',
        11: 'نوامبر',
        12: 'دسامبر',
    },

    # Units of time
    'year': '{count} سال',
    'month': '{count} ماه',
    'week': '{count} هفته',
    'day': '{count} روز',
    'hour': '{count} ساعت',
    'minute': '{count} دقیقه',
    'second': '{count} ثانیه',

    # Relative time
    'ago': '{time} پیش',
    'from_now': '{time} بعد',
    'after': '{time} پس از',
    'before': '{time} پیش از',

    # Meridians
    'meridian': lambda time: 'قبل از ظهر' if 0 <= time[0] < 12 else 'بعد از ظهر',

    # Date formats
    'date_formats': {
        'LTS': 'HH:mm:ss',
        'LT': 'HH:mm',
        'LLLL': 'dddd, D MMMM YYYY HH:mm',
        'LLL': 'D MMMM YYYY HH:mm',
        'LL': 'D MMMM YYYY',
        'L': 'DD/MM/YYYY',
    },
}
