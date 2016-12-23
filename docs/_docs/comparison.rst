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

    born = pendulum.create(1987, 4, 23)
    not_birthday = pendulum.create(2014, 9, 26)
    birthday = pendulum.create(2014, 2, 23)
    past_birthday = pendulum.now().subtract(years=50)

    born.is_birthday(not_birthday)
    False
    born.is_birthday(birthday)
    True
    past_birthday.is_birthday()
    # Compares to now by default
    True
