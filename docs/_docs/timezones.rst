Timezones
=========


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


.. note::

    You can control the normalization behavior:

    .. code-block:: python

        import pendulum

        pendulum.set_transition_rule(pendulum.PRE_TRANSITION)

        pendulum.create(2013, 3, 31, 2, 30, 0, 0, 'Europe/Paris')
        '2013-03-31T01:30:00+01:00'
        pendulum.create(2013, 10, 27, 2, 30, 0, 0, 'Europe/Paris')
        '2013-10-27T02:30:00+02:00'

        pendulum.set_transition_rule(pendulum.TRANSITION_ERROR)

        pendulum.create(2013, 3, 31, 2, 30, 0, 0, 'Europe/Paris')
        # NonExistingTime: The datetime 2013-03-31 02:30:00 does not exist
        pendulum.create(2013, 10, 27, 2, 30, 0, 0, 'Europe/Paris')
        # AmbiguousTime: The datetime 2013-10-27 02:30:00 is ambiguous.

    Note that it only affects instances at creation time. Shifting time around
    transition times still behaves the same.

.. note::

    As of version **0.7.0**, and to be consistent with the standard library (Python 3.6+),
    the ``Pendulum`` class accepts a ``fold`` keyword argument which will be used, when set explicitely,
    to determine the rule to apply on ambiguous or non-existing times.
    Be aware that when it is not set explicitely, the previous behavior remains,
    i.e. the configured transition rule or the default one will be used.

    .. code-block:: python

        from pendulum import Pendulum

        dt = Pendulum(2013, 3, 31, 2, 30, 0, 0, 'Europe/Paris')
        dt.isoformat()
        '2013-03-31T03:30:00+02:00'

        dt = Pendulum(2013, 3, 31, 2, 30, 0, 0, 'Europe/Paris', fold=0)
        dt.isoformat()
        '2013-03-31T01:30:00+01:00'

        dt = Pendulum(2013, 3, 31, 2, 30, 0, 0, 'Europe/Paris', fold=1)
        dt.isoformat()
        '2013-03-31T03:30:00+02:00'

        dt = Pendulum(2013, 10, 27, 2, 30, 0, 0, 'Europe/Paris', fold=0)
        dt.isoformat()
        '2013-10-27T02:30:00+02:00'

        dt = Pendulum(2013, 10, 27, 2, 30, 0, 0, 'Europe/Paris', fold=1)
        dt.isoformat()
        '2013-10-27T02:30:00+01:00'

Shifting time to transition
---------------------------

So, what happens when you add time to a ``Pendulum`` instance and stumble upon
a transition time?
Well ``Pendulum``, provided with the context of the previous instance, will
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

.. warning::

    By default in **Python 3.6+**, the value of the ``fold`` attribute will be used
    to determine the transition rule. So the behavior will be slightly different
    compared to previous versions.

    .. code-block:: python

        from datetime import datetime
        from pendulum import timezone

        paris = timezone('Europe/Paris')
        dt = datetime(2013, 3, 31, 2, 30)
        # By default, fold is set to 0
        dt = paris.convert(dt)
        dt.isoformat()
        '2013-03-31T01:30:00+01:00'

        dt = datetime(2013, 3, 31, 2, 30, fold=1)
        dt = paris.convert(dt)
        dt.isoformat()
        '2013-03-31T03:30:00+02:00'

    You can override this behavior by explicitely passing the
    transition rule to ``convert()``.

    .. code-block:: python

        paris = timezone('Europe/Paris')
        dt = datetime(2013, 3, 31, 2, 30)
        # By default, fold is set to 0
        dt = paris.convert(dt, dst_rule=paris.POST_TRANSITION)
        dt.isoformat()
        '2013-03-31T03:30:00+02:00'


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


.. note::

    You can control the normalization behavior:

    .. code-block:: python

        from datetime import datetime
        from pendulum import timezone

        tz = timezone('Europe/Paris')

        dt = datetime(2013, 3, 31, 2, 30)
        dt = tz.convert(dt, dst_rule=tz.PRE_TRANSITION)
        dt.isoformat()
        '2013-03-31T01:30:00+01:00'
        tz.convert(dt, dst_rule=tz.TRANSITION_ERROR)
        # NonExistingTime: The datetime 2013-03-31 02:30:00 does not exist.


You can also get a normalized ``datetime`` object from a ``Timezone`` by using the ``datetime()`` method:

.. code-block:: python

    import pendulum

    tz = pendulum.timezone('Europe/Paris')
    dt = tz.datetime(2013, 3, 31, 2, 30)
    dt.isoformat()
    '2013-03-31T03:30:00+02:00'
