# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .custom import translations as custom_translations


"""
tr locale file.

It has been generated automatically and must not be modified directly.
"""


locale = {
    "plural": lambda n: "one"
    if ((n == n and ((n == 1))) and (0 == 0 and ((0 == 0))))
    else "other",
    "ordinal": lambda n: "few"
    if (
        ((n % 10) == (n % 10) and (((n % 10) == 3)))
        and (not ((n % 100) == (n % 100) and (((n % 100) == 13))))
    )
    else "one"
    if (
        ((n % 10) == (n % 10) and (((n % 10) == 1)))
        and (not ((n % 100) == (n % 100) and (((n % 100) == 11))))
    )
    else "two"
    if (
        ((n % 10) == (n % 10) and (((n % 10) == 2)))
        and (not ((n % 100) == (n % 100) and (((n % 100) == 12))))
    )
    else "other",
    "translations": {
        "days": {
            "abbreviated": {
                0: "Paz",
                1: "Pzt",
                2: "Sal",
                3: "Çar",
                4: "Per",
                5: "Cum",
                6: "Cmt",
            },
            "narrow": {0: "P", 1: "P", 2: "S", 3: "Ç", 4: "P", 5: "C", 6: "C"},
            "short": {0: "Pa", 1: "Pt", 2: "Sa", 3: "Ça", 4: "Pe", 5: "Cu", 6: "Ct"},
            "wide": {
                0: "Pazar",
                1: "Pazartesi",
                2: "Salı",
                3: "Çarşamba",
                4: "Perşembe",
                5: "Cuma",
                6: "Cumartesi",
            },
        },
        "months": {
            "abbreviated": {
                1: "Oca",
                2: "Şub",
                3: "Mar",
                4: "Nis",
                5: "May",
                6: "Haz",
                7: "Tem",
                8: "Ağu",
                9: "Eyl",
                10: "Eki",
                11: "Kas",
                12: "Ara",
            },
            "narrow": {
                1: "O",
                2: "Ş",
                3: "M",
                4: "N",
                5: "M",
                6: "H",
                7: "T",
                8: "A",
                9: "E",
                10: "E",
                11: "K",
                12: "A",
            },
            "wide": {
                1: "Ocak",
                2: "Şubat",
                3: "Mart",
                4: "Nisan",
                5: "Mayıs",
                6: "Haziran",
                7: "Temmuz",
                8: "Ağustos",
                9: "Eylül",
                10: "Ekim",
                11: "Kasım",
                12: "Aralık",
            },
        },
        "units": {
            "year": {"one": "{0} yıl", "other": "{0} yıl"},
            "month": {"one": "{0} ay", "other": "{0} ay"},
            "week": {"one": "{0} hafta", "other": "{0} hafta"},
            "day": {"one": "{0} gün", "other": "{0} gün"},
            "hour": {"one": "{0} saat", "other": "{0} saat"},
            "minute": {"one": "{0} dakika", "other": "{0} dakika"},
            "second": {"one": "{0} saniye", "other": "{0} saniye"},
            "microsecond": {"one": "{0} mikrosaniye", "other": "{0} mikrosaniye"},
        },
        "relative": {
            "year": {
                "future": {"other": "{0} yıl sonra", "one": "{0} yıl sonra"},
                "past": {"other": "{0} yıl önce", "one": "{0} yıl önce"},
            },
            "month": {
                "future": {"other": "{0} ay sonra", "one": "{0} ay sonra"},
                "past": {"other": "{0} ay önce", "one": "{0} ay önce"},
            },
            "week": {
                "future": {"other": "{0} hafta sonra", "one": "{0} hafta sonra"},
                "past": {"other": "{0} hafta önce", "one": "{0} hafta önce"},
            },
            "day": {
                "future": {"other": "{0} gün sonra", "one": "{0} gün sonra"},
                "past": {"other": "{0} gün önce", "one": "{0} gün önce"},
            },
            "hour": {
                "future": {"other": "{0} saat sonra", "one": "{0} saat sonra"},
                "past": {"other": "{0} saat önce", "one": "{0} saat önce"},
            },
            "minute": {
                "future": {"other": "{0} dakika sonra", "one": "{0} dakika sonra"},
                "past": {"other": "{0} dakika önce", "one": "{0} dakika önce"},
            },
            "second": {
                "future": {"other": "{0} saniye sonra", "one": "{0} saniye sonra"},
                "past": {"other": "{0} saniye önce", "one": "{0} saniye önce"},
            },
        },
        "day_periods": {
            "midnight": "gece yarısı",
            "am": "ÖÖ",
            "noon": "öğle",
            "pm": "ÖS",
            "morning1": "sabah",
            "morning2": "öğleden önce",
            "afternoon1": "öğleden sonra",
            "afternoon2": "akşamüstü",
            "evening1": "akşam",
            "night1": "gece",
        },
    },
    "custom": custom_translations,
}
