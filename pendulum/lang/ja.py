# -*- coding: utf-8 -*-

translations = {
    # Days
    'days': {
        0: '日曜日',
        1: '月曜日',
        2: '火曜日',
        3: '水曜日',
        4: '木曜日',
        5: '金曜日',
        6: '土曜日'
    },
    'days_abbrev': {
        0: '日',
        1: '月',
        2: '火',
        3: '水',
        4: '木',
        5: '金',
        6: '土'
    },

    # Months
    'months': {
        1: '1月',
        2: '2月',
        3: '3月',
        4: '4月',
        5: '5月',
        6: '6月',
        7: '7月',
        8: '8月',
        9: '9月',
        10: '10月',
        11: '11月',
        12: '12月',
    },
    'months_abbrev': {
        1: ' 1',
        2: ' 2',
        3: ' 3',
        4: ' 4',
        5: ' 5',
        6: ' 6',
        7: ' 7',
        8: ' 8',
        9: ' 9',
        10: '10',
        11: '11',
        12: '12',
    },

    # Units of time
    'year': '{count} 年',
    'month': '{count} ヶ月',
    'week': '{count} 週間',
    'day': '{count} 日',
    'hour': '{count} 時間',
    'minute': '{count} 分',
    'second': '{count} 秒',

    # Relative time
    'ago': '{time} 前',
    'from_now': '今から {time}',
    'after': '{time} 後',
    'before': '{time} 前',

    # Meridians
    'meridian': lambda time: '午前' if 0 <= time[0] < 12 else '午後',

    # Date formats
    'date_formats': {
        'LTS': 'Ah時m分s秒',
        'LT': 'Ah時m分',
        'LLLL': 'YYYY年M月D日Ah時m分 dddd',
        'LLL': 'YYYY年M月D日Ah時m分',
        'LL': 'YYYY年M月D日',
        'L': 'YYYY/MM/DD',
    },
}
