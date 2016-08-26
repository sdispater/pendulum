# -*- coding: utf-8 -*-


class Formatter(object):
    """
    Base class for all formatters.
    """

    def format(self, dt, fmt, locale=None):
        """
        Formats a Pendulum instance with a given format and locale.

        :param dt: The instance to format
        :type dt: Pendulum

        :param fmt: The format to use
        :type fmt: str

        :param locale: The locale to use
        :type locale: str or None

        :rtype: str
        """
        raise NotImplementedError()
