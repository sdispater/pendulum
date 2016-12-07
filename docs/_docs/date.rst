Date
====

The ``Date`` class is a drop-in replacement for the native ``date``
class (it is inherited from it).

It shares a lot of methods and attributes with the ``Pendulum`` class.


Instantiation
-------------

There are several different methods available to create a new ``Date`` object.
First there is a constructor. It accepts the same parameters as the standard class.

.. code-block:: python

    from pendulum import Date

    dt = Date(2016, 11, 26)
    isinstance(dt, date)
    True

You can also create known instances by using the corresponding methods:

.. code-block:: python

    today = Date.today()
    print(today)
    '2016-11-26'

    tomorrow = Date.tomorrow()
    print(tomorrow)
    '2016-11-27'

    yesterday = Date.yesterday()
    print(yesterday)
    '2016-11-25'

Next there is the ``create()`` helper.

You can provide as many or as few arguments as you want and the helper will provide default values for all others.
Generally default values are the current date.

.. code-block:: python

    Date.create()
    '2016-11-26'

    Date.create(2015)
    '2015-11-26'

    Date.create(2015, 10, 11)
    '2015-10-11'

Finally, if you find yourself inheriting a ``date`` instance,
you can create a ``Date`` instance via the ``instance()`` method.

.. code-block:: python

    dt = date(2016, 11, 26)
    d = Date.instance(dt)
    print(d)
    '2016-11-26'


Localization
------------

Localization occurs when using the ``format()`` method which accepts a ``locale`` keyword.

.. code-block:: python

    from pendulum import Date

    dt = Date(1975, 5, 21)

    dt.format('%A %d %B %Y', locale='de')
    'Mittwoch 21 Mai 1975'

    dt.format('%A %d %B %Y')
    'Wednesday 21 May 1975'

``diff_for_humans()`` is also localized, you can set the locale globally
by using the ``pendulum.set_locale()``.

.. code-block:: python

    import pendulum
    from pendulum import Date

    pendulum.set_locale('de')
    print(Date.today().add(years=1).diff_for_humans())
    'in 1 Jahr'

    pendulum.set_locale('en')

However, you might not want to set the locale globally.
The ``diff_for_humans()`` method accept a ``locale`` keyword argument to use a locale for a specific call.

.. code-block:: python

    pendulum.set_locale('de')
    print(Date.today().add(years=1).diff_for_humans(locale='fr'))
    'dans 1 an'


Attributes and Properties
-------------------------

Pendulum gives access to more attributes and properties than the default ``date`` class.

.. code-block:: python

    from pendulum import Date

    dt = Date(2012, 9, 5)

    # These properties specifically return integers
    dt.year
    2012
    dt.month
    9
    dt.day
    5
    dt.day_of_week
    3
    dt.day_of_year
    248
    dt.week_of_month
    1
    dt.week_of_year
    36
    dt.days_in_month
    30
    dt.quarter
    3


Comparison
----------

You can refer to the corresponding `section <#comparison>`_ of the documentation.


Addition and Subtraction
------------------------

You can refer to the corresponding `section <#addition-and-subtraction>`_ of the documentation.


Difference
----------

You can refer to the corresponding `section <#difference>`_ of the documentation.


Modifiers
---------

You can refer to the corresponding `section <#modifiers>`_ of the documentation.
