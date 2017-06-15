import pendulum

import locale as _locale

from ..formatting import FORMATTERS


class FormattableMixing(object):

    def format(self, fmt, locale=None, formatter=None):
        """
        Formats the instance using the given format.

        :param fmt: The format to use
        :type fmt: str

        :param locale: The locale to use
        :type locale: str or None

        :param formatter: The formatter to use
        :type formatter: str or None

        :rtype: str
        """
        if formatter is None:
            formatter = pendulum.get_formatter()
        elif formatter not in FORMATTERS:
            raise ValueError('Invalid formatter [{}]'.format(formatter))
        else:
            formatter = FORMATTERS[formatter]

        return formatter.format(self, fmt, locale)

    def strftime(self, fmt):
        """
        Formats the instance using the given format.

        :param fmt: The format to use
        :type fmt: str

        :rtype: str
        """
        return self.format(fmt, _locale.getlocale()[0], 'classic')

    def for_json(self):
        """
        Methods for automatic json serialization by simplejson

        :rtype: str
        """
        return str(self)

    def __format__(self, format_spec):
        if len(format_spec) > 0:
            return self.format(format_spec)

        return str(self)

    def __str__(self):
        return self.isoformat()
