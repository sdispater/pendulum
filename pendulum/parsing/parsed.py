class Parsed:
    """
    Parsed object
    """

    def __init__(self):
        self.is_date = False
        self.is_time = False
        self.is_datetime = False
        self.is_duration = False
        self.is_period = False

        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.microsecond = 0
        self.offset = None

        self.years = 0
        self.months = 0
        self.weeks = 0
        self.days = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.microseconds = 0

    def is_valid(self):
        return (
            self.is_date
            or self.is_time
            or self.is_datetime
            or self.is_duration
            or self.is_period
        )

    def from_date(self, date):
        self.year = date.year
        self.month = date.month
        self.day = date.day

        self.is_date = True
        self.is_time = False
        self.is_datetime = False

        return self

    def from_time(self, time):
        self.hour = time.hour
        self.minute = time.minute
        self.second = time.second
        self.microsecond = time.microsecond

        self.is_date = False
        self.is_time = True
        self.is_datetime = False

        return self

    def from_datetime(self, datetime):
        self.year = datetime.year
        self.month = datetime.month
        self.day = datetime.day

        self.hour = datetime.hour
        self.minute = datetime.minute
        self.second = datetime.second
        self.microsecond = datetime.microsecond

        if datetime.tzinfo is not None:
            self.offset = getattr(
                datetime.tzinfo,
                'offset',
                datetime.utcoffset().total_seconds()
            )

        self.is_date = False
        self.is_time = False
        self.is_datetime = True

        return self
