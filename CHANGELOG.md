### 0.5.3

(August 29th, 2016)

- [Fix] Fixes setters and modifiers (start_of/end_of) to properly apply DST transitions.
- [Fix] Fixes timezone file loading on some installs (See [#34](https://github.com/sdispater/pendulum/issues/34))
(Thanks to [mayfield](https://github.com/mayfield))

### 0.5.2

(August 22nd, 2016)

- [Fix] Fixes `TimezoneInfo.utcoffset()` method.
- [Fix] Fixes arithmetic operations on intervals not returning intervals.
- [Fix] Allows Pendulum instances comparison to None . (Thanks to [jkeyes](https://github.com/jkeyes))
- [Feature] Adds a small speedup when changing timezones.
- [Feature] Makes .offset_hours return a float. 


### 0.5.1

(August 18th, 2016)

- [Fix] Fixes `now()` not behaving properly when given a timezone.
- [Fix] Fixes double file opening when getting local timezone. (Thanks to [yggdr](https://github.com/yggdr))
- [Fix] Fixes `pt_BR` locale. (Thanks to [YomoFuno](https://github.com/YomoFuno))
- [Fix] Fixes `pl` locale. (Thanks to [MichalTHEDUDE](https://github.com/MichalTHEDUDE))


### 0.5

(August 15th, 2016)

This version introduces a new timezone library which improves
timezone switching and behavior around DST transition times.

- Adds a new timezone library to properly normalize and localize datetimes.
``Pendulum`` no longer relies on ``pytz``.
Check the [Documentation](/docs/#timezone) to see what has changed exactly.


### 0.4

(July 26th, 2016)

This version mostly brings the new ``Period`` class and improves performances overall.

- Adds the `Period` class, which basically is a datetime-aware interval.
- Makes the `format()` method support a `locale` keyword argument.
- Changes custom directives. `%P` becomes `%_z` and `%t` becomes `%_t`.
Basically, all new custom directives will be in the form `%_{directive}`
- Fixes singular for negative values of intervals.

### 0.3.1

(July 13th, 2016)

- Fixes parsing of string with partial offset.


### 0.3

(July 11th, 2016)

This version causes major breaking API changes to simplify it and making it more intuitive.

- Improves testing by providing a `test()` contextmanager.
- Makes passing a naive `datetime` to `instance()` default to `UTC`.
- Reduces `add_xxx()`/`sub_xxx()` methods to `add(**kwargs)`/`subtract(**kwargs)`.
- Changes the `for_humans()` method of the `Interval` class to `in_words()` to avoid confusion with the `diff_for_humans()` method.
- Makes more constants and methods available at module level.
- Makes the constructor behave like the standard one. No more `Pendulum()`.
- Fixes "sl" locale.
- Renames the `to()` method to `in_timezone()`.
- Removes the comparison methods to just stick with the basic operators.
- Reduces `first_of_xxx()`/`last_of_xxx()`/`nth_of_xxx()` methods to `first_of(unit)`/`last_of(unit)`/`nth_of(unit, nth)`.
- Reduces `start_of_xxx()`/`end_of_xxx()` methods to `start_of(unit)`/`end_of(unit)`.
- Removes the `diff_in_xxx()` methods from the `Pendulum` and adds `in_xxx()` methods to the `Interval` class.
- Renames the `PendulumInterval` class to simply `Interval`.
- Makes the `Pendulum` class immutable.


### 0.2

(July 4th, 2016)

- Makes the `Pendulum` class truly inherits from `datetime`


### 0.1.1

(July 4th, 2016)

- Adds support for the `TZ` environment variable
- Adds `closest()`/`farthest()` comparison methods
- Makes `set_test_now()` available at module level
- Adds min/max attributes. Renames min/max methods.
- Fixes `diff_for_humans()` method when setting locale.


### 0.1

(July 4th, 2016)

- Initial release
