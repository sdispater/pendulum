Installation
============

You can install Pendulum in 2 different ways:

* The easier and more straightforward is to use pip

.. code-block:: bash

    $ pip install pendulum

* Use the official repository (https://github.com/sdispater/pendulum)


Introduction
============

Pendulum is a Python package to ease datetimes manipulation.

It is heavily inspired by `Carbon <http://carbon.nesbot.com>`_ for PHP.

The ``Pendulum`` class is a drop-in replacement for the native ``datetime``
class (it is inherited from it) with the exception that its mutable.

Unlike the native class, most of the methods modify the current instance
of ``Pendulum`` in place. If you want to modify a copy just use the ``copy()`` method.

Special care has been taken to ensure timezones are handled correctly,
and where appropriate are based on the underlying ``tzinfo`` implementation.
For example all comparisons are done in UTC or in the timezone of the datetime being used.

.. code-block:: python

    dt_toronto = Pendulum.create_from_date(2012, 1, 1, 'America/Toronto')
    dt_vancouver = Pendulum.create_from_date(2012, 1, 1, 'America/Vancouver')

    print(dt.vancouver.diff_in_hours(dt_toronto)) # 3

The default timezone, except when using the ``now()`` method will always be ``UTC``.

.. note::

    Also ``is`` comparisons (like ``is_today()``) are done in the timezone of the provided Pendulum instance.
    For example, my current timezone is -13 hours from Tokyo.
    So ``Pendulum.now('Asia/Tokyo').is_today()`` would only return ``False`` for any time past 1 PM my time.
    This doesn't make sense since ``now()`` in tokyo is always today in Tokyo.
    Thus the comparison to ``now()`` is done in the same timezone as the current instance.


.. note::

    Every class methods that will be covered in this documentation are also accessible at module
    level:

    ============================= =====================
    Class Method                  Module Function
    ============================= =====================
    ``instance()``                ``instance()``
    ``parse()``                   ``parse()``
    ``now()``                     ``now()``
    ``utcnow()``                  ``utcnow()``
    ``today()``                   ``today()``
    ``tomorrow()``                ``tomorrow()``
    ``yesterday()``               ``yesterday()``
    ``create()``                  ``create()``
    ``create_from_date()``        ``from_date()``
    ``create_from_time()``        ``from_time()``
    ``create_from_format()``      ``from_time()``
    ``strptime()``                ``strptime()``
    ``create_from_timestamp()``   ``from_timestamp()``
    ============================= =====================

Instantiation
=============

There are several different methods available to create a new instance of Pendulum.
First there is a constructor. It overrides the parent constructor to be more flexible.
Basically, unlike ``datetime`` you can omit parameters and any omitted parameter will
default to its ``now()`` value. However, if you provide the ``year``, ``month``, ``day``
it will emulate the default ``datetime`` behavior.

.. code-block:: python

    dt = Pendulum() # equivalent to Pendulum.utcnow()
    isinstance(dt, datetime)
    True

    dt = Pendulum(2015, 2, 5, tzinfo='America/Vancouver')
    dt = Pendulum.now(-5)

You'll notice above that the timezone (2nd) parameter was passed as a string and an integer
rather than a ``tzinfo`` instance. All timezone parameters have been augmented
so you can pass a ``tzinfo`` instance, string or integer offset to GMT
and the timezone will be created for you.
This is again shown in the next example which also introduces the ``now()`` function.

.. code-block:: python

    now = Pendulum.now()

    now_in_london_tz = Pendulum.now(pytz.timezone('Europe/London'))

    # or just pass the timezone as a string
    now_in_london_tz = Pendulum.now('Europe/London')
    print(now_in_london_tz.timezone_name)
    'Europe/London'

    # or to create a date with a timezone of +1 to GMT
    # during DST then just pass an integer
    print(Pendulum.now(1).timezone_name))
    None

.. note::

    You'll notice that when using an integer offset, you don't have access
    to the name of the timezone.

To accompany ``now()``, a few other static instantiation helpers exist to create widely known instances.
The only thing to really notice here is that ``today()``, ``tomorrow()`` and ``yesterday()``,
besides behaving as expected, all accept a timezone parameter and each has their time value set to ``00:00:00``.

.. code-block:: python

    now = Pendulum.now()
    print(now)
    '2016-06-28T16:51:45.978473-05:00'

    today = Pendulum.today()
    print(today)
    '2016-06-28T00:00:00-05:00'

    tomorrow = Pendulum.tomorrow('Europe/London')
    print(tomorrow)
    '2016-06-29T00:00:00+01:00'

    yesterday = Pendulum.yesterday()
    print(yesterday)
    '2016-06-27T00:00:00-05:00'

The next group of static helpers are the ``create_xxx()`` helpers.
Most of the static ``create`` functions allow you to provide
as many or as few arguments as you want and will provide default values for all others.
Generally default values are the current date, time or timezone.

.. code-block:: python

    Pendulum.create_from_date(year, month, day, tz)
    Pendulum.create_from_time(hour, minute, second, microsecond, tz)
    Pendulum.create(year, month, day, hour, minute, second, microsecond, tz)

``create_from_date()`` will default the time to now. ``create_from_time()`` will default the date to today.
``create()`` will default any null parameter to the current respective value.
As before, the ``tz`` defaults to the ``UTC`` timezone and otherwise can be a ``tzinfo`` instance
or simply a string timezone value. The only special case for default values occurs when an hour value
is specified but no minutes or seconds, they will get defaulted to ``0``.

.. code-block:: python

    xmas_this_year = Pendulum.create_from_date(None, 12, 25) # Year defaults to current year
    y2k = Pendulum.create(2000, 1, 1, 0, 0, 0)
    noon_london_tz = Pendulum.create_from_time(12, 0, 0, tz='Europe/London')

.. code-block:: python

    Pendulum.create_from_format(time, format, tz)

``create_from_format()`` is mostly a wrapper for the base Python function ``datetime.strptime()``.
The difference being the addition the ``tz`` argument that can be a ``tzinfo`` instance or a string timezone value
(defaults to ``UTC``).

.. code-block:: python

    Pendulum.create_from_format('1975-05-21 22', '%Y-%m-%d %H').to_datetime_string()
    '1975-05-21 22:00:00'
    Pendulum.create_from_format('1975-05-21 22', '%Y-%m-%d %H', 'Europe/London').isoformat()
    '1975-05-21T22:00:00+01:00'

    # Using strptime is also possible (the timezone will be UTC)
    Pendulum.strptime('1975-05-21 22', '%Y-%m-%d %H').isoformat()

The final ``create`` function is for working with unix timestamps.
``create_from_timestamp()`` will create a Pendulum instance equal to the given timestamp
and will set the timezone as well or default it to ``UTC``.

.. code-block:: python

    Pendulum.create_from_timestamp(-1).to_datetime_string()
    '1969-12-31 23:59:59'

    Pendulum.create_from_timestamp(-1, 'Europe/London').to_datetime_string()
    '1970-01-01 00:59:59'

You can also create a ``copy()`` of an existing Pendulum instance.
As expected the date, time and timezone values are all copied to the new instance.

.. code-block:: python

    dt = Pendulum.now()
    print(dt.diff_in_years(dt.copy().add_year()))
    1

    # dt was unchanged and still holds the value of Pendulum.now()

Finally, if you find yourself inheriting a ``datetime`` instance,
you can create a Pendulum instance via the ``instance()`` function.

.. code-block:: python

    dt = datetime(2008, 1, 1)
    p = Pendulum.instance(dt)
    print(p.to_datetime_string())
    '2008-01-01 00:00:00'


Localization
============

Localization occurs naturally when using the ``format()`` method since it relies on the
native ``strftime`` datetime function.

.. code-block:: python

    import locale

    dt = Pendulum(1975, 5, 21)

    locale.setlocale(locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8'))
    dt.format('%A %d %B %Y')
    'Mittwoch 21 Mai 1975'

    locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
    dt.format('%A %d %B %Y')
    'Wednesday 21 May 1975'

``diff_for_humans()`` is also localized, you can set the Pendulum locale
by using the class method ``Pendulum.set_locale()``.

.. code-block:: python

    Pendulum.set_locale('de')
    print(Pendulum.now().add_year().diff_for_humans())
    'in 1 Jahr'

    Pendulum.set_locale('en')

However, you might not want to set the locale globally. The ``diff_for_humans()``
method accept a ``locale`` keyword argument to use a locale for a specific call.

.. code-block:: python

    Pendulum.set_locale('de')
    print(Pendulum.now().add_year().diff_for_humans(locale='fr'))
    'dans 1 an'


Attributes and Properties
=========================

Pendulum gives access to more attributes and properties than the default `datetime` class.

.. code-block:: python

    dt = Pendulum.parse('2012-9-5 23:26:11.123789')

    # These properties specifically return integers
    dt.year
    2012
    dt.month
    9
    dt.day
    5
    dt.hour
    23
    dt.minute
    26
    dt.second
    11
    dt.microsecond
    123789
    dt.day_of_week
    3
    dt.day_of_year
    248
    dt.week_of_month
    1
    dt.week_of_year
    36
    dt.days_in_month
    30
    dt.timestamp
    1346887571
    dt.create_from_date(1975, 5, 21).age
    41 # calculated vs now in the same tz
    dt.quarter
    3

    dt.float_timestamp
    1346887571.123789

    # Returns an int of seconds difference from UTC (+/- sign included)
    Pendulum.create_from_timestamp(0).offset
    0
    Pendulum.create_from_timestamp(0, 'America/Toronto').offset
    -18000

    # Returns an int of hours difference from UTC (+/- sign included)
    Pendulum.create_from_timestamp(0, 'America/Toronto').offset_hours
    -5

    # Indicates if day light savings time is on
    Pendulum.create_from_date(2012, 1, 1, 'America/Toronto').is_dst
    False
    Pendulum.create_from_date(2012, 9, 1, 'America/Toronto').is_dst
    True

    # Indicates if the instance is in the same timezone as the local timezone
    Pendulum.now().local
    True
    Pendulum.now('Europe/London').local
    False

    # Indicates if the instance is in the UTC timezone
    Pendulum.now().utc
    False
    Pendulum.now('Europe/London').local
    False
    Pendulum.utcnow().utc
    True

    # Gets the timezone instance
    Pendulum.now().timezone
    Pendulum.now().tz

    # Gets the timezone name
    Pendulum.now().timezone_name


Fluent Setters
==============

Unlike the native ``datetime`` class, ``Pendulum`` instances are mutable.
However, none of the setters, with the exception of explicitely setting the
timezone, will change the timezone of the instance. Specifically,
setting the timestamp will not set the corresponding timezone to UTC.

.. code-block:: python

    dt = Pendulum.now()

    dt.year_(1975).month_(5).day_(21).hour_(22).minute_(32).second_(5).to_datetime_string()
    '1975-05-21 22:32:05'

    dt.set_date(1975, 5, 21).set_time(22, 32, 5).to_datetime_string()
    '1975-05-21 22:32:05'

    dt.timestamp_(169957925).timezone_('Europe/London')

    dt.tz_('America/Toronto').to('America/Vancouver')


String Formatting
=================

All the ``to_xxx_string()`` methods rely on the native ``datetime.strftime()`` with additional
directives available.
The ``__str__`` magic method is defined which allows Pendulum instance to be printed
as a pretty date string when used in a string context.
The default string representation is the same as the one returned by the ``isoformat()`` method.

.. code-block:: python

    dt = Pendulum(1975, 12, 25, 14, 15, 16)

    print(dt)
    '1975-12-25T14:15:16+00:00'

    dt.to_date_string()
    '1975-12-25'

    dt.to_formatted_date_string()
    'Dec 25, 1975'

    dt.to_time_string()
    '14:15:16'

    dt.to_datetime_string()
    '1975-12-25 14:15:16'

    dt.to_day_datetime_string()
    'Thu, Dec 25, 1975 2:15 PM'

    # You can also use the format() method
    dt.format('%A %-d%t of %B %Y %I:%M:%S %p')
    'Thursday 25th of December 1975 02:15:16 PM'

    # Of course, the strftime method is still available
    dt.strftime('%A %-d%t of %B %Y %I:%M:%S %p')
    'Thursday 25th of December 1975 02:15:16 PM'

You can also set the default ``__str__`` format.

.. code-block:: python

    Pendulum.set_to_string_format('%-d%t of %B, %Y %-I:%M:%S %p')

    print(dt)
    '25th of December, 1975 2:15:16 PM'

    Pendulum.reset_to_string_format()
    print(dt)
    '25th of December, 1975 2:15:16 PM'

.. note::

    For localization support see the `Localization`_ section.

Custom Directives
-----------------

Apart from the `default directives <For localization support see the Localization section.>`_,
Pendulum comes with its own:

===========  ======================================================================== =================================
Directive    Meaning                                                                  Example
===========  ======================================================================== =================================
``%P``       Difference to Greenwich time (GMT) with colon between hours and minutes  ``+02:00``
``%t``       English ordinal suffix for the day of the month, 2 characters            ``st``, ``nd``, ``rd`` or ``th``
===========  ======================================================================== =================================

Common Formats
--------------

The following are methods to display a ``Pendulum`` instance as a common format:

.. code-block:: python

    dt = Pendulum.now()

    dt.to_atom_string()
    '1975-12-25T14:15:16-05:00'

    dt.to_cookie_string()
    'Thursday, 25-Dec-1975 14:15:16 EST'

    dt.to_iso8601_string()
    '1975-12-25T14:15:16-0500'

    dt.to_rfc822_string()
    'Thu, 25 Dec 75 14:15:16 -0500'

    dt.to_rfc850_string()
    'Thursday, 25-Dec-75 14:15:16 EST'

    dt.to_rfc1036_string()
    'Thu, 25 Dec 75 14:15:16 -0500'

    dt.to_rfc1123_string()
    'Thu, 25 Dec 1975 14:15:16 -0500'

    dt.to_rfc2822_string()
    'Thu, 25 Dec 1975 14:15:16 -0500'

    dt.to_rfc3339_string()
    '1975-12-25T14:15:16-05:00'

    dt.to_rss_string()
    'Thu, 25 Dec 1975 14:15:16 -0500'

    dt.to_w3c_string()
    '1975-12-25T14:15:16-05:00'


Comparison
==========

Simple comparison is offered up via the following functions or the basic operators.
Remember that the comparison is done in the UTC timezone so things aren't always as they seem.

.. code-block:: python

    first = Pendulum.create(2012, 9, 5, 23, 26, 11, 0, tz='America/Toronto')
    second = Pendulum.create(2012, 9, 5, 20, 26, 11, 0, tz='America/Vancouver')

    first.to_datetime_string()
    '2012-09-05 23:26:11'
    first.timezone_name
    'America/Toronto'
    second.to_datetime_string()
    '2012-09-05 20:26:11'
    second.timezone_name
    'America/Vancouver'

    first.eq(second) # ==
    True
    first.ne(second) # !=
    False
    first.gt(second) # >
    False
    first.gte(second) # >=
    True
    first.lt(second) # <
    False
    first.lte(second) # <=
    True

    first.set_date_time(2012, 1, 1, 0, 0, 0)
    second.set_date_time(2012, 1, 1, 0, 0, 0) # tz is still America/Vancouver

    first.eq(second)
    False
    first.ne(second)
    True
    first.gt(second)
    False
    first.gte(second)
    False
    first.lt(second)
    True
    first.lte(second)
    True

To determine if the current instance is between two other instances you can use the ``between()`` method.
The third parameter indicates if an equal to comparison should be done.
The default is ``True`` which determines if its between or equal to the boundaries.

.. code-block:: python

    first = Pendulum.create(2012, 9, 5, 1)
    second = Pendulum.create(2012, 9, 5, 5)

    Pendulum.create(2012, 9, 5, 3).between(first, second)
    True
    Pendulum.create(2012, 9, 5, 3).between(first, second)
    True
    Pendulum.create(2012, 9, 5, 5).between(first, second, False)
    False

There are also the ``min_()`` and ``max_()`` methods.
As usual the default parameter is ``now`` if ``None`` is specified.

.. code-block:: python

    dt1 =  Pendulum.create(2012, 1, 1, 0, 0, 0, 0)
    dt2 =  Pendulum.create(2014, 1, 30, 0, 0, 0, 0)

    print(dt1.min_(dt2))
    '2012-01-01T00:00:00+00:00'

    print(dt1.max_(dt2))
    '2014-01-30T00:00:00+00:00'

    # now is the default param
    print(dt1.max_())
    '2016-06-30T19:09:03.757597+00:00'

.. note::

    ``min_()`` and ``max_()`` methods are named with an underscore
    to not override the default ``min`` and ``max`` attributes of
    ``datetime`` objects.

To handle the most used cases there are some simple helper functions.
For the methods that compare to ``now()`` (ex. ``is_today()``) in some manner
the ``now()`` is created in the same timezone as the instance.

.. code-block:: python

    dt = Pendulum.now()

    dt.is_weekday()
    dt.is_weekend()
    dt.is_yesterday()
    dt.is_today()
    dt.is_tomorrow()
    dt.is_future()
    dt.is_past()
    dt.is_leap_year()
    dt.is_same_day(Pendulum.now())

    born = Pendulum.create_from_date(1987, 4, 23)
    not_birthday = Pendulum.create_from_date(2014, 9, 26)
    birthday = Pendulum.create_from_date(2014, 2, 23)
    past_birthday = Pendulum.now().sub_years(50)

    born.is_birthday(not_birthday)
    False
    born.is_birthday(birthday)
    True
    past_birthday.is_birthday()
    # Compares to now by default
    True


Addition and Substraction
=========================

To easily adding and substracting time, you can use the ``add_xxx()``/``sub_xxx()``
methods or the more generic ones ``add()``/``sub()``.

.. code-block:: python

    dt = Pendulum.create(2012, 1, 31, 0)

    dt.to_datetime_string()
    '2012-01-31 00:00:00'

    dt.add_years(5)
    '2017-01-31 00:00:00'
    dt.add_year()
    '2018-01-31 00:00:00'
    dt.sub_year()
    '2017-01-31 00:00:00'
    dt.sub_years(5)
    '2012-01-31 00:00:00'

    dt.add_months(60)
    '2017-01-31 00:00:00'
    dt.add_month()
    '2017-02-28 00:00:00'
    dt.sub_month()
    '2017-01-28 00:00:00'
    dt.sub_months(60)
    '2012-01-28 00:00:00'

    dt.add_days(29)
    '2012-02-26 00:00:00'
    dt.add_day()
    '2012-02-27 00:00:00'
    dt.sub_day()
    '2012-02-26 00:00:00'
    dt.sub_days(29)
    '2012-01-28 00:00:00'

    dt.add_weeks(3)
    '2012-02-18 00:00:00'
    dt.add_week()
    '2012-02-25 00:00:00'
    dt.sub_week()
    '2012-02-18 00:00:00'
    dt.sub_weeks(3)
    '2012-01-28 00:00:00'

    dt.add_hours(24)
    '2012-01-29 00:00:00'
    dt.add_hour()
    '2012-02-25 01:00:00'
    dt.sub_hour()
    '2012-02-29 00:00:00'
    dt.sub_hours(24)
    '2012-01-28 00:00:00'

    dt.add_minutes(61)
    '2012-01-28 01:01:00'
    dt.add_minute()
    '2012-01-28 01:02:00'
    dt.sub_minute()
    '2012-01-28 01:01:00'
    dt.sub_minutes(24)
    '2012-01-28 00:00:00'

    dt.add_seconds(61)
    '2012-01-28 00:01:01'
    dt.add_second()
    '2012-01-28 00:01:02'
    dt.sub_second()
    '2012-01-28 00:01:01'
    dt.sub_seconds(61)
    '2012-01-28 00:00:00'

    dt.add(years=3, months=2, days=6, hours=12, minutes=31, seconds=43)
    '2015-04-03 12:31:43'
    dt.sub(years=3, months=2, days=6, hours=12, minutes=31, seconds=43)
    '2012-01-28 00:00:00'

    # You can also add or remove a timedelta
    dt.add_timedelta(timedelta(hours=3, minutes=4, seconds=5))
    '2012-01-28 03:04:05'
    dt.sub_timedelta(timedelta(hours=3, minutes=4, seconds=5))
    '2012-01-28 00:00:00'


Difference
==========

These functions always return *the total difference expressed* in the specified time requested.
All values are truncated and not rounded.
Each function below has a default first parameter which is the Pendulum instance to compare to,
or ``None`` if you want to use ``now()``.
The 2nd parameter is optional and indicates if you want the return value to be the absolute value
or a relative value that might have a ``-`` (negative) sign if the passed in date
is less than the current instance.
This will default to ``True``, return the absolute value. The comparisons are done in UTC.

.. code-block:: python

    dt_ottawa = Pendulum.create_from_date(2000, 1, 1, 'America/Toronto')
    dt_vancouver = Pendulum.create_from_date(200, 1, 1, 'America/Vancouver')

    dt_ottawa.diff_in_hours(dt_vancouver)
    3
    dt_ottawa.diff_in_hours(dt_vancouver, False)
    3
    dt_vancouver.diff_in_hours(dt_ottawa, False)
    -3

    dt = Pendulum.create(2012, 1, 31, 0)
    dt.diff_in_days(dt.copy().add_month())
    29
    dt.diff_in_days(dt.copy().sub_month(), False)
    -31

    dt = Pendulum.create(2012, 4, 30, 0)
    dt.diff_in_days(dt.copy().add_month())
    30
    dt.diff_in_days(dt.copy().add_week())
    7

    dt = Pendulum.create(2012, 1, 1, 0)
    dt.diff_in_minutes(dt.copy().add_seconds(59))
    0
    dt.diff_in_minutes(dt.copy().add_seconds(60))
    1
    dt.diff_in_minutes(dt.copy().add_seconds(119))
    1
    dt.diff_in_minutes(dt.copy().add_seconds(120))
    2

    dt.add_seconds(120).seconds_since_midnight()
    120

Difference for Humans
---------------------

The ``diff_for_humans()`` method will add a phrase after the difference value relative
to the instance and the passed in instance. There are 4 possibilities:

* When comparing a value in the past to default now:
    * 1 hour ago
    * 5 months ago

* When comparing a value in the future to default now:
    * 1 hour from now
    * 5 months from now

* When comparing a value in the past to another value:
    * 1 hour before
    * 5 months before

* When comparing a value in the future to another value:
    * 1 hour after
    * 5 months after

You may also pass ``True`` as a 2nd parameter to remove the modifiers `ago`, `from now`, etc.

.. code-block:: python

    # The most typical usage is for comments
    # The instance is the date the comment was created
    # and its being compared to default now()
    Pendulum.now().sub_days().diff_for_humans()
    '5 days ago'

    Pendulum.now().diff_for_humans(Pendulum.now().sub_year())
    '1 year after'

    dt = Pendulum.create_from_date(2011, 8, 1)
    dt.diff_for_humans(dt.copy.add_month())
    '1 month before'
    dt.diff_for_humans(dt.copy.sub_month())
    '1 month after'

    Pendulum.now().add_seconds(5).diff_for_humans()
    '5 seconds from now'

    Pendulum.now().sub_days(24).diff_for_humans()
    '3 weeks ago'

    Pendulum.now().sub_days(24).diff_for_humans(absolute=True)
    '3 weeks'

You can also change the locale of the string either globally by using ``Pendulum.set_locale('fr')``
before the ``diff_for_humans()`` call or specifically for the call by passing the ``locale`` keyword
argument. See the `Localization`_ section for more detail.

.. code-block:: python

    Pendulum.set_locale('de')
    Pendulum.now().add_year().diff_for_humans()
    'in 1 Jahr'
    Pendulum.now().add_year().diff_for_humans(locale='fr')
    'dans 1 an'


Modifiers
=========

These group of methods perform helpful modifications to the current instance.
You'll notice that the ``start_of_xxx()``, ``next()`` and ``previous()`` methods
set the time to ``00:00:00`` and the ``end_of_xxx()`` methods set the time to ``23:59:59``.

The only one slightly different is the ``average()`` method.
It moves your instance to the middle date between itself and the provided Pendulum argument.

.. code-block:: python

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of_day()
    '2012-01-31 00:00:00'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of_day()
    '2012-01-31 23:59:59'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of_month()
    '2012-01-01 00:00:00'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of_month()
    '2012-01-31 23:59:59'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of_year()
    '2012-01-01 00:00:00'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of_year()
    '2012-01-31 23:59:59'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of_decade()
    '2010-01-01 00:00:00'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of_decade()
    '2019-01-31 23:59:59'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of_century()
    '2000-01-01 00:00:00'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of_century()
    '2099-12-31 23:59:59'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of_week()
    '2012-01-30 00:00:00'
    dt.day_of_week == Pendulum.MONDAY
    True # ISO8601 week starts on Monday

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of_week()
    '2012-02-05 23:59:59'
    dt.day_of_week == Pendulum.SUNDAY
    True # ISO8601 week ends on SUNDAY

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of_week()
    '2012-02-05 23:59:59'
    dt.day_of_week == Pendulum.SUNDAY
    True # ISO8601 week ends on SUNDAY

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.next(Pendulum.WEDNESDAY)
    '2012-02-01 00:00:00'
    dt.day_of_week == Pendulum.WEDNESDAY
    True

    dt = Pendulum.create(2012, 1, 1, 12, 0, 0)
    dt.next()
    '2012-01-08 00:00:00'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.previous(Pendulum.WEDNESDAY)
    '2012-01-25 00:00:00'
    dt.day_of_week == Pendulum.WEDNESDAY
    True

    dt = Pendulum.create(2012, 1, 1, 12, 0, 0)
    dt.previous()
    '2011-12-25 00:00:00'

    start = Pendulum.create(2014, 1, 1, 0, 0, 0)
    end = Pendulum.create(2014, 1, 30, 0, 0, 0)
    start.average(end)
    '2014-01-15 12:00:00'

    # others that are defined that are similar
    # first_of_month(), last_of_month(), nth_of_month()
    # first_of_quarter(), last_of_quarter(), nth_of_quarter()
    # first_of_year(), last_of_year(), nth_of_year()


Constants
=========

The following constants are defined in the Pendulum class and at module
level.

.. code-block:: python

    SUNDAY
    0
    MONDAY
    1
    TUESDAY
    2
    WEDNESDAY
    3
    THURSDAY
    4
    FRIDAY
    5
    SATURDAY
    6

    YEARS_PER_CENTURY
    100
    YEARS_PER_DECADE
    10
    MONTHS_PER_YEAR
    12
    WEEKS_PER_YEAR
    52
    DAYS_PER_WEEK
    7
    HOURS_PER_DAY
    24
    MINUTES_PER_HOUR
    60
    SECONDS_PER_MINUTE
    60


PendulumInterval
================

When you subtract a ``Pendulum`` instance to another, it will return a ``PendulumInterval`` instance.
The ``PendulumInterval`` class is inherited from the native ``timedelta`` class.
It has many improvements over the base class.

.. note::

    Even though, it inherits from the ``timedelta`` class, its behavior is slightly different.
    The more important to notice is that the native normalization does not happen, this is so that
    it feels more intuituve.

    .. code-block:: python

        d1 = datetime(2012, 1, 1, 1, 2, 3, tzinfo=pytz.UTC)
        d2 = datetime(2011, 12, 31, 22, 2, 3, tzinfo=pytz.UTC)
        delta = d2 - d1
        delta.days
        -1
        delta.seconds
        75600

        d1 = Pendulum(2012, 1, 1, 1, 2, 3)
        d2 = Pendulum(2011, 12, 31, 22, 2, 3)
        delta = d2 - d1
        delta.days
        0
        delta.hours
        -3

Instantiation
-------------

You can create an instance in the following ways:

.. code-block:: python

    it = PendulumInterval(days=1177, seconds=7284, microseconds=1234)
    it = pendulum.interval(days=1177, seconds=7284, microseconds=1234)

    # You can use an existing timedelta instance
    delta = timedelta(days=1177, seconds=7284, microseconds=1234)
    it = PendulumInterval.instance(delta)

Properties and Duration Methods
-------------------------------

The ``PendulumInterval`` class brings more properties than the default ``days``, ``seconds`` and
``microseconds``.

.. code-block:: python

    it = PendulumInterval(days=1177, seconds=7284, microseconds=1234)

    # Both weeks and days are based on the total of days
    it.weeks
    168
    it.days
    1117

    # If you want the remaining days not included in full weeks
    it.days_exclude_weeks
    1

    # The remaining number in each unit
    it.hours
    2
    it.minutes
    1
    it.seconds
    24
    it.microseconds
    1234

If you want to get the total duration of the interval in each supported unit
you can use the appropriate methods.

.. code-block:: python

    # Each method returns a float like the native
    # total_seconds() method
    it.total_weeks()
    168.15490079569113

    it.total_days()
    1177.0843055698379

    it.total_hours()
    28250.02333367611

    it.total_minutes()
    1695001.4000205665

    it.total_seconds()
    101700084.001234

It also has a handy ``for_humans()``, which determines the interval representation when printed,
that prints the interval for humans.

.. code-block:: python

    PendulumInterval.set_locale('fr')
    # or pendulum.interval.set_locale('fr')

    it = PendulumInterval(days=1177, seconds=7284, microseconds=1234)

    it.for_humans()
    '168 semaines 1 jour 2 heures 1 minute 24 secondes'

    print(it)
    '168 semaines 1 jour 2 heures 1 minute 24 secondes'

    it.for_humans(locale='de')
    '168 Wochen 1 Tag 2 Stunden 1 Minute 24 Sekunden'
