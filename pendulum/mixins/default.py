# -*- coding: utf-8 -*-

import locale as _locale
import warnings

from contextlib import contextmanager

from ..exceptions import PendulumDeprecationWarning
from ..translator import Translator
from ..formatting import FORMATTERS


class TranslatableMixin(object):

    _translator = None

    @classmethod
    def translator(cls):
        """
        Initialize the translator instance if necessary.

        :rtype: Translator
        """
        if cls._translator is None:
            cls._translator = Translator('en')
            cls.set_locale('en')

        return cls._translator

    @classmethod
    def set_translator(cls, translator):
        """
        Set the translator instance to use.

        :param translator: The translator
        :type translator: Translator
        """
        cls._translator = translator

    @classmethod
    def get_locale(cls):
        """
        Get the current translator locale.

        :rtype: str
        """
        return cls.translator().locale

    @classmethod
    def set_locale(cls, locale):
        """
        Set the current translator locale and
        indicate if the source locale file exists.

        :type locale: str

        :rtype: bool
        """
        if not cls.translator().has_translations(locale):
            return False

        cls.translator().locale = locale

        return True


class FormattableMixing(object):

    # Default format to use for __str__ method when type juggling occurs.
    DEFAULT_TO_STRING_FORMAT = None

    _to_string_format = DEFAULT_TO_STRING_FORMAT

    _DEFAULT_FORMATTER = 'classic'
    _FORMATTER = _DEFAULT_FORMATTER

    @classmethod
    def reset_to_string_format(cls):
        """
        Reset the format used to the default
        when type juggling a Date instance to a string.
        """
        warnings.warn(
            'The reset_to_string_format() helper '
            'will be removed in version 2.0.',
            PendulumDeprecationWarning,
            stacklevel=2
        )
        cls.set_to_string_format(cls.DEFAULT_TO_STRING_FORMAT)

    @classmethod
    def set_to_string_format(cls, fmt):
        """
        Set the default format used
        when type juggling a Date instance to a string

        :type fmt: str
        """
        warnings.warn(
            'The set_to_string_format() helper '
            'will be removed in version 2.0.',
            PendulumDeprecationWarning,
            stacklevel=2
        )
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
            formatter = self._FORMATTER

        if formatter not in FORMATTERS:
            raise ValueError('Invalid formatter [{}]'.format(formatter))

        return FORMATTERS[formatter].format(self, fmt, locale)

    def strftime(self, fmt):
        """
        Formats the instance using the given format.

        :param fmt: The format to use
        :type fmt: str

        :rtype: str
        """
        return self.format(fmt, _locale.getlocale()[0], 'classic')

    @classmethod
    def set_formatter(cls, formatter=None):
        """
        Sets the default string formatter.

        :param formatter: The parameter to set as default.
        :type formatter: str or None
        """
        if formatter is None:
            formatter = cls._DEFAULT_FORMATTER

        if formatter not in FORMATTERS:
            raise ValueError('Invalid formatter [{}]'.format(formatter))

        cls._FORMATTER = formatter

    @classmethod
    def get_formatter(cls):
        """
        Gets the currently used string formatter.

        :rtype: str
        """
        return cls._FORMATTER

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

        return self.format(self._to_string_format, formatter='classic')

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, str(self))


class TestableMixin(object):

    # A test Pendulum instance to be returned when now instances are created.
    _test_now = None

    @classmethod
    @contextmanager
    def test(cls, mock):
        """
        Context manager to temporarily set the test_now value.

        :type mock: Pendulum or Date or Time or None
        """
        cls.set_test_now(mock)

        yield

        cls.set_test_now()

    @classmethod
    def set_test_now(cls, test_now=None):
        """
        Set a Pendulum instance (real or mock) to be returned when a "now"
        instance is created.  The provided instance will be returned
        specifically under the following conditions:
            - A call to the classmethod now() method, ex. Pendulum.now()
            - When nothing is passed to the constructor or parse(), ex. Pendulum()
            - When the string "now" is passed to parse(), ex. Pendulum.parse('now')

        Note the timezone parameter was left out of the examples above and
        has no affect as the mock value will be returned regardless of its value.

        To clear the test instance call this method using the default
        parameter of null.

        :type test_now: Pendulum or None
        """
        cls._test_now = test_now

    @classmethod
    def get_test_now(cls):
        """
        Get the Pendulum instance (real or mock) to be returned when a "now"
        instance is created.

        :rtype: Pendulum or None
        """
        return cls._test_now

    @classmethod
    def has_test_now(cls):
        return cls._test_now is not None
