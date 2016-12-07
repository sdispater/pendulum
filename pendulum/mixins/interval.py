# -*- coding: utf-8 -*-

from .default import TranslatableMixin


class WordableIntervalMixin(TranslatableMixin):

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
                ('week', self.weeks),
                ('day', self.remaining_days),
                ('hour', self.hours),
                ('minute', self.minutes),
                ('second', self.remaining_seconds)
            ]

        parts = []
        for period in _periods:
            unit, count = period
            if abs(count) > 0:
                parts.append(
                    self.translator().transchoice(
                        unit, abs(count), {'count': count}, locale=locale
                    )
                )

        if not parts and abs(self.microseconds) > 0:
            translation = self.translator().transchoice(
                'second', 1,
                {'count': '{:.2f}'.format(abs(self.microseconds) / 1e6)},
                locale=locale
            )
            parts.append(translation)

        return separator.join(parts)

    def __str__(self):
        return self.in_words()

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, str(self))
