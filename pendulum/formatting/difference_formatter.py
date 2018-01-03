# -*- coding: utf-8 -*-

from .._compat import decode
from ..translator import Translator


class DifferenceFormatter(object):
    """
    Handles formatting differences in text.
    """

    def __init__(self, translator=Translator()):
        self._translator = translator

    def diff_for_humans(self, date, other=None, absolute=False, locale=None):
        """
        Get the difference in a human readable format.

        :param date: The datetime to start with.
        :type date: pendulum.Date or pendulum.Pendulum

        :param other: The datetime to compare against (defaults to now).
        :type other: pendulum.Date or pendulum.Pendulum or None

        :param absolute: Removes time difference modifiers ago, after, etc
        :type absolute: bool

        :param locale: The locale to use
        :type locale: str or None

        :rtype: str
        """
        is_now = other is None

        if is_now:
            if hasattr(date, 'now'):
                other = date.now(date.timezone)
            else:
                other = date.today()

        diff = date.diff(other)

        count = diff.remaining_seconds
        unit = 'second'

        if diff.years > 0:
            unit = 'year'
            count = diff.years

            if diff.months > 6:
                count += 1
        elif diff.months == 11 and (diff.weeks * 7 + diff.remaining_days) > 15:
            unit = 'year'
            count = 1
        elif diff.months > 0:
            unit = 'month'
            count = diff.months

            if (diff.weeks * 7 + diff.remaining_days) >= 27:
                count += 1
        elif diff.weeks > 0:
            unit = 'week'
            count = diff.weeks

            if diff.remaining_days > 3:
                count += 1
        elif diff.remaining_days > 0:
            unit = 'day'
            count = diff.remaining_days
        elif diff.hours > 0:
            unit = 'hour'
            count = diff.hours
        elif diff.minutes > 0:
            unit = 'minute'
            count = diff.minutes

        if count == 0:
            count = 1

        time = self._translator.transchoice(unit, count, {'count': count}, locale=locale)

        if absolute:
            return decode(time)

        is_future = diff.invert

        if is_now:
            trans_id = 'from_now' if is_future else 'ago'
        else:
            trans_id = 'after' if is_future else 'before'

        # Some langs have special pluralization for past and future tense
        try_key_exists = '%s_%s' % (unit, trans_id)
        if try_key_exists != self._translator.transchoice(try_key_exists, count, locale=locale):
            time = self._translator.transchoice(try_key_exists, count, {'count': count}, locale=locale)

        trans = self._translator.trans(trans_id, {'time': time}, locale=locale)

        return decode(trans)
