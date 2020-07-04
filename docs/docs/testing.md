# Testing

The testing methods allow you to set a `DateTime` instance (real or mock) to be returned
when a "now" instance is created.
The provided instance will be returned specifically under the following conditions:

* A call to the `now()` method, ex. `pendulum.now()`.
* When the string "now" is passed to the `parse()` method, ex. `pendulum.parse('now')`

```python
>>> import pendulum

# Create testing datetime
>>> known = pendulum.datetime(2001, 5, 21, 12)

# Set the mock
>>> pendulum.set_test_now(known)

>>> print(pendulum.now())
'2001-05-21T12:00:00+00:00'

>>> print(pendulum.parse('now'))
'2001-05-21T12:00:00+00:00'

# Clear the mock
>>> pendulum.set_test_now()

>>> print(pendulum.now())
'2016-07-10T22:10:33.954851-05:00'
```

Related methods will also return values mocked according to the **now** instance.

```python
>>> print(pendulum.today())
'2001-05-21T00:00:00+00:00'

>>> print(pendulum.tomorrow())
'2001-05-22T00:00:00+00:00'

>>> print(pendulum.yesterday())
'2001-05-20T00:00:00+00:00'
```

If you don't want to manually clear the mock (or you are afraid of forgetting),
you can use the provided `test()` contextmanager.

```python
>>> import pendulum

>>> known = pendulum.datetime(2001, 5, 21, 12)

>>> with pendulum.test(known):
>>>     print(pendulum.now())
'2001-05-21T12:00:00+00:00'

>>> print(pendulum.now())
'2016-07-10T22:10:33.954851-05:00'
```
