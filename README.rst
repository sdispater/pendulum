Pendulum
########

.. image:: https://travis-ci.org/sdispater/pendulum.png
   :alt: Pendulum Build status
   :target: https://travis-ci.org/sdispater/pendulum

Python datetimes made easy.

Supports Python **2.7+** and **3.2+**.


.. code-block:: python

   >>> import pendulum

   >>> now_in_paris = pendulum.now('Europe/Paris')
   >>> now_in_paris
   '2016-07-04T00:49:58.502116+02:00'

   # Seamless timezone switching
   >>> now_in_paris.in_timezone('UTC')
   '2016-07-03T22:49:58.502116+00:00'

   >>> tomorrow = pendulum.now().add(days=1)
   >>> last_week = pendulum.now().subtract(weeks=1)

   >>> if pendulum.now().is_weekend():
   ...     print('Party!')
   'Party!'

   >>> past = pendulum.now().subtract(minutes=2)
   >>> past.diff_for_humans()
   >>> '2 minutes ago'

   >>> delta = past - last_week
   >>> delta.hours
   23
   >>> delta.in_words(locale='en')
   '6 days 23 hours 58 minutes'

   # Proper handling of datetime normalization
   >>> pendulum.create(2013, 3, 31, 2, 30, 0, 0, 'Europe/Paris')
   '2013-03-31T03:30:00+02:00' # 2:30 does not exist (Skipped time)

   # Proper handling of dst transitions
   >>> just_before = pendulum.create(2013, 3, 31, 1, 59, 59, 999999, 'Europe/Paris')
   '2013-03-31T01:59:59.999999+01:00'
   >>> just_before.add(microseconds=1)
   '2013-03-31T03:00:00+02:00'


Why Pendulum?
=============

Native ``datetime`` instances are enough for basic cases but when you face more complex use-cases
they often show limitations and are not so intuitive to work with.
``Pendulum`` provides a cleaner and more easy to use API while still relying on the standard library.
So it's still ``datetime`` but better.

Unlike other datetime libraries for Python, Pendulum is a drop-in replacement
for the standard ``datetime`` class (it inherits from it), so, basically, you can replace all your ``datetime``
instances by ``Pendulum`` instances in you code (exceptions exist for libraries that check
the type of the objects by using the ``type`` function like ``sqlite3`` or ``PyMySQL`` for instance).

It also removes the notion of naive datetimes: each ``Pendulum`` instance is timezone-aware
and by default in ``UTC`` for ease of use.

Pendulum also improves the standard ``timedelta`` class by providing more intuitive methods and properties.


Why not Arrow?
==============

Arrow is the most popular datetime library for Python right now, however its behavior
and API can be erratic and unpredictable. The ``get()`` method can receive pretty much anything
and it will try its best to return something while silently failing to handle some cases:

.. code-block:: python

    arrow.get('2016-1-17')
    # <Arrow [2016-01-01T00:00:00+00:00]>

    pendulum.parse('2016-1-17')
    # <Pendulum [2016-01-17T00:00:00+00:00]>

    # Parsing of a date with wrong day
    arrow.get('2015-06-31')
    # <Arrow [2015-06-01T00:00:00+00:00]>

    pendulum.parse('2016-06-31')
    # ValueError: day is out of range for month

    # fromtimestamp with timezone displays wrong offset
    arrow.Arrow.fromtimestamp(0, pytz.timezone('Europe/Paris'))
    # <Arrow [1970-01-01T01:00:00+00:09]>

    pendulum.from_timestamp(0, pytz.timezone('Europe/Paris'))
    # fromtimestamp() is also possible
    # <Pendulum [1970-01-01T01:00:00+01:00]>

    # Working with DST
    just_before = arrow.Arrow(2013, 3, 31, 1, 59, 59, 999999, 'Europe/Paris')
    just_after = just_before.replace(microseconds=1)
    '2013-03-31T02:00:00+02:00'
    # Should be 2013-03-31T03:00:00+02:00

    (just_after.to('utc') - just_before.to('utc')).total_seconds()
    -3599.999999
    # Should be 1e-06

    just_before = pendulum.create(2013, 3, 31, 1, 59, 59, 999999, 'Europe/Paris')
    just_after = just_before.add(microseconds=1)
    '2013-03-31T03:00:00+02:00'

    (just_after.in_timezone('utc') - just_before.in_timezone('utc')).total_seconds()
    1e-06

Those are a few examples showing that Arrow cannot always be trusted to have a consistent
behavior with the data you are passing to it.


Resources
=========

* `Official Website <http://pendulum.eustace.io>`_
* `Documentation <http://pendulum.eustace.io/docs/>`_
* `Issue Tracker <https://github.com/sdispater/pendulum/issues>`_


Contributing
============

Contributions are welcome, especially with localization.
Check the `languages <https://github.com/sdispater/pendulum/tree/master/pendulum/lang>`_ already supported,
and if you want to add a new one, take the `en <https://github.com/sdispater/pendulum/tree/master/pendulum/lang/en.py>`_
file as a starting point and add tests accordingly.
