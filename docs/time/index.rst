Time
====

The ``Time`` class is a drop-in replacement for the native ``time``
class (it is inherited from it).


Instantiation
-------------

There are several different methods available to create a new ``Time`` object.
First there is a constructor. It accepts the same parameters as the standard class.

.. code-block:: python

    from pendulum import Time

    t = Time(19, 48, 57)
    isinstance(t, time)
    True

You can also get the current time by using the ``now()`` method:

.. code-block:: python

    t = Time.now()
    print(t)
    '19:48:57.025226'

    # To exclude the microseconds, pass False
    # as the first argument
    t = Time.now(False)
    print(t)
    '19:48:57'

Finally, if you find yourself inheriting a ``time`` instance,
you can create a ``Time`` instance via the ``instance()`` method.

.. code-block:: python

    t1 = time(19, 48, 57)
    t = Time.instance(t1)
    print(t)
    '19:48:57'


Localization
------------

Localization occurs when using the ``format()`` method.

.. code-block:: python

    from pendulum import Time

    t = Time(19, 48, 57)

    t.format('%H:%M:%S')
    '19:48:57'

``diff_for_humans()`` is localized, you can set the locale globally
by using the ``pendulum.set_locale()``.

.. code-block:: python

    import pendulum
    from pendulum import Time

    pendulum.set_locale('de')
    print(Time.now().add(hours=1).diff_for_humans())
    'in 1 Stunde'

    pendulum.set_locale('en')

However, you might not want to set the locale globally.
The ``diff_for_humans()`` method accept a ``locale`` keyword argument to use a locale for a specific call.

.. code-block:: python

    pendulum.set_locale('de')
    print(Time.now().add(years=1).diff_for_humans(locale='fr'))
    'dans 1 heure'


Attributes and Properties
-------------------------

Pendulum gives access to more attributes and properties than the default ``time`` class.

.. code-block:: python

    from pendulum import Time

    t = Time(19, 48, 57, 123456)

    # These properties specifically return integers
    t.hour
    19
    t.minute
    48
    t.second
    57
    t.microsecond
    123456


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
