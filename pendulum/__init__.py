# Types
from .datetime import DateTime
from .date import Date
from .time import Time
from .duration import Duration
from .period import Period

# Mimicking standard library
datetime = DateTime
date = Date
time = Time

# Constants
from .constants import (
    MONDAY, TUESDAY, WEDNESDAY,
    THURSDAY, FRIDAY, SATURDAY, SUNDAY,
    YEARS_PER_CENTURY, YEARS_PER_DECADE,
    MONTHS_PER_YEAR, WEEKS_PER_YEAR, DAYS_PER_WEEK,
    HOURS_PER_DAY, MINUTES_PER_HOUR, SECONDS_PER_MINUTE,
    SECONDS_PER_HOUR, SECONDS_PER_DAY
)

from .tz.timezone import Timezone

PRE_TRANSITION = Timezone.PRE_TRANSITION
POST_TRANSITION = Timezone.POST_TRANSITION
TRANSITION_ERROR = Timezone.TRANSITION_ERROR

# Global helpers
from .translator import Translator
from .formatting import FORMATTERS

_TEST_NOW = None
_LOCALE = 'en'
_DEFAULT_FORMATTER = FORMATTERS['classic']
_FORMATTER = _DEFAULT_FORMATTER
_TRANSLATOR = Translator(_LOCALE)

from .helpers import (
    test, set_test_now, has_test_now, get_test_now,
    set_locale, get_locale, translator,
    set_formatter, get_formatter
)

# Helpers
from .parser import parse

instance = DateTime.instance
now = DateTime.now
utcnow = DateTime.utcnow
today = DateTime.today
tomorrow = DateTime.tomorrow
yesterday = DateTime.yesterday
create = DateTime.create
from_format = DateTime.create_from_format
strptime = DateTime.strptime
from_timestamp = DateTime.create_from_timestamp
set_to_string_format = DateTime.set_to_string_format
reset_to_string_format = DateTime.reset_to_string_format
set_transition_rule = DateTime.set_transition_rule
get_transition_rule = DateTime.get_transition_rule

# Standard helpers
min = DateTime.min
max = DateTime.max
fromtimestamp = DateTime.fromtimestamp
utcfromtimestamp = DateTime.utcfromtimestamp
fromordinal = DateTime.fromordinal
combine = DateTime.combine

# Duration
duration = Duration

# Period
period = Period

# Timezones
from .tz import (
    timezone,
    local_timezone, test_local_timezone, set_local_timezone,
    UTC
)
