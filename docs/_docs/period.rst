Period
======

When you subtract a ``Pendulum`` instance to another, or use the ``diff()`` method, it will return a ``Period`` instance.
it inherits from the `Interval`_ class with the added benefit that it is aware of the
instances that generated it, so that it can give access to more methods and properties:

.. code-block:: python

    import pendulum

    start = pendulum.datetime(2000, 1, 1)
    end = pendulum.datetime(2000, 1, 31)

    period = end - start

    # You have access to the years and months
    # properties and there related methods
    start = pendulum.datetime(2000, 11, 20)
    end = pendulum.datetime(2016, 11, 5)

    period = end - start

    period.years
    15
    period.months
    11
    period.in_years()
    15
    period.in_months()
    191

    # Note that the weeks property
    # will change compared to the Interval class
    period.weeks
    2 # 832 for the interval

    # However the days property will still remain the same
    # to keep the compatiblity with the timedelta class
    period.days
    5829

Be aware that a period, just like an interval, is compatible with the ``timedelta`` class regarding
its attributes. However, its custom attributes (like ``remaining_days``) will be aware of any DST
transitions that might have occurred and adjust accordingly. Let's take an example:

.. code-block:: python

    import pendulum

    start = pendulum.datetime(2017, 3, 7, tz='America/Toronto')
    end = start.add(days=6)

    period = end - start

    # timedelta properties
    period.days
    5
    period.seconds
    82800

    # period properties
    period.remaining_days
    6
    period.hours
    0
    period.remaining_seconds
    0


.. warning::

    Due to its nature (fixed duration between two datetimes), most arithmetic operations will
    return an ``Interval`` instead of a ``Period``.

    .. code-block:: python

        import pendulum

        dt1 = pendulum.datetime(2016, 8, 7, 12, 34, 56)
        dt2 = dt1.add(days=6, seconds=34)
        period = pendulum.period(dt1, dt2)
        period * 2
        # <Interval [1 week 5 days 1 minute 8 seconds]>


Instantiation
-------------

You can create an instance in the following ways:

.. code-block:: python

    import pendulum

    start = pendulum.datetime(2000, 1, 1)
    end = pendulum.datetime(2000, 1, 31)

    period = pendulum.period(start, end)
    period = end - start

You can also make an inverted period:

.. code-block:: python

    period = pendulum.period(end, start)
    period.days
    -30

If you have inverted dates but want to make sure that the period is positive,
you set the ``absolute`` keyword argument to ``True``:

.. code-block:: python

    period = pendulum.period(end, start, absolute=True)
    period.days
    30

Range
-----

If you want to iterate over a period, you can use the ``range()`` method:

.. code-block:: python

    import pendulum

    start = pendulum.datetime(2000, 1, 1)
    end = pendulum.datetime(2000, 1, 10)

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

You can pass an amount for the passed unit to control the length of the gap:

.. code-block:: python

    for dt in period.range('days', 2):
        print(dt)

    '2000-01-01T00:00:00+00:00'
    '2000-01-03T00:00:00+00:00'
    '2000-01-05T00:00:00+00:00'
    '2000-01-07T00:00:00+00:00'
    '2000-01-09T00:00:00+00:00'

You can also directly iterate over the ``Period`` instance, the unit will be ``days`` in this case:

.. code-block:: python

    for dt in period:
        print(dt)

You can check if a ``Pendulum`` instance is inside a period using the ``in`` keyword:

.. code-block:: python

    dt = pendulum.datetime(2000, 1, 4)

    dt in period
    True

Intersection
------------

You can get the intersection of the current ``Period`` instance with others by
using the ``intersect()`` method.

.. code-block:: python

    import pendulum


    monday = pendulum.datetime(2016, 9, 12)
    wednesday = monday.next(pendulum.WEDNESDAY)
    friday = monday.next(pendulum.FRIDAY)
    saturday = monday.next(pendulum.SATURDAY)

    period = pendulum.datetime(monday, friday)

    period.intersect(pendulum.period(wednesday, saturday))
    # <Period [2016-09-14T00:00:00+00:00 -> 2016-09-16T00:00:00+00:00]>

You can also pass multiple period to ``intersect()``.

.. code-block:: python

    import pendulum


    monday = pendulum.datetime(2016, 9, 12)
    wednesday = monday.next(pendulum.WEDNESDAY)
    thursday = monday.next(pendulum.THURSDAY)
    friday = monday.next(pendulum.FRIDAY)
    saturday = monday.next(pendulum.SATURDAY)
    sunday = monday.next(pendulum.SUNDAY)

    period = pendulum.period(monday, friday)
    wednesday_to_saturday = pendulum.period(wednesday, saturday)
    thursday_to_sunday = pendulum.period(thursday, sunday)

    period.intersect(
        wednesday_to_saturday,
        thursday_to_sunday
    )
    # <Period [2016-09-15T00:00:00+00:00 -> 2016-09-16T00:00:00+00:00]>

If no intersection exists, ``intersect()`` will return ``None``:

.. code-block:: python

    period.intersect(pendulum.period(saturday, sunday))
    None
