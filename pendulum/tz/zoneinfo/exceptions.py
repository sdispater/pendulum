class ZoneinfoError(Exception):

    pass


class InvalidZoneinfoFile(ZoneinfoError):

    pass


class InvalidTimezone(ZoneinfoError):

    def __init__(self, name):
        super().__init__(
            'Invalid timezone "{}"'.format(name)
        )
