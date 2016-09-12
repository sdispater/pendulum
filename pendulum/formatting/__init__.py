# -*- coding: utf-8 -*-

from .classic_formatter import ClassicFormatter
from .alternative_formatter import AlternativeFormatter


FORMATTERS = {
    'classic': ClassicFormatter(),
    'alternative': AlternativeFormatter(),
}
