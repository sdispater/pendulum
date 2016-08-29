# -*- coding: utf-8 -*-


def meridian(hour, minute):
    hm = hour * 100 + minute

    if hm < 600:
        return '凌晨'
    elif hm < 900:
        return '早上'
    elif hm < 1130:
        return '上午'
    elif hm < 1230:
        return '中午'
    elif hm < 1800:
        return '下午'

    return '晚上'


translations = {
    # Days
    'days': {
        0: '星期日',
        1: '星期一',
        2: '星期二',
        3: '星期三',
        4: '星期四',
        5: '星期五',
        6: '星期六'
    },
    'days_abbrev': {
        0: '日',
        1: '一',
        2: '二',
        3: '三',
        4: '四',
        5: '五',
        6: '六'
    },

    # Months
    'months': {
        1: '一月',
        2: '二月',
        3: '三月',
        4: '四月',
        5: '五月',
        6: '六月',
        7: '七月',
        8: '八月',
        9: '九月',
        10: '十月',
        11: '十一月',
        12: '十二月',
    },
    'months_abbrev': {
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

    # Units of time
    'year': '{count}年',
    'month': '{count}个月',
    'week': '{count}周',
    'day': '{count}天',
    'hour': '{count}小时',
    'minute': '{count}分钟',
    'second': '{count}秒',

    # Relative time
    'ago': '{time}前',
    'from_now': '距现在{time}',
    'after': '{time}后',
    'before': '{time}前',

    # Meridians
    'meridian': lambda time: meridian(*time),

    # Date formats
    'date_formats': {
        'LTS': 'Ah点m分s秒',
        'LT': 'Ah点mm分',
        'LLLL': 'YYYY年MMMD日ddddAh点mm分',
        'LLL': 'YYYY年MMMD日Ah点mm分',
        'LL': 'YYYY年MMMD日',
        'L': 'YYYY-MM-DD',
    },
}

