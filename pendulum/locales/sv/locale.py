from .custom import translations as custom_translations


"""
sv locale file.

It has been generated automatically and must not be modified directly.
"""


locale = {
    "plural": lambda n: "one"
    if ((n == n and (n == 1)) and (0 == 0 and (0 == 0)))
    else "other",
    "ordinal": lambda n: "one"
    if (
        ((n % 10) == (n % 10) and (((n % 10) == 1) or ((n % 10) == 2)))
        and (not ((n % 100) == (n % 100) and (((n % 100) == 11) or ((n % 100) == 12))))
    )
    else "other",
    "translations": {
        "days": {
            "abbreviated": {
                0: "sön",
                1: "mån",
                2: "tis",
                3: "ons",
                4: "tors",
                5: "fre",
                6: "lör",
            },
            "narrow": {
                0: "S",
                1: "M",
                2: "T",
                3: "O",
                4: "T",
                5: "F",
                6: "L",
            },
            "short": {
                0: "sö",
                1: "må",
                2: "ti",
                3: "on",
                4: "to",
                5: "fr",
                6: "lö",
            },
            "wide": {
                0: "söndag",
                1: "måndag",
                2: "tisdag",
                3: "onsdag",
                4: "torsdag",
                5: "fredag",
                6: "lördag",
            },
        },
        "months": {
            "abbreviated": {
                1: "jan.",
                2: "feb.",
                3: "mars",
                4: "apr.",
                5: "maj",
                6: "juni",
                7: "juli",
                8: "aug.",
                9: "sep.",
                10: "okt.",
                11: "nov.",
                12: "dec.",
            },
            "narrow": {
                1: "J",
                2: "F",
                3: "M",
                4: "A",
                5: "M",
                6: "J",
                7: "J",
                8: "A",
                9: "S",
                10: "O",
                11: "N",
                12: "D",
            },
            "wide": {
                1: "januari",
                2: "februari",
                3: "mars",
                4: "april",
                5: "maj",
                6: "juni",
                7: "juli",
                8: "augusti",
                9: "september",
                10: "oktober",
                11: "november",
                12: "december",
            },
        },
        "units": {
            "year": {
                "one": "{0} år",
                "other": "{0} år",
            },
            "month": {
                "one": "{0} månad",
                "other": "{0} månader",
            },
            "week": {
                "one": "{0} vecka",
                "other": "{0} veckor",
            },
            "day": {
                "one": "{0} dygn",
                "other": "{0} dygn",
            },
            "hour": {
                "one": "{0} timme",
                "other": "{0} timmar",
            },
            "minute": {
                "one": "{0} minut",
                "other": "{0} minuter",
            },
            "second": {
                "one": "{0} sekund",
                "other": "{0} sekunder",
            },
            "microsecond": {
                "one": "{0} mikrosekund",
                "other": "{0} mikrosekunder",
            },
        },
        "relative": {
            "year": {
                "future": {
                    "other": "om {0} år",
                    "one": "om {0} år",
                },
                "past": {
                    "other": "för {0} år sedan",
                    "one": "för {0} år sedan",
                },
            },
            "month": {
                "future": {
                    "other": "om {0} månader",
                    "one": "om {0} månad",
                },
                "past": {
                    "other": "för {0} månader sedan",
                    "one": "för {0} månad sedan",
                },
            },
            "week": {
                "future": {
                    "other": "om {0} veckor",
                    "one": "om {0} vecka",
                },
                "past": {
                    "other": "för {0} veckor sedan",
                    "one": "för {0} vecka sedan",
                },
            },
            "day": {
                "future": {
                    "other": "om {0} dagar",
                    "one": "om {0} dag",
                },
                "past": {
                    "other": "för {0} dagar sedan",
                    "one": "för {0} dag sedan",
                },
            },
            "hour": {
                "future": {
                    "other": "om {0} timmar",
                    "one": "om {0} timme",
                },
                "past": {
                    "other": "för {0} timmar sedan",
                    "one": "för {0} timme sedan",
                },
            },
            "minute": {
                "future": {
                    "other": "om {0} minuter",
                    "one": "om {0} minut",
                },
                "past": {
                    "other": "för {0} minuter sedan",
                    "one": "för {0} minut sedan",
                },
            },
            "second": {
                "future": {
                    "other": "om {0} sekunder",
                    "one": "om {0} sekund",
                },
                "past": {
                    "other": "för {0} sekunder sedan",
                    "one": "för {0} sekund sedan",
                },
            },
        },
        "day_periods": {
            "midnight": "midnatt",
            "am": "fm",
            "pm": "em",
            "morning1": "på morgonen",
            "morning2": "på förmiddagen",
            "afternoon1": "på eftermiddagen",
            "evening1": "på kvällen",
            "night1": "på natten",
        },
    },
    "custom": custom_translations,
}
