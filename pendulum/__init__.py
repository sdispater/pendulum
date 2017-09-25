# -*- coding: utf-8 -*-

# Types
from .pendulum import Pendulum
from .date import Date
from .time import Time
from .interval import Interval
from .period import Period

# Mimicking standard library
datetime = Pendulum
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

from .mixins.default import TranslatableMixin, FormattableMixing, TestableMixin

from ._global import Global

PRE_TRANSITION = Timezone.PRE_TRANSITION
POST_TRANSITION = Timezone.POST_TRANSITION
TRANSITION_ERROR = Timezone.TRANSITION_ERROR

# Global helpers
test = Global.test
set_test_now = Global.set_test_now
has_test_now = Global.has_test_now
get_test_now = Global.get_test_now
set_locale = Global.set_locale
get_locale = Global.get_locale
translator = Global.translator
set_translator = Global.set_translator
set_formatter = Global.set_formatter
get_formatter = Global.get_formatter

# Helpers
from .parser import parse

instance = Pendulum.instance
now = Pendulum.now
utcnow = Pendulum.utcnow
today = Pendulum.today
tomorrow = Pendulum.tomorrow
yesterday = Pendulum.yesterday
create = Pendulum.create
from_format = Pendulum.create_from_format
strptime = Pendulum.strptime
from_timestamp = Pendulum.create_from_timestamp
set_to_string_format = Pendulum.set_to_string_format
reset_to_string_format = Pendulum.reset_to_string_format
set_transition_rule = Pendulum.set_transition_rule
get_transition_rule = Pendulum.get_transition_rule

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
from .tz import timezone, timezones, local_timezone, UTC
