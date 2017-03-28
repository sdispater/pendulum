# -*- coding: utf-8 -*-

from .mixins.default import (
    TestableMixin, FormattableMixing, TranslatableMixin
)
from .datetime import DateTime
from .date import Date
from .time import Time


class Global(TestableMixin, FormattableMixing, TranslatableMixin):

    @classmethod
    def set_test_now(cls, test_now=None):
        cls._test_now = test_now

        DateTime.set_test_now(test_now)
        Date.set_test_now(test_now)
        Time.set_test_now(test_now)

    @classmethod
    def set_formatter(cls, formatter=None):
        super(Global, cls).set_formatter(formatter)

        DateTime.set_formatter(formatter)
        Date.set_formatter(formatter)
        Time.set_formatter(formatter)

    @classmethod
    def set_locale(cls, locale):
        super(Global, cls).set_locale(locale)

        DateTime.set_locale(locale)
        Date.set_locale(locale)
        Time.set_locale(locale)
