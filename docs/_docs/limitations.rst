Limitations
===========

Even though the ``Pendulum`` class is a subclass of ``datetime`` there are some rare cases where
it can't replace the native class directly. Here is a list (non-exhaustive) of the reported cases with
a possible solution, if any:

* ``sqlite3`` will use the the ``type()`` function to determine the type of the object by default. To work around it you can register a new adapter:

.. code-block:: python

    from pendulum import Pendulum
    from sqlite3 import register_adapter

    register_adapter(Pendulum, lambda val: val.isoformat(' '))

* ``mysqlclient`` (former ``MySQLdb``) and ``PyMySQL`` will use the the ``type()`` function to determine the type of the object by default. To work around it you can register a new adapter:

.. code-block:: python

    import MySQLdb.converters
    import pymysql.converters

    from pendulum import Pendulum

    MySQLdb.converters.conversions[Pendulum] = MySQLdb.converters.DateTime2literal
    pymysql.converters.conversions[Pendulum] = pymysql.converters.escape_datetime

* ``django`` will use the ``isoformat()`` method to store datetimes in the database. However since ``pendulum`` is always timezone aware the offset information will always be returned by ``isoformat()`` raising an error, at least for MySQL databases. To work around it you can either create your own ``DateTimeField`` or use the previous workaround for ``MySQLdb``:

.. code-block:: python

    from django.db.models import DateTimeField as BaseDateTimeField
    from pendulum import Pendulum


    class DateTimeField(BaseDateTimeField):

        def value_to_string(self, obj):
            val = self.value_from_object(obj)

            if isinstance(value, Pendulum):
                return value.to_datetime_string()

            return '' if val is None else val.isoformat()
