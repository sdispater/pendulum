import pendulum

import locale as _locale

from ..formatting import FORMATTERS


class FormattableMixing(object):

    # Default format to use for __str__ method when type juggling occurs.
    DEFAULT_TO_STRING_FORMAT = None

    _to_string_format = DEFAULT_TO_STRING_FORMAT

    @classmethod
    def reset_to_string_format(cls):
        """
        Reset the format used to the default
        when type juggling a Date instance to a string.
        """
        cls.set_to_string_format(cls.DEFAULT_TO_STRING_FORMAT)

    @classmethod
    def set_to_string_format(cls, fmt):
        """
        Set the default format used
        when type juggling a Date instance to a string

        :type fmt: str
        """
        cls._to_string_format = fmt

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
        if self._to_string_format is None:
            return self.isoformat()

        return self.format(self._to_string_format)

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, str(self))
