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

    dt = dt.year_(1975).month_(5).day_(21).to_datetime_string()
    '1975-05-21 13:45:18'

    dt.hour_(22).minute_(32).second_(5).to_datetime_string()
    '2016-11-16 22:32:05'

    dt.on(1975, 5, 21).at(22, 32, 5).to_datetime_string()
    '1975-05-21 22:32:05'

    dt.timestamp_(169957925).timezone_('Europe/London')

    dt.tz_('America/Toronto').in_timezone('America/Vancouver')

.. note::

    ``timezone_()`` and ``tz_()`` just modify the timezone information without
    making any conversion while ``in_timezone()`` converts the time in the
    appropriate timezone.
