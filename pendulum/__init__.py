# -*- coding: utf-8 -*-

from .pendulum import Pendulum
from .interval import Interval

# Constants
MONDAY = Pendulum.MONDAY
TUESDAY = Pendulum.TUESDAY
WEDNESDAY = Pendulum.WEDNESDAY
THURSDAY = Pendulum.THURSDAY
FRIDAY = Pendulum.FRIDAY
SATURDAY = Pendulum.SATURDAY
SUNDAY = Pendulum.SUNDAY

YEARS_PER_CENTURY = Pendulum.YEARS_PER_CENTURY
YEARS_PER_DECADE = Pendulum.YEARS_PER_DECADE
MONTHS_PER_YEAR = Pendulum.MONTHS_PER_YEAR
WEEKS_PER_YEAR = Pendulum.WEEKS_PER_YEAR
DAYS_PER_WEEK = Pendulum.DAYS_PER_WEEK
HOURS_PER_DAY = Pendulum.HOURS_PER_DAY
MINUTES_PER_HOUR = Pendulum.MINUTES_PER_HOUR
SECONDS_PER_MINUTE = Pendulum.SECONDS_PER_MINUTE

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
set_transaltor = Pendulum.set_translator
set_to_string_format = Pendulum.set_to_string_format
reset_to_string_format = Pendulum.reset_to_string_format

# Standard helpers
min = Pendulum.min
max = Pendulum.max
fromtimestamp = Pendulum.fromtimestamp
utcfromtimestamp = Pendulum.utcfromtimestamp
fromordinal = Pendulum.fromordinal
combine = Pendulum.combine

# Interval
interval = Interval
