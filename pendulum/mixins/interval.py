import pendulum

from ..locales.locale import Locale


class WordableDurationMixin:

    def in_words(self, locale=None, separator=' ', _periods=None):
        """
        Get the current interval in words in the current locale.

        Ex: 6 jours 23 heures 58 minutes

        :param locale: The locale to use. Defaults to current locale.
        :type locale: str

        :param separator: The separator to use between each unit
        :type separator: str

        :param _periods: Custom periods to use as word parts
        :type _periods: list or None

        :rtype: str
        """
        if _periods is None:
            _periods = [
                ('year', self.years),
                ('month', self.months),
                ('week', self.weeks),
                ('day', self.remaining_days),
                ('hour', self.hours),
                ('minute', self.minutes),
                ('second', self.remaining_seconds)
            ]

        if locale is None:
            locale = pendulum.get_locale()

        locale = pendulum.locale(locale)
        parts = []
        for period in _periods:
            unit, count = period
            if abs(count) > 0:
                translation = locale.translation(
                    f'units.{unit}.{locale.plural(abs(count))}'
                )
                parts.append(translation.format(count))

        if not parts and abs(self.microseconds) > 0:
            translation = locale.translation(
                f'units.second.{locale.plural(1)}'
            )
            us = abs(self.microseconds) / 1e6
            parts.append(
                translation.format(f'{us:.2f}')
            )

        return separator.join(parts)

    def __str__(self):
        return self.in_words()
