# -*- coding: utf-8 -*-

from .pendulum import Pendulum
from .interval import Interval
from .period import Period

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

# Helpers
instance = Pendulum.instance
parse = Pendulum.parse
now = Pendulum.now
utcnow = Pendulum.utcnow
today = Pendulum.today
tomorrow = Pendulum.tomorrow
yesterday = Pendulum.yesterday
create = Pendulum.create
from_date = Pendulum.create_from_date
from_time = Pendulum.create_from_time
from_format = Pendulum.create_from_format
strptime = Pendulum.strptime
from_timestamp = Pendulum.create_from_timestamp
test = Pendulum.test
set_test_now = Pendulum.set_test_now
has_test_now = Pendulum.has_test_now
get_test_now = Pendulum.get_test_now
set_locale = Pendulum.set_locale
get_locale = Pendulum.get_locale
translator = Pendulum.translator
set_translator = Pendulum.set_translator
set_to_string_format = Pendulum.set_to_string_format
reset_to_string_format = Pendulum.reset_to_string_format
set_transition_rule = Pendulum.set_transition_rule
get_transition_rule = Pendulum.get_transition_rule
set_formatter = Pendulum.set_formatter
get_formatter = Pendulum.get_formatter

# Standard helpers
min = Pendulum.min
max = Pendulum.max
fromtimestamp = Pendulum.fromtimestamp
utcfromtimestamp = Pendulum.utcfromtimestamp
fromordinal = Pendulum.fromordinal
combine = Pendulum.combine

# Interval
interval = Interval

# Period
period = Period

# Timezones
from .tz import timezone, local_timezone, UTC
