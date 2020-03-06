# Introduction

Pendulum is a Python package to ease datetimes manipulation.

It provides classes that are drop-in replacements for the native ones (they inherit from them).

Special care has been taken to ensure timezones are handled correctly,
and are based on the underlying `tzinfo` implementation.
For example, all comparisons are done in `UTC` or in the timezone of the datetime being used.

```python
>>> import pendulum

>>> dt_toronto = pendulum.datetime(2012, 1, 1, tz='America/Toronto')
>>> dt_vancouver = pendulum.datetime(2012, 1, 1, tz='America/Vancouver')

>>> print(dt_vancouver.diff(dt_toronto).in_hours())
3
```

The default timezone, except when using the `now()`, method will always be `UTC`.
