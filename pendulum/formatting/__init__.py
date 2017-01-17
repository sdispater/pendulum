# -*- coding: utf-8 -*-

from .formatter import Formatter
from .classic_formatter import ClassicFormatter
from .alternative_formatter import AlternativeFormatter


FORMATTERS = {
    'classic': ClassicFormatter(),
    'alternative': AlternativeFormatter(),
}


def register_formatter(name, formatter):
    """
    Register a new formatter.

    :param name: The name of the formatter.
    :type name: str

    :param formatter: The formatter instance
    :type formatter: Formatter

    :rtype: None
    """
    if name in FORMATTERS:
        raise ValueError('Formatter [{}] already exists'.format(name))

    if not isinstance(formatter, Formatter):
        raise ValueError(
            'The formatter instance '
            'must be an instance of Formatter'
        )

    FORMATTERS[name] = formatter
