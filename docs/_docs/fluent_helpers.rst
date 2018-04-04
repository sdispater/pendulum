Fluent Helpers
==============

Pendulum provides helpers that returns a new instance with some attributes
modified compared to the original instance.
However, none of these helpers, with the exception of explicitely setting the
timezone, will change the timezone of the instance. Specifically,
setting the timestamp will not set the corresponding timezone to UTC.

.. code-block:: python

    import pendulum
    from datetime import time, date

    dt = pendulum.now()

    dt = dt.set(year=1975, month=5, day=21).to_datetime_string()
    '1975-05-21 13:45:18'

    dt.set(hour=22, minute=32, second=5).to_datetime_string()
    '2016-11-16 22:32:05'

    dt.on(1975, 5, 21).at(22, 32, 5).to_datetime_string()
    '1975-05-21 22:32:05'

    dt.set(tz='Europe/London')

    dt.set(tz='America/Toronto').in_timezone('America/Vancouver')

.. note::

    ``set(tz=...)`` just modify the timezone information without
    making any conversion while ``in_timezone()`` converts the time in the
    appropriate timezone.
