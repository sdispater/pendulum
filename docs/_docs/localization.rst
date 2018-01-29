.. _Localization:

Localization
============

Localization occurs when using the ``format()`` method which accepts a ``locale`` keyword.

.. code-block:: python

    import pendulum

    dt = pendulum.create(1975, 5, 21)

    dt.format('dddd DD MMMM YYYY', locale='de')
    'Mittwoch 21 Mai 1975'

    dt.format('dddd DD MMMM YYYY')
    'Wednesday 21 May 1975'

.. note::

    You can also use the ``strftime()`` method, which behaves exactly like the native one.

    .. code-block:: python

        import locale
        from pendulum import Pendulum

        dt = Pendulum(1975, 5, 21)

        locale.setlocale(locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8'))
        dt.format('%A %d %B %Y')
        'Mittwoch 21 Mai 1975'

        locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
        dt.format('%A %d %B %Y')
        'Wednesday 21 May 1975'

``diff_for_humans()`` is also localized, you can set the locale
by using ``pendulum.set_locale()``.

.. code-block:: python

    import pendulum

    pendulum.set_locale('de')
    print(pendulum.now().add(years=1).diff_for_humans())
    'in 1 Jahr'

    pendulum.set_locale('en')

However, you might not want to set the locale globally. The ``diff_for_humans()``
method accept a ``locale`` keyword argument to use a locale for a specific call.

.. code-block:: python

    pendulum.set_locale('de')
    dt = pendulum.now().add(years=1)
    print(dt.diff_for_humans(locale='fr'))
    'dans 1 an'
