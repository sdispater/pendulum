Interval
========

The ``Interval`` class is inherited from the native ``timedelta`` class.
It has many improvements over the base class.

.. note::

    Even though, it inherits from the ``timedelta`` class, its behavior is slightly different.
    The more important to notice is that the native normalization does not happen, this is so that
    it feels more intuitive.

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
    it.remaning_days
    1

    # The remaining number in each unit
    it.hours
    2
    it.minutes
    1

    # Seconds are, like days, a special case and the default
    # property will return the whole value of remaining
    # seconds just like the timedelta class for compatibility
    it.seconds
    7284

    # If you want the number of seconds not included
    # in hours and minutes
    it.remaining_seconds
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
