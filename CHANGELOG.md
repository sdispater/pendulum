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
