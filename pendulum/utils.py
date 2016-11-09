# -*- coding: utf-8 -*-

import functools
import warnings

from ._compat import PY3K


def deprecated(message=None):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    :param message: The deprecation message.
    :type message: str or None
    """

    def _deprecated(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if PY3K:
                func_code = func.__code__
            else:
                func_code = func.func_code

            warnings.warn_explicit(
                message or "Call to deprecated function {}.".format(func.__name__),
                category=DeprecationWarning,
                filename=func_code.co_filename,
                lineno=func_code.co_firstlineno + 1
            )

            return func(*args, **kwargs)

        return wrapper

    return _deprecated
