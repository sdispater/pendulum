# Period

When you subtract a `DateTime` instance from another, or use the `diff()` method, it will return a `Period` instance.
It inherits from the [Duration](#duration) class with the added benefit that it is aware of the
instances that generated it, so that it can give access to more methods and properties:

```python
>>> import pendulum

>>> start = pendulum.datetime(2000, 11, 20)
>>> end = pendulum.datetime(2016, 11, 5)

>>> period = end - start

>>> period.years
15
>>> period.months
11
>>> period.in_years()
15
>>> period.in_months()
191

# Note that the weeks property
# will change compared to the Duration class
>>> period.weeks
2 # 832 for the duration

# However the days property will still remain the same
# to keep the compatiblity with the timedelta class
>>> period.days
5829
```

Be aware that a period, just like an interval, is compatible with the `timedelta` class regarding
its attributes. However, its custom attributes (like `remaining_days`) will be aware of any DST
transitions that might have occurred and adjust accordingly. Let's take an example:

```python
>>> import pendulum

>>> start = pendulum.datetime(2017, 3, 7, tz='America/Toronto')
>>> end = start.add(days=6)

>>> period = end - start

# timedelta properties
>>> period.days
5
>>> period.seconds
82800

# period properties
>>> period.remaining_days
6
>>> period.hours
0
>>> period.remaining_seconds
0
```

!!!warning

    Due to their nature (fixed duration between two datetimes), most arithmetic operations will
    return a `Duration` instead of a `Period`.

    ```python
    >>> import pendulum

    >>> dt1 = pendulum.datetime(2016, 8, 7, 12, 34, 56)
    >>> dt2 = dt1.add(days=6, seconds=34)
    >>> period = pendulum.period(dt1, dt2)
    >>> period * 2
    Duration(weeks=1, days=5, minutes=1, seconds=8)
    ```


## Instantiation

You can create an instance by using the `period()` helper:

```python

>>> import pendulum

>>> start = pendulum.datetime(2000, 1, 1)
>>> end = pendulum.datetime(2000, 1, 31)

>>> period = pendulum.period(start, end)
```

You can also make an inverted period:

```python
>>> period = pendulum.period(end, start)
>>> period.remaining_days
-2
```

If you have inverted dates but want to make sure that the period is positive,
you should set the `absolute` keyword argument to `True`:

```python
>>> period = pendulum.period(end, start, absolute=True)
>>> period.remaining_days
2
```

## Range

If you want to iterate over a period, you can use the `range()` method:

```python
>>> import pendulum

>>> start = pendulum.datetime(2000, 1, 1)
>>> end = pendulum.datetime(2000, 1, 10)

>>> period = pendulum.period(start, end)

>>> for dt in period.range('days'):
>>>     print(dt)

'2000-01-01T00:00:00+00:00'
'2000-01-02T00:00:00+00:00'
'2000-01-03T00:00:00+00:00'
'2000-01-04T00:00:00+00:00'
'2000-01-05T00:00:00+00:00'
'2000-01-06T00:00:00+00:00'
'2000-01-07T00:00:00+00:00'
'2000-01-08T00:00:00+00:00'
'2000-01-09T00:00:00+00:00'
'2000-01-10T00:00:00+00:00'
```

!!!note

    Supported units for `range()` are: `years`, `months`, `weeks`,
    `days`, `hours`, `minutes` and `seconds`

You can pass an amount for the passed unit to control the length of the gap:

```python
>>> for dt in period.range('days', 2):
>>>     print(dt)

'2000-01-01T00:00:00+00:00'
'2000-01-03T00:00:00+00:00'
'2000-01-05T00:00:00+00:00'
'2000-01-07T00:00:00+00:00'
'2000-01-09T00:00:00+00:00'
```

You can also directly iterate over the `Period` instance,
the unit will be `days` in this case:

```python
>>> for dt in period:
>>>     print(dt)
```

You can check if a `DateTime` instance is inside a period using the `in` keyword:

```python
>>> dt = pendulum.datetime(2000, 1, 4)
>>> dt in period
True
```
