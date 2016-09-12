# -*- coding: utf-8 -*-

from .default import TranslatableMixin


class WordableIntervalMixin(TranslatableMixin):

    def in_words(self, locale=None, separator=' '):
        """
        Get the current interval in words in the current locale.

        Ex: 6 jours 23 heures 58 minutes

        :param locale: The locale to use. Defaults to current locale.
        :type locale: str

        :param separator: The separator to use between each unit
        :type separator: str

        :rtype: str
        """
        periods = [
            ('week', self.weeks),
            ('day', self.days_exclude_weeks),
            ('hour', self.hours),
            ('minute', self.minutes),
            ('second', self.seconds)
        ]

        parts = []
        for period in periods:
            unit, count = period
            if abs(count) > 0:
                parts.append(
                    self.translator().transchoice(unit, abs(count), {'count': count}, locale=locale)
                )

        return separator.join(parts)

    def __str__(self):
        return self.in_words()

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, str(self))
