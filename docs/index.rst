Installation
============

You can install Pendulum in 2 different ways:

* The easier and more straightforward is to use pip

.. code-block:: bash

    $ pip install pendulum

* Use the official repository (https://github.com/sdispater/pendulum)


Introduction
============

.. warning::

    Pendulum is still in development, so expect (not to many I hope) breaking API changes in
    the future.

Pendulum is a Python package to ease datetimes manipulation.

It is heavily inspired by `Carbon <http://carbon.nesbot.com>`_ for PHP.

The ``Pendulum`` class is a drop-in replacement for the native ``datetime``
class (it is inherited from it).

Special care has been taken to ensure timezones are handled correctly,
and where appropriate are based on the underlying ``tzinfo`` implementation.
For example all comparisons are done in UTC or in the timezone of the datetime being used.

.. code-block:: python

    import pendulum

    dt_toronto = pendulum.from_date(2012, 1, 1, 'America/Toronto')
    dt_vancouver = pendulum.from_date(2012, 1, 1, 'America/Vancouver')

    print(dt_vancouver.diff(dt_toronto).in_hours())
    3

The default timezone, except when using the ``now()``, method will always be ``UTC``.

.. note::

    Also ``is`` comparisons (like ``is_today()``) are done in the timezone of the provided Pendulum instance.

    For example, my current timezone is -13 hours from Tokyo.
    So ``pendulum.now('Asia/Tokyo').is_today()`` would only return ``False`` for any time past 1 PM my time.
    This doesn't make sense since ``now()`` in tokyo is always today in Tokyo.

    Thus the comparison to ``now()`` is done in the same timezone as the current instance.


.. note::

    Every class methods that will be covered in this documentation are also accessible at module
    level and vice-versa with the following correspondences:

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
First there is a constructor. It accepts the same parameters as the standard class.

.. code-block:: python

    from pendulum import Pendulum

    dt = Pendulum(2015, 2, 5, tzinfo='America/Vancouver')
    isinstance(dt, datetime)
    True

    dt = Pendulum.now(-5)

You'll notice above that the timezone (2nd) parameter was passed as a string and an integer
rather than a ``tzinfo`` instance. All timezone parameters have been augmented
so you can pass a ``tzinfo`` instance, string or integer offset to GMT
and the timezone will be created for you.
This is again shown in the next example which also introduces the ``now()`` function.

.. code-block:: python

    import pendulum

    now = pendulum.now()

    now_in_london_tz = pendulum.now(pytz.timezone('Europe/London'))

    # or just pass the timezone as a string
    now_in_london_tz = pendulum.now('Europe/London')
    print(now_in_london_tz.timezone_name)
    'Europe/London'

    # or to create a date with a timezone of +1 to GMT
    # during DST then just pass an integer
    print(pendulum.now(1).timezone_name))
    None

.. note::

    You'll notice that when using an integer offset, you don't have access
    to the name of the timezone.

To accompany ``now()``, a few other static instantiation helpers exist to create widely known instances.
The only thing to really notice here is that ``today()``, ``tomorrow()`` and ``yesterday()``,
besides behaving as expected, all accept a timezone parameter and each has their time value set to ``00:00:00``.

.. code-block:: python

    now = pendulum.now()
    print(now)
    '2016-06-28T16:51:45.978473-05:00'

    today = pendulum.today()
    print(today)
    '2016-06-28T00:00:00-05:00'

    tomorrow = pendulum.tomorrow('Europe/London')
    print(tomorrow)
    '2016-06-29T00:00:00+01:00'

    yesterday = pendulum.yesterday()
    print(yesterday)
    '2016-06-27T00:00:00-05:00'

The next group of static helpers are the ``from_xxx()`` and ``create()`` helpers.
Most of the static ``create`` functions allow you to provide
as many or as few arguments as you want and will provide default values for all others.
Generally default values are the current date, time or timezone.

.. code-block:: python

    pendulum.from_date(year, month, day, tz)
    pendulum.from_time(hour, minute, second, microsecond, tz)
    pendulum.create(year, month, day, hour, minute, second, microsecond, tz)

``from_date()`` will default the time to now. ``from_time()`` will default the date to today.
``create()`` will default any null parameter to the current respective value.
As before, the ``tz`` defaults to the ``UTC`` timezone and otherwise can be a ``tzinfo`` instance
or simply a string timezone value. The only special case for default values occurs when an hour value
is specified but no minutes or seconds, they will get defaulted to ``0``.

.. code-block:: python

    xmas_this_year = pendulum.from_date(None, 12, 25)
    # Year defaults to current year
    y2k = pendulum.create(2000, 1, 1, 0, 0, 0)
    noon_london_tz = pendulum.from_time(12, 0, 0, tz='Europe/London')

.. code-block:: python

    pendulum.from_format(time, format, tz)

``from_format()`` is mostly a wrapper for the base Python function ``datetime.strptime()``.
The difference being the addition the ``tz`` argument that can be a ``tzinfo`` instance or a string timezone value
(defaults to ``UTC``).

.. code-block:: python

    pendulum.from_format('1975-05-21 22', '%Y-%m-%d %H').to_datetime_string()
    '1975-05-21 22:00:00'
    pendulum.from_format('1975-05-21 22', '%Y-%m-%d %H', 'Europe/London').isoformat()
    '1975-05-21T22:00:00+01:00'

    # Using strptime is also possible (the timezone will be UTC)
    pendulum.strptime('1975-05-21 22', '%Y-%m-%d %H').isoformat()

The final ``create`` function is for working with unix timestamps.
``from_timestamp()`` will create a ``Pendulum`` instance equal to the given timestamp
and will set the timezone as well or default it to ``UTC``.

.. code-block:: python

    pendulum.from_timestamp(-1).to_datetime_string()
    '1969-12-31 23:59:59'

    pendulum.from_timestamp(-1, 'Europe/London').to_datetime_string()
    '1970-01-01 00:59:59'

    # Using the standard fromtimestamp is also possible
    pendulum.fromtimestamp(-1).to_datetime_string()
    '1969-12-31 23:59:59'

You can also create a ``copy()`` of an existing ``Pendulum`` instance.
As expected the date, time and timezone values are all copied to the new instance.

.. code-block:: python

    dt = pendulum.now()
    print(dt.diff(dt.copy().add(years=1)).in_years())
    1

    # dt was unchanged and still holds the value of pendulum.now()

Finally, if you find yourself inheriting a ``datetime`` instance,
you can create a ``Pendulum`` instance via the ``instance()`` function.

.. code-block:: python

    dt = datetime(2008, 1, 1)
    p = pendulum.instance(dt)
    print(p.to_datetime_string())
    '2008-01-01 00:00:00'


Localization
============

Localization occurs when using the ``format()`` method which accepts a ``locale`` keyword.

.. code-block:: python

    from pendulum import Pendulum

    dt = Pendulum(1975, 5, 21)

    dt.format('%A %d %B %Y', locale='de')
    'Mittwoch 21 Mai 1975'

    dt.format('%A %d %B %Y')
    'Wednesday 21 May 1975'

.. note::

    You can also use the ``strftime()`` method, which behaves exactly like the native one.

    .. code-block:: python

        import locale
        from pendulum import Pendulum

        dt = Pendulum(1975, 5, 21)

        locale.setlocale(locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8'))
        dt.format('%A %d %B %Y')
        'Mittwoch 21 Mai 1975'

        locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
        dt.format('%A %d %B %Y')
        'Wednesday 21 May 1975'

``diff_for_humans()`` is also localized, you can set the Pendulum locale
by using the class method ``pendulum.set_locale()``.

.. code-block:: python

    import pendulum

    pendulum.set_locale('de')
    print(pendulum.now().add(years=1).diff_for_humans())
    'in 1 Jahr'

    pendulum.set_locale('en')

However, you might not want to set the locale globally. The ``diff_for_humans()``
method accept a ``locale`` keyword argument to use a locale for a specific call.

.. code-block:: python

    pendulum.set_locale('de')
    print(pendulum.now().add(years=1).diff_for_humans(locale='fr'))
    'dans 1 an'


Attributes and Properties
=========================

Pendulum gives access to more attributes and properties than the default `datetime` class.

.. code-block:: python

    import pendulum

    dt = pendulum.parse('2012-9-5 23:26:11.123789')

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
    pendulum.from_date(1975, 5, 21).age
    41 # calculated vs now in the same tz
    dt.quarter
    3

    dt.float_timestamp
    1346887571.123789

    # Returns an int of seconds difference from UTC (+/- sign included)
    pendulum.from_timestamp(0).offset
    0
    pendulum.from_timestamp(0, 'America/Toronto').offset
    -18000

    # Returns an int of hours difference from UTC (+/- sign included)
    pendulum.from_timestamp(0, 'America/Toronto').offset_hours
    -5

    # Indicates if day light savings time is on
    pendulum.from_date(2012, 1, 1, 'America/Toronto').is_dst
    False
    pendulum.from_date(2012, 9, 1, 'America/Toronto').is_dst
    True

    # Indicates if the instance is in the same timezone as the local timezone
    pendulum.now().local
    True
    pendulum.now('Europe/London').local
    False

    # Indicates if the instance is in the UTC timezone
    pendulum.now().utc
    False
    pendulum.now('Europe/London').local
    False
    pendulum.utcnow().utc
    True

    # Gets the timezone instance
    pendulum.now().timezone
    pendulum.now().tz

    # Gets the timezone name
    pendulum.now().timezone_name


Fluent Helpers
==============

Pendulum provides helpers that returns a new instance with some attributes
modified compared to the original instance.
However, none of these helpers, with the exception of explicitely setting the
timezone, will change the timezone of the instance. Specifically,
setting the timestamp will not set the corresponding timezone to UTC.

.. code-block:: python

    import pendulum

    dt = pendulum.now()

    dt.year_(1975).month_(5).day_(21).hour_(22).minute_(32).second_(5).to_datetime_string()
    '1975-05-21 22:32:05'

    dt.with_date(1975, 5, 21).with_time(22, 32, 5).to_datetime_string()
    '1975-05-21 22:32:05'

    dt.timestamp_(169957925).timezone_('Europe/London')

    dt.tz_('America/Toronto').in_timezone('America/Vancouver')

.. note::

    ``timezone_()`` and ``tz_()`` just modify the timezone information without
    making any conversion while ``in_timezone()`` converts the time in the
    appropriate timezone.


String Formatting
=================

All the ``to_xxx_string()`` methods rely on the native ``datetime.strftime()`` with additional
directives available.
The ``__str__`` magic method is defined which allows ``Pendulum`` instances to be printed
as a pretty date string when used in a string context.
The default string representation is the same as the one returned by the ``isoformat()`` method.

.. code-block:: python

    from pendulum import Pendulum

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

    import pendulum

    pendulum.set_to_string_format('%-d%t of %B, %Y %-I:%M:%S %p')

    print(dt)
    '25th of December, 1975 2:15:16 PM'

    pendulum.reset_to_string_format()
    print(dt)
    '25th of December, 1975 2:15:16 PM'

.. note::

    For localization support see the `Localization`_ section.

Custom Directives
-----------------

Apart from the `default directives <https://docs.python.org/3.5/library/time.html#time.strftime>`_,
Pendulum comes with its own (each custom directive is in the form ``%_{directive}``):

===========  ======================================================================== =================================
Directive    Meaning                                                                  Example
===========  ======================================================================== =================================
``%_z``      Difference to Greenwich time (GMT) with colon between hours and minutes  ``+02:00``
``%_t``      Ordinal suffix for the day of the month, 2 characters                    ``st``, ``nd``, ``rd`` or ``th``
===========  ======================================================================== =================================

Common Formats
--------------

The following are methods to display a ``Pendulum`` instance as a common format:

.. code-block:: python

    import pendulum

    dt = pendulum.now()

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

Simple comparison is offered up via the basic operators.
Remember that the comparison is done in the UTC timezone so things aren't always as they seem.

.. code-block:: python

    import pendulum

    first = pendulum.create(2012, 9, 5, 23, 26, 11, 0, tz='America/Toronto')
    second = pendulum.create(2012, 9, 5, 20, 26, 11, 0, tz='America/Vancouver')

    first.to_datetime_string()
    '2012-09-05 23:26:11'
    first.timezone_name
    'America/Toronto'
    second.to_datetime_string()
    '2012-09-05 20:26:11'
    second.timezone_name
    'America/Vancouver'

    first == second
    True
    first != second
    False
    first > second
    False
    first >= second
    True
    first < second
    False
    first <= second
    True

    first = first.with_date_time(2012, 1, 1, 0, 0, 0)
    second = second.with_date_time(2012, 1, 1, 0, 0, 0)
    # tz is still America/Vancouver for second

    first == second
    False
    first != second
    True
    first > second
    False
    first >= second
    False
    first < second
    True
    first <= second
    True

To determine if the current instance is between two other instances you can use the ``between()`` method.
The third parameter indicates if an equal to comparison should be done.
The default is ``True`` which determines if its between or equal to the boundaries.

.. code-block:: python

    import pendulum

    first = pendulum.create(2012, 9, 5, 1)
    second = pendulum.create(2012, 9, 5, 5)

    pendulum.create(2012, 9, 5, 3).between(first, second)
    True
    pendulum.create(2012, 9, 5, 3).between(first, second)
    True
    pendulum.create(2012, 9, 5, 5).between(first, second, False)
    False

There are also the ``min_()`` and ``max_()`` methods.
As usual the default parameter is ``now`` if ``None`` is specified.

.. code-block:: python

    import pendulum

    dt1 =  pendulum.create(2012, 1, 1, 0, 0, 0, 0)
    dt2 =  pendulum.create(2014, 1, 30, 0, 0, 0, 0)

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

    import pendulum

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

    born = pendulum.from_date(1987, 4, 23)
    not_birthday = pendulum.from_date(2014, 9, 26)
    birthday = pendulum.from_date(2014, 2, 23)
    past_birthday = pendulum.now().sub(years=50)

    born.is_birthday(not_birthday)
    False
    born.is_birthday(birthday)
    True
    past_birthday.is_birthday()
    # Compares to now by default
    True


Addition and Subtraction
========================

To easily adding and subtracting time, you can use the ``add()`` and ``sub()``
methods`.
Each method returns a new ``Pendulum`` instance.

.. code-block:: python

    import pendulum

    dt = pendulum.create(2012, 1, 31, 0)

    dt.to_datetime_string()
    '2012-01-31 00:00:00'

    dt = dt.add(years=5)
    '2017-01-31 00:00:00'
    dt = dt.add(years=1)
    '2018-01-31 00:00:00'
    dt = dt.sub(years=1)
    '2017-01-31 00:00:00'
    dt = dt.sub(years=5)
    '2012-01-31 00:00:00'

    dt = dt.add(months=60)
    '2017-01-31 00:00:00'
    dt = dt.add(months=1)
    '2017-02-28 00:00:00'
    dt = dt.sub(months=1)
    '2017-01-28 00:00:00'
    dt = dt.sub(months=60)
    '2012-01-28 00:00:00'

    dt = dt.add(days=29)
    '2012-02-26 00:00:00'
    dt = dt.add(days=1)
    '2012-02-27 00:00:00'
    dt = dt.sub(days=1)
    '2012-02-26 00:00:00'
    dt = dt.sub(days=29)
    '2012-01-28 00:00:00'

    dt = dt.add(weeks=3)
    '2012-02-18 00:00:00'
    dt = dt.add(weeks=1)
    '2012-02-25 00:00:00'
    dt = dt.sub(weeks=1)
    '2012-02-18 00:00:00'
    dt = dt.sub(weeks=3)
    '2012-01-28 00:00:00'

    dt = dt.add(hours=24)
    '2012-01-29 00:00:00'
    dt = dt.add(hours=1)
    '2012-02-25 01:00:00'
    dt = dt.sub(hours=1)
    '2012-02-29 00:00:00'
    dt = dt.sub(hours=24)
    '2012-01-28 00:00:00'

    dt = dt.add(minutes=61)
    '2012-01-28 01:01:00'
    dt = dt.add(minutes=1)
    '2012-01-28 01:02:00'
    dt = dt.sub(minutes=1)
    '2012-01-28 01:01:00'
    dt = dt.sub(minutes=24)
    '2012-01-28 00:00:00'

    dt = dt.add(seconds=61)
    '2012-01-28 00:01:01'
    dt = dt.add(seconds=1)
    '2012-01-28 00:01:02'
    dt = dt.sub(seconds=1)
    '2012-01-28 00:01:01'
    dt = dt.sub(seconds=61)
    '2012-01-28 00:00:00'

    dt = dt.add(years=3, months=2, days=6, hours=12, minutes=31, seconds=43)
    '2015-04-03 12:31:43'
    dt = dt.sub(years=3, months=2, days=6, hours=12, minutes=31, seconds=43)
    '2012-01-28 00:00:00'

    # You can also add or remove a timedelta
    dt.add_timedelta(timedelta(hours=3, minutes=4, seconds=5))
    '2012-01-28 03:04:05'
    dt.sub_timedelta(timedelta(hours=3, minutes=4, seconds=5))
    '2012-01-28 00:00:00'


Difference
==========

The ``diff()`` method returns a `Period`_ instance that represents the total duration
between two ``Pendulum`` instances. This interval can be then expressed in various units.
These interval methods always return *the total difference expressed* in the specified time requested.
All values are truncated and not rounded.

The ``diff()`` method has a default first parameter which is the ``Pendulum`` instance to compare to,
or ``None`` if you want to use ``now()``.
The 2nd parameter is optional and indicates if you want the return value to be the absolute value
or a relative value that might have a ``-`` (negative) sign if the passed in date
is less than the current instance.
This will default to ``True``, return the absolute value. The comparisons are done in UTC.

.. code-block:: python

    import pendulum

    dt_ottawa = pendulum.from_date(2000, 1, 1, 'America/Toronto')
    dt_vancouver = pendulum.from_date(200, 1, 1, 'America/Vancouver')

    dt_ottawa.diff(dt_vancouver).in_hours()
    3
    dt_ottawa.diff(dt_vancouver, False).in_hours()
    3
    dt_vancouver.diff(dt_ottawa, False).in_hours()
    -3

    dt = pendulum.create(2012, 1, 31, 0)
    dt.diff(dt.add(months=1)).in_days()
    29
    dt.diff(dt.sub(months=1), False).in_days()
    -31

    dt = pendulum.create(2012, 4, 30, 0)
    dt.diff(dt.add(months=1)).in_days()
    30
    dt.diff(dt.add(weeks=1)).in_days()
    7

    dt = pendulum.create(2012, 1, 1, 0)
    dt.diff(dt.add(seconds=59)).in_minutes()
    0
    dt.diff(dt.add(seconds=60)).in_minutes()
    1
    dt.diff(dt.add(seconds=119)).in_minutes()
    1
    dt.diff(dt.add(seconds=120)).in_minutes()
    2

    dt.add(seconds=120).seconds_since_midnight()
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

    import pendulum

    # The most typical usage is for comments
    # The instance is the date the comment was created
    # and its being compared to default now()
    pendulum.now().sub(dayss=1).diff_for_humans()
    '5 days ago'

    pendulum.now().diff_for_humans(Pendulum.now().sub(years=1))
    '1 year after'

    dt = pendulum.from_date(2011, 8, 1)
    dt.diff_for_humans(dt.add(months=1))
    '1 month before'
    dt.diff_for_humans(dt.sub(months=1))
    '1 month after'

    pendulum.now().add(seconds=5).diff_for_humans()
    '5 seconds from now'

    pendulum.now().sub(days=24).diff_for_humans()
    '3 weeks ago'

    pendulum.now().sub(days=24).diff_for_humans(absolute=True)
    '3 weeks'

You can also change the locale of the string either globally by using ``pendulum.set_locale('fr')``
before the ``diff_for_humans()`` call or specifically for the call by passing the ``locale`` keyword
argument. See the `Localization`_ section for more detail.

.. code-block:: python

    import pendulum

    pendulum.set_locale('de')
    pendulum.now().add(years=1).diff_for_humans()
    'in 1 Jahr'
    pendulum.now().add(years=1).diff_for_humans(locale='fr')
    'dans 1 an'


Modifiers
=========

These group of methods perform helpful modifications to a copy of the current instance.
You'll notice that the ``start_of()``, ``next()`` and ``previous()`` methods
set the time to ``00:00:00`` and the ``end_of()`` methods set the time to ``23:59:59``.

The only one slightly different is the ``average()`` method.
It moves your instance to the middle date between itself and the provided Pendulum argument.

.. code-block:: python

    import pendulum

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of('day')
    '2012-01-31 00:00:00'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of('day')
    '2012-01-31 23:59:59'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of('month')
    '2012-01-01 00:00:00'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of('month')
    '2012-01-31 23:59:59'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of('year')
    '2012-01-01 00:00:00'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of('year')
    '2012-01-31 23:59:59'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of('decade')
    '2010-01-01 00:00:00'

    dt = Pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of('decade')
    '2019-01-31 23:59:59'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of('century')
    '2000-01-01 00:00:00'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of('century')
    '2099-12-31 23:59:59'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.start_of('week')
    '2012-01-30 00:00:00'
    dt.day_of_week == pendulum.MONDAY
    True # ISO8601 week starts on Monday

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of('week')
    '2012-02-05 23:59:59'
    dt.day_of_week == pendulum.SUNDAY
    True # ISO8601 week ends on SUNDAY

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.end_of('week')
    '2012-02-05 23:59:59'
    dt.day_of_week == pendulum.SUNDAY
    True # ISO8601 week ends on SUNDAY

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.next(pendulum.WEDNESDAY)
    '2012-02-01 00:00:00'
    dt.day_of_week == pendulum.WEDNESDAY
    True

    dt = Pendulum.create(2012, 1, 1, 12, 0, 0)
    dt.next()
    '2012-01-08 00:00:00'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.previous(pendulum.WEDNESDAY)
    '2012-01-25 00:00:00'
    dt.day_of_week == pendulum.WEDNESDAY
    True

    dt = pendulum.create(2012, 1, 1, 12, 0, 0)
    dt.previous()
    '2011-12-25 00:00:00'

    start = pendulum.create(2014, 1, 1, 0, 0, 0)
    end = pendulum.create(2014, 1, 30, 0, 0, 0)
    start.average(end)
    '2014-01-15 12:00:00'

    # others that are defined that are similar
    # and tha accept month, quarter and year units
    # first_of(), last_of(), nth_of()


Timezones
=========

.. versionchanged:: 0.5

    ``Pendulum`` provides its own timezone handling and no longer
    rely on ``pytz`` which does not always perform very well, particularly
    to localize and normalize a naive-datetime.


Timezones are an important part of every datetime library and ``Pendulum``
tries to provide an easy and accurate system to handle them properly.

.. note::

    The timezone system works best inside the ``pendulum`` ecosystem but
    can also be used with the standard ``datetime`` library with a few limitations.
    See `Using the timezone library directly`_

Normalization
-------------

When you create a ``Pendulum`` instance, the library will normalize it for the
given timezone to properly handle any transition that might have occurred.

.. code-block:: python

    import pendulum

    pendulum.create(2013, 3, 31, 2, 30, 0, 0, 'Europe/Paris')
    # 2:30 for the 31th of March 2013 does not exist
    # so pendulum will return the actual time which is 3:30+02:00
    '2013-03-31T03:30:00+02:00'

    pendulum.create(2013, 10, 27, 2, 30, 0, 0, 'Europe/Paris')
    # Here, 2:30 exists twice in the day so pendulum will
    # assume that the transition already occurred
    '2013-10-27T02:30:00+01:00'


Shifting time to transition
---------------------------

So, what happens when you add time to a ``Pendulum`` instance and stumble upon
a transition time?
Well, ``Pendulum``, provided with the context of the previous instance, will
adopt the proper behavior and apply the transition accordingly.

.. code-block:: python

    import pendulum

    dt = pendulum.create(2013, 3, 31, 1, 59, 59, 999999, 'Europe/Paris')
    '2013-03-31T01:59:59.999999+01:00'
    dt = dt.add(microseconds=1)
    '2013-03-31T03:00:00+02:00'
    dt.subtract(microseconds=1)
    '2013-03-31T01:59:59.999998+01:00'

    dt = pendulum.create(2013, 10, 27, 1, 59, 59, 999999, 'Europe/Paris')
    dt = dt.add(hours=1)
    # We can't just do
    # pendulum.create(2013, 10, 27, 2, 59, 59, 999999, 'Europe/Paris')
    # because of the default normalization
    '2013-10-27T02:59:59.999999+02:00'
    dt = dt.add(microseconds=1)
    '2013-10-27T02:00:00+01:00'
    dt = dt.subtract(microseconds=1)
    '2013-10-27T02:59:59.999999+02:00'

Switching timezones
-------------------

You can easily change the timezone of a ``Pendulum`` instance
with the ``in_timezone()`` method.

.. note::

    You can also use the more concise ``in_tz()``

.. code-block:: python

    in_paris = pendulum.create(2016, 8, 7, 22, 24, 30, tz='Europe/Paris')
    '2016-08-07T22:24:30+02:00'
    in_paris.in_timezone('America/New_York')
    '2016-08-07T16:24:30-04:00'
    in_paris.in_tz('Asia/Tokyo')
    '2016-08-08T05:24:30+09:00'

Using the timezone library directly
-----------------------------------

Like said in the introduction, you can use the timezone library
directly with standard ``datetime`` objects but with limitations, especially
when adding and subtracting time around transition times.

.. code-block:: python

    from datetime import datetime, timedelta
    from pendulum import timezone

    paris = timezone('Europe/Paris')
    dt = datetime(2013, 3, 31, 2, 30)
    dt = paris.convert(dt)
    dt.isoformat()
    '2013-03-31T03:30:00+02:00'
    # Normalization works as expected

    new_york = timezone('America/New_York')
    new_york.convert(dt).isoformat()
    '2013-03-30T21:30:00-04:00'
    # Timezone switching works as expected

    dt = datetime(2013, 3, 31, 1, 59, 59, 999999)
    dt = paris.convert(dt)
    dt.isoformat()
    '2013-03-31T01:59:59.999999+01:00'
    dt = dt + timedelta(microseconds=1)
    dt.isoformat()
    '2013-03-31T02:00:00+01:00'
    # This does not work as expected.
    # This is a limitation of datetime objects
    # that can't switch around transition times.
    # However, you can use convert()
    # to retrieve the proper datetime.
    dt = tz.convert(dt)
    dt.isoformat()
    '2013-03-31T03:00:00+02:00'


Testing
=======

The testing methods allow you to set a ``Pendulum`` instance (real or mock) to be returned
when a "now" instance is created.
The provided instance will be returned specifically under the following conditions:

* A call to the ``now()`` method, ex. ``pendulum.now()``.
* When the string "now" is passed to the ``parse()``, ex. ``pendulum.parse('now')``

.. code-block:: python

    import pendulum

    # Create testing datetime
    known = pendulum.create(2001, 5, 21, 12)

    # Set the mock
    pendulum.set_test_now(known)

    print(pendulum.now())
    '2001-05-21T12:00:00+00:00'

    print(pendulum.parse('now'))
    '2001-05-21T12:00:00+00:00'

    # Clear the mock
    pendulum.set_test_now()

    print(pendulum.now())
    '2016-07-10T22:10:33.954851-05:00'

Related methods will also returned values mocked according to the *now* instance.

.. code-block:: python

    print(pendulum.today())
    '2001-05-21T00:00:00+00:00'

    print(pendulum.tomorrow())
    '2001-05-22T00:00:00+00:00'

    print(pendulum.yesterday())
    '2001-05-20T00:00:00+00:00'

If you don't want to manually clear the mock (or you are afraid of forgetting),
you can use the provided ``test()`` contextmanager.

.. code-block:: python

    import pendulum

    known = pendulum.create(2001, 5, 21, 12)

    with pendulum.test(known):
        print(pendulum.now())
        '2001-05-21T12:00:00+00:00'

    print(pendulum.now())
    '2016-07-10T22:10:33.954851-05:00'


Interval
========

The ``Interval`` class is inherited from the native ``timedelta`` class.
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

    import pendulum

    it = pendulum.Interval(days=1177, seconds=7284, microseconds=1234)
    it = pendulum.interval(days=1177, seconds=7284, microseconds=1234)

    # You can use an existing timedelta instance
    delta = timedelta(days=1177, seconds=7284, microseconds=1234)
    it = pendulum.interval.instance(delta)

Properties and Duration Methods
-------------------------------

The ``Interval`` class brings more properties than the default ``days``, ``seconds`` and
``microseconds``.

.. code-block:: python

    import pendulum

    it = pendulum.interval(days=1177, seconds=7284, microseconds=1234)

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

Similarly, it has the ``in_xxx()`` methods which returns to total duration in each
supported unit as a truncated integer.

.. code-block:: python

    it.in_weeks()
    168

    it.in_days()
    1177

    it.in_hours()
    28250

    it.in_minutes()
    1695001

    it.in_seconds()
    101700084

It also has a handy ``in_words()``, which determines the interval representation when printed.

.. code-block:: python

    import pendulum

    pendulum.interval.set_locale('fr')
    # or pendulum.interval.set_locale('fr')

    it = pendulum.interval(days=1177, seconds=7284, microseconds=1234)

    it.in_words()
    '168 semaines 1 jour 2 heures 1 minute 24 secondes'

    print(it)
    '168 semaines 1 jour 2 heures 1 minute 24 secondes'

    it.in_words(locale='de')
    '168 Wochen 1 Tag 2 Stunden 1 Minute 24 Sekunden'


Period
======

When you subtract a ``Pendulum`` instance to another, or use the ``diff()`` method, it will return a ``Period`` instance.
it inherits from the `Interval`_ class with the added benefit that it is aware of the
instances that generated it, so that it can give access to more methods and properties:

.. code-block:: python

    from pendulum import Pendulum

    start = Pendulum(2000, 1, 1)
    end = Pendulum(2000, 1, 31)

    period = end - start
    period.in_weekdays()
    21

    period.in_weekend_days()
    10


.. warning::

    Due to its nature (fixed duration between two datetimes), most arithmetic operations will
    return an ``Interval`` instead of a ``Period``.

    .. code-block:: python

        dt1 = Pendulum(2016, 8, 7, 12, 34, 56)
        dt2 = dt1.add(days=6, seconds=34)
        period = Period(dt1, dt2)
        period * 2
        # <Interval [1 week 5 days 1 minute 8 seconds]>


Instantiation
-------------

You can create an instance in the following ways:

.. code-block:: python

    import pendulum

    start = pendulum.Pendulum(2000, 1, 1)
    end = pendulum.Pendulum(2000, 1, 31)

    period = pendulum.Period(start, end)
    period = pendulum.period(start, end)

You can also make an inverted period:

.. code-block:: python

    period = pendulum.period(end, start)
    period.in_weekdays()
    -21

    period.in_weekend_days()
    -10

If you have inverted dates but want to make sure that the period is positive,
you set the ``absolute`` keyword argument to ``True``:

.. code-block:: python

    period = pendulum.period(end, start, absolute=True)
    period.in_weekdays()
    21

    period.in_weekend_days()
    10

Range
-----

If you want to iterate over a period, you can use the ``range()`` method:

.. code-block:: python

    import pendulum

    start = pendulum.Pendulum(2000, 1, 1)
    end = pendulum.Pendulum(2000, 1, 10)

    period = pendulum.period(start, end)

    for dt in period.range('days'):
        print(dt)

    '2000-01-01T00:00:00+00:00'
    '2000-01-02T00:00:00+00:00'
    '2000-01-03T00:00:00+00:00'
    '2000-01-04T00:00:00+00:00'
    '2000-01-05T00:00:00+00:00'
    '2000-01-06T00:00:00+00:00'
    '2000-01-07T00:00:00+00:00'
    '2000-01-08T00:00:00+00:00'
    '2000-01-09T00:00:00+00:00'
    '2000-01-10T00:00:00+00:00'

.. note::

    Supported units for ``range()`` are: ``years``, ``months``, ``weeks``,
    ``days``, ``hours``, ``minutes`` and ``seconds``

.. note::

    If you just want a generator you can use the ``xrange()`` method.

You can also directly iterate over the ``Period`` instance, the unit will be ``days`` in this case:

.. code-block:: python

    for dt in period:
        print(dt)

You can check if a ``Pendulum`` instance is inside a period using the ``in`` keyword:

.. code-block:: python

    dt = Pendulum(2000, 1, 4)

    dt in period
    True
