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

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
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

    dt = pendulum.create(2012, 1, 1, 12, 0, 0)
    dt.next()
    '2012-01-08 00:00:00'
    dt.next(keep_time=True)
    '2012-01-08T12:00:00+00:00'

    dt = pendulum.create(2012, 1, 31, 12, 0, 0)
    dt.previous(pendulum.WEDNESDAY)
    '2012-01-25 00:00:00'
    dt.day_of_week == pendulum.WEDNESDAY
    True

    dt = pendulum.create(2012, 1, 1, 12, 0, 0)
    dt.previous()
    '2011-12-25 00:00:00'
    dt.previous(keep_time=True)
    '2011-12-25 12:00:00'

    start = pendulum.create(2014, 1, 1, 0, 0, 0)
    end = pendulum.create(2014, 1, 30, 0, 0, 0)
    start.average(end)
    '2014-01-15 12:00:00'

    # others that are defined that are similar
    # and tha accept month, quarter and year units
    # first_of(), last_of(), nth_of()
