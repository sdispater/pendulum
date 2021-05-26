from ..formatting import Formatter


_formatter = Formatter()


class FormattableMixin(object):

    _formatter = _formatter

    def format(self, fmt, locale=None):  # type: (str, Optional[str]) -> str
        """
        Formats the instance using the given format.
        """
        return self._formatter.format(self, fmt, locale)

    def for_json(self):  # type: () -> str
        """
        Methods for automatic json serialization by simplejson
        """
        return str(self)

    def __format__(self, format_spec):
        if len(format_spec) > 0:
            if "%" in format_spec:
                return self.strftime(format_spec)

            return self.format(format_spec)

        return str(self)

    def __str__(self):
        return self.isoformat()
