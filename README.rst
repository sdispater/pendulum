Pendulum
########

.. image:: https://travis-ci.org/sdispater/pendulum.png
   :alt: Orator Build status
   :target: https://travis-ci.org/sdispater/pendulum

Python datetimes made easy.

.. code-block:: python

    import pendulum

    now_in_paris = pendulum.now('Europe/Paris')
    '2016-07-04T00:49:58.502116+02:00'
    now_in_paris.to('UTC')
    '2016-07-03T22:49:58.502116+00:00'

    tomorrow = pendulum.now().add_day()
    last_week = pendulum.now().sub_week()

    if pendulum.now().is_weekend():
        print('Party!')

    past = pendulum.now().sub_minutes(2)
    past.diff_for_humans()
    '2 minutes ago'

    delta = past - last_week
    delta.hours
    23
    delta.for_humans(locale='fr')
    '6 jours 23 heures 58 minutes'

Resources
=========

* `Official Website <http://pendulum.eustace.io>`_
* `Documentation <http://pendulum.eustace.io/docs/>`_
* `Issue Tracker <https://github.com/sdispater/pendulum/issues>`_
