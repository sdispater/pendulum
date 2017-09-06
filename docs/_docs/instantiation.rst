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

.. note::

    Supported strings for timezones are the one provided by the `IANA time zone database <https://www.iana.org/time-zones>`_.
    The special ``local`` string is also supported and will return your current timezone.

This is again shown in the next example which also introduces the ``now()`` function.

.. code-block:: python

    import pendulum

    now = pendulum.now()

    tz = pendulum.timezone('Europe/London')
    now_in_london_tz = pendulum.now(tz)

    # or just pass the timezone as a string
    now_in_london_tz = pendulum.now('Europe/London')
    print(now_in_london_tz.timezone_name)
    'Europe/London'

    # or to create a date with a timezone of +1 to GMT
    # during DST then just pass an integer
    print(pendulum.now(1).timezone_name)
    '+01:00'

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

The next helper is ``create()`` which allows you to provide
as many or as few arguments as you want and will provide default values for all others.

.. code-block:: python

    pendulum.create(year, month, day, hour, minute, second, microsecond, tz)

``create()`` will default any null parameter to the current date for the date part and to ``00:00:00`` for time.
As before, the ``tz`` defaults to the ``UTC`` timezone and otherwise can be a ``Timezone`` instance
or simply a string timezone value.

.. code-block:: python

    pendulum.from_format(time, fmt, tz)

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

Parsing
-------

You can also instantiate ``Pendulum`` instances by passing a string to the ``parse()`` method.

.. code-block:: python

    import pendulum

    dt = pendulum.parse('1975-05-21 22:00:00')
    print(dt)
    '1975-05-21T22:00:00+00:00

    # You can pass a tz keyword to specify the timezone
    dt = pendulum.parse('1975-05-21 22:00:00', tz='Europe/Paris')
    print(dt)
    '1975-05-21T22:00:00+01:00'

The library natively supports the RFC 3339 format, most ISO 8601 formats and some other common formats.
If you pass a non-standard or more complicated string, the library will fallback on the
`dateutil <https://dateutil.readthedocs.io>`_ parser.

RFC 3339
~~~~~~~~

+-----------------------------------+-------------------------------------------+
|String                             |Output                                     |
+===================================+===========================================+
|1996-12-19T16:39:57-08:00          |1996-12-19T16:39:57-08:00                  |
+-----------------------------------+-------------------------------------------+
|1990-12-31T23:59:59Z               |1990-12-31T23:59:59+00:00                  |
+-----------------------------------+-------------------------------------------+

ISO 8601
~~~~~~~~

Datetime
++++++++

+-----------------------------------+-------------------------------------------+
|String                             |Output                                     |
+===================================+===========================================+
|20161001T143028+0530               |2016-10-01T14:30:28+05:30                  |
+-----------------------------------+-------------------------------------------+
|20161001T14                        |2016-10-01T14:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+

Date
++++

+-----------------------------------+-------------------------------------------+
|String                             |Output                                     |
+===================================+===========================================+
|2012                               |2012-01-01T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+
|2012-05-03                         |2012-05-03T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+
|20120503                           |2012-05-03T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+
|2012-05                            |2012-05-01T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+

Ordinal day
+++++++++++

+-----------------------------------+-------------------------------------------+
|String                             |Output                                     |
+===================================+===========================================+
|2012-007                           |2012-01-07T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+
|2012007                            |2012-01-07T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+

Week number
+++++++++++

+-----------------------------------+-------------------------------------------+
|String                             |Output                                     |
+===================================+===========================================+
|2012-W05                           |2012-01-30T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+
|2012W05                            |2012-01-30T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+
|2012-W05-5                         |2012-02-03T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+
|2012W055                           |2012-02-03T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+

Time
++++

When passing only time information the date will default to today.

+-----------------------------------+-------------------------------------------+
|String                             |Output                                     |
+===================================+===========================================+
|00:00                              |2016-12-17T00:00:00+00:00                  |
+-----------------------------------+-------------------------------------------+
|12:04:23                           |2016-12-17T12:04:23+00:00                  |
+-----------------------------------+-------------------------------------------+
|120423                             |2016-12-17T12:04:23+00:00                  |
+-----------------------------------+-------------------------------------------+
|12:04:23.45                        |2016-12-17T12:04:23.450000+00:00           |
+-----------------------------------+-------------------------------------------+


.. note::

    You can pass the ``strict`` keyword argument to ``parse()`` to get the exact type
    that the string represents:

    .. code-block:: python

        import pendulum

        pendulum.parse('2012-05-03', strict=True)
        # <Date [2012-05-03]>

        pendulum.parse('12:04:23', strict=True)
        # <Time [12:04:23]>
