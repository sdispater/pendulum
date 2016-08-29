# -*- coding: utf-8 -*-

translations = {
    # Days
    'days': {
        0: '일요일',
        1: '월요일',
        2: '화요일',
        3: '수요일',
        4: '목요일',
        5: '금요일',
        6: '토요일'
    },
    'days_abbrev': {
        0: '일',
        1: '월',
        2: '화',
        3: '수',
        4: '목',
        5: '금',
        6: '토'
    },

    # Months
    'months': {
        1: '1월',
        2: '2월',
        3: '3월',
        4: '4월',
        5: '5월',
        6: '6월',
        7: '7월',
        8: '8월',
        9: '9월',
        10: '10월',
        11: '11월',
        12: '12월',
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
    'year': '{count} 년',
    'month': '{count} 개월',
    'week': '{count} 주일',
    'day': '{count} 일',
    'hour': '{count} 시간',
    'minute': '{count} 분',
    'second': '{count} 초',

    # Relative time
    'ago': '{time} 전',
    'from_now': '{time} 후',
    'after': '{time} 뒤',
    'before': '{time} 앞',

    # Meridians
    'meridian': lambda time: '오전' if 0 <= time[0] < 12 else '오후',

    # Date formats
    'date_formats': {
        'LTS': 'A h시 m분 s초',
        'LT': 'A h시 m분',
        'LLLL': 'YYYY년 MMMM D일 dddd A h시 m분',
        'LLL': 'YYYY년 MMMM D일 A h시 m분',
        'LL': 'YYYY년 MMMM D일',
        'L': 'YYYY.MM.DD',
    },
}
