Introduction
============

Pendulum is a Python package to ease datetimes manipulation.

It is heavily inspired by `Carbon <http://carbon.nesbot.com>`_ for PHP.

The ``Pendulum`` class is a drop-in replacement for the native ``datetime``
class (it is inherited from it).

Special care has been taken to ensure timezones are handled correctly,
and where appropriate are based on the underlying ``tzinfo`` implementation.
For example all comparisons are done in UTC or in the timezone of the datetime being used.

.. code-block:: python

    import pendulum

    dt_toronto = pendulum.create(2012, 1, 1, tz='America/Toronto')
    dt_vancouver = pendulum.create(2012, 1, 1, tz='America/Vancouver')

    print(dt_vancouver.diff(dt_toronto).in_hours())
    3

The default timezone, except when using the ``now()``, method will always be ``UTC``.

.. note::

    Also ``is`` comparisons (like ``is_today()``) are done in the timezone of the provided Pendulum instance.

    For example, my current timezone is -13 hours from Tokyo.
    So ``pendulum.now('Asia/Tokyo').is_today()`` would only return ``False`` for any time past 1 PM my time.
    This doesn't make sense since ``now()`` in tokyo is always today in Tokyo.

    Thus the comparison to ``now()`` is done in the same timezone as the current instance.
