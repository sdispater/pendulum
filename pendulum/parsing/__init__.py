# -*- coding: utf-8 -*-

from .parser import Parser


def parse(text, **options):
    """
    Parses a string with the given options.

    :param text: The string to parse.
    :type text: str

    :param options: The parsing options.
    :type options: dict

    :rtype: dict

    :raises: ParserError
    """
    return Parser(**options).parse(text)
