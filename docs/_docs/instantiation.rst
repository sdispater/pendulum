Instantiation
=============

There are several different methods available to create a new `DateTime` instance.

First there is the main ``datetime()`` helper.

.. code-block:: python

    import pendulum

    dt = pendulum.datetime(2015, 2, 5, tz='America/Vancouver')
    isinstance(dt, datetime)
    True

``datetime()`` sets the time to ``00:00:00`` if it's not specified,
and the timezone (the ``tz`` keyword argument) to ``UTC``.

It otherwise can be a ``Timezone`` instance or simply a string timezone value.

.. note::

    Supported strings for timezones are the one provided by the `IANA time zone database <https://www.iana.org/time-zones>`_.
    The special ``local`` string is also supported and will return your current timezone.

.. warning::

    The ``tz`` argument is keyword-only, unlike in version `1.x`

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

To accompany ``now()``, a few other static instantiation helpers exist to create known instances.
The only thing to really notice here is that ``today()``, ``tomorrow()`` and ``yesterday()``,
besides behaving as expected, all accept a timezone parameter
and each has their time value set to ``00:00:00``.

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

The next helper, ``from_format()``, is similar to the native ``datetime.strptime()`` function
but uses custom tokens to create a ``DateTime`` instance.

.. code-block:: python

    dt = pendulum.from_format('1975-05-21 22', 'YYYY-MM-DD HH')
    print(dt)
    '1975-05-21T22:00:00+00:00'

.. note::

    To see all the available tokens, you can check the :ref:`Formatter` section.

It also accepts a ``tz`` keyword argument to specify the timezone:

.. code-block:: python

    dt = pendulum.from_format('1975-05-21 22', 'YYYY-MM-DD HH', tz='Europe/London')
    '1975-05-21T22:00:00+01:00'

The final helper is for working with unix timestamps.
``from_timestamp()`` will create a ``DateTime`` instance equal to the given timestamp
and will set the timezone as well or default it to ``UTC``.

.. code-block:: python

    dt = pendulum.from_timestamp(-1)
    print(dt)
    '1969-12-31T23:59:59+00:00'

    dt  = pendulum.from_timestamp(-1, tz='Europe/London')
    print(dt)
    '1970-01-01T00:59:59+01:00'

Finally, if you find yourself inheriting a ``datetime`` instance,
you can create a ``DateTime`` instance via the ``instance()`` function.

.. code-block:: python

    dt = datetime(2008, 1, 1)
    p = pendulum.instance(dt)
    print(p)
    '2008-01-01T00:00:00+00:00'
