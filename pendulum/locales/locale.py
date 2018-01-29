import re
from importlib import import_module
from pathlib import Path


class Locale:
    """
    Represent a specific locale.
    """

    _cache = {}

    def __init__(self, locale, data):
        self._locale = locale
        self._data = data
        self._key_cache = {}

    @classmethod
    def load(cls, locale):
        if isinstance(locale, Locale):
            return locale

        locale = cls.normalize_locale(locale)
        if locale in cls._cache:
            return cls._cache[locale]

        # Checking locale existence
        actual_locale = locale
        locale_path = Path(__file__).parent / actual_locale
        while not locale_path.exists():
            if actual_locale == locale:
                raise ValueError(f'Locale [{locale}] does not exist.')

            actual_locale = actual_locale.split('_')[0]

        m = import_module(f'pendulum.locales.{actual_locale}.locale')

        cls._cache[locale] = cls(locale, m.locale)

        return cls._cache[locale]

    @classmethod
    def normalize_locale(cls, locale):
        m = re.match('([a-z]{2})[-_]([a-z]{2})', locale, re.I)
        if m:
            return '{}_{}'.format(m.group(1).lower(), m.group(2).lower())
        else:
            return locale.lower()

    def get(self, key, default=None):
        if key in self._key_cache:
            return self._key_cache[key]

        parts = key.split('.')
        try:
            result = self._data[parts[0]]
            for part in parts[1:]:
                result = result[part]
        except KeyError:
            result = default

        self._key_cache[key] = result

        return self._key_cache[key]

    def translation(self, key):
        return self.get(f'translations.{key}')

    def plural(self, number):
        return self._data['plural'](number)

    def ordinal(self, number):
        return self._data['ordinal'](number)

    def ordinalize(self, number):
        ordinal = self.get(f'custom.ordinal.{self.ordinal(number)}')

        if not ordinal:
            return f'{number}'

        return f'{number}{ordinal}'

    def match_translation(self, key, value):
        translations = self.translation(key)
        if value not in translations.values():
            return None

        return {v: k for k, v in translations.items()}[value]

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._locale}')"
