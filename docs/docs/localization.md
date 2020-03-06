# Localization

Localization occurs when using the `format()` method which accepts a `locale` keyword.

```python
>>> import pendulum

>>> dt = pendulum.datetime(1975, 5, 21)
>>> dt.format('dddd DD MMMM YYYY', locale='de')
'Mittwoch 21 Mai 1975'

>>> dt.format('dddd DD MMMM YYYY')
'Wednesday 21 May 1975'
```

`diff_for_humans()` is also localized, you can set the locale
by using `pendulum.set_locale()`.

```python
>>> import pendulum

>>> pendulum.set_locale('de')
>>> pendulum.now().add(years=1).diff_for_humans()
'in 1 Jahr'
>>> pendulum.set_locale('en')
```

However, you might not want to set the locale globally. The `diff_for_humans()`
method accepts a `locale` keyword argument to use a locale for a specific call.

```python
>>> pendulum.set_locale('de')
>>> dt = pendulum.now().add(years=1)
>>> dt.diff_for_humans(locale='fr')
'dans 1 an'
```
