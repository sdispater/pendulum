# Comparison

Simple comparison is offered up via the basic operators.
Remember that the comparison is done in the UTC timezone
so things aren't always as they seem.

```python
>>> import pendulum

>>> first = pendulum.datetime(2012, 9, 5, 23, 26, 11, 0, tz='America/Toronto')
>>> second = pendulum.datetime(2012, 9, 5, 20, 26, 11, 0, tz='America/Vancouver')

>>> first.to_datetime_string()
'2012-09-05 23:26:11'
>>> first.timezone_name
'America/Toronto'
>>> second.to_datetime_string()
'2012-09-05 20:26:11'
>>> second.timezone_name
'America/Vancouver'

>>> first == second
True
>>> first != second
False
>>> first > second
False
>>> first >= second
True
>>> first < second
False
>>> first <= second
True

>>> first = first.on(2012, 1, 1).at(0, 0, 0)
>>> second = second.on(2012, 1, 1).at(0, 0, 0)
# tz is still America/Vancouver for second

>>> first == second
False
>>> first != second
True
>>> first > second
False
>>> first >= second
False
>>> first < second
True
>>> first <= second
True
```

To handle the most used cases there are some simple helper functions.
For the methods that compare to `now()` (ex. `is_today()`) in some manner
the `now()` is created in the same timezone as the instance.

```python
>>> import pendulum

>>> dt = pendulum.now()

>>> dt.is_past()
>>> dt.is_leap_year()

>>> born = pendulum.datetime(1987, 4, 23)
>>> not_birthday = pendulum.datetime(2014, 9, 26)
>>> birthday = pendulum.datetime(2014, 4, 23)
>>> past_birthday = pendulum.now().subtract(years=50)

>>> born.is_birthday(not_birthday)
False
>>> born.is_birthday(birthday)
True
>>> past_birthday.is_birthday()
# Compares to now by default
True
```
