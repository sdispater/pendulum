String Formatting
=================

All the ``to_xxx_string()`` methods rely on the native ``datetime.strftime()`` with additional
directives available.
The ``__str__`` magic method is defined which allows ``Pendulum`` instances to be printed
as a pretty date string when used in a string context.
The default string representation is the same as the one returned by the ``isoformat()`` method.

.. code-block:: python

    from pendulum import Pendulum

    dt = Pendulum(1975, 12, 25, 14, 15, 16)

    print(dt)
    '1975-12-25T14:15:16+00:00'

    dt.to_date_string()
    '1975-12-25'

    dt.to_formatted_date_string()
    'Dec 25, 1975'

    dt.to_time_string()
    '14:15:16'

    dt.to_datetime_string()
    '1975-12-25 14:15:16'

    dt.to_day_datetime_string()
    'Thu, Dec 25, 1975 2:15 PM'

    # You can also use the format() method
    dt.format('%A %-d%t of %B %Y %I:%M:%S %p')
    'Thursday 25th of December 1975 02:15:16 PM'

    # Of course, the strftime method is still available
    dt.strftime('%A %-d%t of %B %Y %I:%M:%S %p')
    'Thursday 25th of December 1975 02:15:16 PM'

You can also set the default ``__str__`` format.

.. code-block:: python

    import pendulum

    pendulum.set_to_string_format('%-d%t of %B, %Y %-I:%M:%S %p')

    print(dt)
    '25th of December, 1975 2:15:16 PM'

    pendulum.reset_to_string_format()
    print(dt)
    '25th of December, 1975 2:15:16 PM'

.. note::

    For localization support see the `Localization`_ section.

.. warning::

    Even if you have set the default formatter to the alternative one (See `Alternative Formatter`_),
    the ``__str__`` format must still be in the default format (ie the standard Python format).

Custom Directives
-----------------

Apart from the `default directives <https://docs.python.org/3.5/library/time.html#time.strftime>`_,
Pendulum comes with its own (each custom directive is in the form ``%_{directive}``):

===========  ======================================================================== =================================
Directive    Meaning                                                                  Example
===========  ======================================================================== =================================
``%_z``      Difference to Greenwich time (GMT) with colon between hours and minutes  ``+02:00``
``%_t``      Ordinal suffix for the day of the month, 2 characters                    ``st``, ``nd``, ``rd`` or ``th``
===========  ======================================================================== =================================

Common Formats
--------------

The following are methods to display a ``Pendulum`` instance as a common format:

.. code-block:: python

    import pendulum

    dt = pendulum.now()

    dt.to_atom_string()
    '1975-12-25T14:15:16-05:00'

    dt.to_cookie_string()
    'Thursday, 25-Dec-1975 14:15:16 EST'

    dt.to_iso8601_string()
    '1975-12-25T14:15:16-0500'

    dt.to_rfc822_string()
    'Thu, 25 Dec 75 14:15:16 -0500'

    dt.to_rfc850_string()
    'Thursday, 25-Dec-75 14:15:16 EST'

    dt.to_rfc1036_string()
    'Thu, 25 Dec 75 14:15:16 -0500'

    dt.to_rfc1123_string()
    'Thu, 25 Dec 1975 14:15:16 -0500'

    dt.to_rfc2822_string()
    'Thu, 25 Dec 1975 14:15:16 -0500'

    dt.to_rfc3339_string()
    '1975-12-25T14:15:16-05:00'

    dt.to_rss_string()
    'Thu, 25 Dec 1975 14:15:16 -0500'

    dt.to_w3c_string()
    '1975-12-25T14:15:16-05:00'

Alternative formatter
---------------------

Pendulum supports an alternative format when using the ``format()`` method.
This format is more intuitive to use than the default one and supports more
directives.
You can use this format either locally when calling the ``format()`` method
or globally by using ``pendulum.set_formatter()``.

.. code-block:: python

    import pendulum

    dt = pendulum.Pendulum(1975, 12, 25, 14, 15, 16)
    dt.format('YYYY-MM-DD HH:mm:ss', formatter='alternative')
    '1975-12-25 14:15:16'

    pendulum.set_formatter('alternative')
    dt.format('YYYY-MM-DD HH:mm:ss')
    '1975-12-25 14:15:16'

    # Reset to default formatter
    pendulum.set_formatter()

Tokens
~~~~~~

The following tokens are currently supported:


+--------------------------------+--------------+-------------------------------------------+
|                                |Token         |Output                                     |
+================================+==============+===========================================+
|**Year**                        |YYYY          |2000, 2001, 2002 ... 2012, 2013            |
+--------------------------------+--------------+-------------------------------------------+
|                                |YY            |00, 01, 02 ... 12, 13                      |
+--------------------------------+--------------+-------------------------------------------+
|**Quarter**                     |Q             |1 2 3 4                                    |
+--------------------------------+--------------+-------------------------------------------+
|                                |Qo            |1st 2nd 3rd 4th                            |
+--------------------------------+--------------+-------------------------------------------+
|**Month**                       |MMMM          |January, February, March ...               |
+--------------------------------+--------------+-------------------------------------------+
|                                |MMM           |Jan, Feb, Mar ...                          |
+--------------------------------+--------------+-------------------------------------------+
|                                |MM            |01, 02, 03 ... 11, 12                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |M             |1, 2, 3 ... 11, 12                         |
+--------------------------------+--------------+-------------------------------------------+
|                                |Mo            |1st 2nd ... 11th 12th                      |
+--------------------------------+--------------+-------------------------------------------+
|**Day of Year**                 |DDDD          |001, 002, 003 ... 364, 365                 |
+--------------------------------+--------------+-------------------------------------------+
|                                |DDD           |1, 2, 3 ... 4, 5                           |
+--------------------------------+--------------+-------------------------------------------+
|**Day of Month**                |DD            |01, 02, 03 ... 30, 31                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |D             |1, 2, 3 ... 30, 31                         |
+--------------------------------+--------------+-------------------------------------------+
|                                |Do            |1st, 2nd, 3rd ... 30th, 31st               |
+--------------------------------+--------------+-------------------------------------------+
|**Day of Week**                 |dddd          |Monday, Tuesday, Wednesday ...             |
+--------------------------------+--------------+-------------------------------------------+
|                                |ddd           |Mon, Tue, Wed ...                          |
+--------------------------------+--------------+-------------------------------------------+
|                                |d             |1, 2, 3 ... 6, 7                           |
+--------------------------------+--------------+-------------------------------------------+
|**Hour**                        |HH            |00, 01, 02 ... 23, 24                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |H             |0, 1, 2 ... 23, 24                         |
+--------------------------------+--------------+-------------------------------------------+
|                                |hh            |01, 02, 03 ... 11, 12                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |h             |1, 2, 3 ... 11, 12                         |
+--------------------------------+--------------+-------------------------------------------+
|**Minute**                      |mm            |00, 01, 02 ... 58, 59                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |m             |0, 1, 2 ... 58, 59                         |
+--------------------------------+--------------+-------------------------------------------+
|**Second**                      |ss            |00, 01, 02 ... 58, 59                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |s             |0, 1, 2 ... 58, 59                         |
+--------------------------------+--------------+-------------------------------------------+
|**Fractional Second**           |S             |0 1 ... 8 9                                |
+--------------------------------+--------------+-------------------------------------------+
|                                |SS            |00, 01, 02 ... 98, 99                      |
+--------------------------------+--------------+-------------------------------------------+
|                                |SSS           |000 001 ... 998 999                        |
+--------------------------------+--------------+-------------------------------------------+
|                                |SSSS ...      |000[0..] 001[0..] ... 998[0..] 999[0..]    |
|                                |SSSSSS        |                                           |
+--------------------------------+--------------+-------------------------------------------+
|**AM / PM**                     |A             |AM, PM                                     |
+--------------------------------+--------------+-------------------------------------------+
|**Timezone**                    |ZZ            |-07:00, -06:00 ... +06:00, +07:00          |
+--------------------------------+--------------+-------------------------------------------+
|                                |Z             |-0700, -0600 ... +0600, +0700              |
+--------------------------------+--------------+-------------------------------------------+
|                                |zz            |Asia/Baku, Europe/Warsaw, GMT ...          |
+--------------------------------+--------------+-------------------------------------------+
|                                |z             |EST CST ... MST PST                        |
+--------------------------------+--------------+-------------------------------------------+
|**Timestamp**                   |X             |1381685817                                 |
+--------------------------------+--------------+-------------------------------------------+

Localized Formats
~~~~~~~~~~~~~~~~~

Because preferred formatting differs based on locale,
there are a few tokens that can be used to format an instance based on its locale.

+--------------------------------------------+--------------+-------------------------------------------+
|**Time**                                    |LT            |8:30 PM                                    |
+--------------------------------------------+--------------+-------------------------------------------+
|**Time with seconds**                       |LTS           |8:30:25 PM                                 |
+--------------------------------------------+--------------+-------------------------------------------+
|**Month numeral, day of month, year**       |L             |09/04/1986                                 |
+--------------------------------------------+--------------+-------------------------------------------+
|**Month name, day of month, year**          |LL            |September 4 1986                           |
+--------------------------------------------+--------------+-------------------------------------------+
|**Month name, day of month, year, time**    |LLL           |September 4 1986 8:30 PM                   |
+--------------------------------------------+--------------+-------------------------------------------+
|**Month name, day of month, day of week,**  |LLLL          |Thursday, September 4 1986 8:30 PM         |
|**year, time**                              |              |                                           |
+--------------------------------------------+--------------+-------------------------------------------+

Escaping Characters
~~~~~~~~~~~~~~~~~~~

To escape characters in format strings, you can wrap the characters in square brackets.

.. code-block:: python

    import pendulum

    pendulum.now().format('[today] dddd', formatter='alternative')
    'today Sunday'
