# Change Log

## [1.2.4] - 2017-06-20

### Fixed

- Fixed parsing of the `now` string.


## [1.2.3] - 2017-06-18

### Fixed

- Fixed behavior of some short timezones (like EST, MST or HST).
- Fixed warning when building C extensions.


## [1.2.2] - 2017-06-15

### Fixed

- Fixed `next()` and `previous()` hanging when passed an invalid input.
- Fixed wrong result when adding/subtracting a Period if a DST transition occurs.


## [1.2.1] - 2017-05-23

### Fixed

- Fixed incorrect `fold` attribute on Python 3.6 when not passing a timezone. (Thanks to [neonquill](https://github.com/neonquill))


## [1.2.0] - 2017-03-24

### Added

- Added support for EXIF-formatted strings in parser. (Thanks to [emattiza](https://github.com/emattiza))

### Changed

- Improved performances when parsing ISO 8601 string with C extensions.

### Fixed

- Fixed parsing of ISO 8601 week dates.
- Fixed `eu` and `sk` locales. (Thanks to [eumiro](https://github.com/eumiro))


## [1.1.1] - 2017-03-14

### Fixed

- Fixed `diff_for_humans()` when crossing DST transitions.


## [1.1.0] - 2017-02-20

### Added

- Added the `keep_time` keyword argument to `next()`/`previous()` methods to keep time information.

### Changed

- Greatly improved `diff()` performance.
- Improved `diff_for_humans()` method to display more intuitive strings on edge cases.
- Formatting (with f-strings or `format()`) will now use the configured formatter.


## [1.0.2] - 2017-02-04

### Changed

- Adds support for external tzinfo as timezones. (Thanks to [iv597](https://github.com/iv597))

### Fixed

- Fixed `day_of_year` not returning the correct value. (Thanks to [asrenzo](https://github.com/asrenzo))


## [1.0.1] - 2017-01-25

### Fixed

- Fixed parsing, especially for strings in the form `31-01-01`.


## [1.0.0] - 2017-01-17

### Changed

- Using `PRE_TRANSITION` rule no longer produces a time in a DST gap.
- Improved performances when adding time to a `Pendulum` instance.
- Improved parsing of ISO 8601 strings.
- Removed deprecated methods


## [0.8.0] - 2016-12-23

### Added

- Added `on()` and `at()` methods which replace `with_date()` and `with_time()`.
- Added a `strict` keyword argument to `parse()` to get the type matching the parsed string.
- Added the ability to pass an amount to the `range()` method to control the length of the gap.
- Added a `datetime()` helper method to the `Timezone` class.

### Changed

- Improved parsing of ISO 8601 strings.

### Deprecated

- `with_date()` and `with_time()` are deprecated. Use `on()` and `at()` instead.
- `create_from_date()` and `create_from_time()` are deprecated. Use `create()` instead.


## [0.7.0] - 2016-12-07

### Added

- Added a `Date` class.
- Added a `Time` class.
- Added experimental support for the `fold` attribute introduced in Python 3.6.
- Added a `remaining_days` property to the `Interval` class.
- Added a `int_timestamp` property to the `Pendulum` class to retrieve the behavior of the now deprecated `timestamp` property.
- `start_of()`/`end_of()` now supports `hour`, `minute` and `second` units.
- `astimezone()` now supports timezone strings.
- `in_words()` now displays subseconds when no other units are available.

### Changed

- `Period` properties (especially `years` and `months`) are now accurate.
- `Interval.seconds` now returns the whole number of remaining seconds, like `timedelta`, for compatibility. Use `remaining_seconds` to retrieve the previous behavior.
- Improved parsing performances for common formats.
- The library no longer relies on `pytz`. It now depends on [pytzdata](https://github.com/sdispater/pytzdata) for its timezone database.
- Locale, test instance and formatter are now set gobally at the module level when using the corresponding module methods.

### Deprecated

- `timestamp` should now be used as a method and no longer as a property. It will be a native method in the next major version.
- `Interval` properties and methods related to years and months are now deprecated.
- `Interval.days_exclude_weeks` is now deprecated. Use `remaining_days` instead.

### Fixed

- Exception when loading specific timezones has been fixed.
- `end_of('day')` now properly sets microseconds to `999999`.
- Accuracy of `Period` instances properties has been improved.
- Accuracy for microseconds when initializing a Pendulum instance in some timezones has been fixed.
- Periods are now serializable with `pickle`.
- Fixed `minute_()`, `second_()` and `microsecond_()` setters changing the hour unit.
- Fixed Windows support.


## [0.6.6] - 2016-11-25

### Fixed

- Fixed a memory leak in C extension. (thanks to [ntoll](https://github.com/ntoll))


## [0.6.5] - 2016-10-31

### Changed

- Adds validation to `set_week_starts_at()`, `set_week_ends_at()` and `set_weekend_days()`. (thanks to [kleschenko](https://github.com/kleschenko))
- Updates ukrainian localization. (thanks to [kleschenko](https://github.com/kleschenko))

### Fixed

- Fixes loading of timezones without transitions.
- Fixes `Timezone.utcoffset()`. (thanks to [regnarock](https://github.com/regnarock))


## [0.6.4] - 2016-10-22

### Changed

- Adds support for `pytz` timezones in constructor.

### Fixed

- Fixes behavior of `add()`/`subtract()` methods for years, months and days when a DST transition occurs.
- Fixes `range()` behavior.


## [0.6.3] - 2016-10-19

### Changed

- Makes `replace()` accept the same tzinfo types as the constructor.

### Fixed

- Fixes `timezone_()` not setting the tzinfo properly.
- Fixes pickling/unpickling of Pendulum instances with fixed timezone.


## [0.6.2] - 2016-09-26

### Fixed

- Fixes timezones loading on Windows


## [0.6.1] - 2016-09-19

### Changed

- `Pendulum` instances can no longer be compared to strings and integers.

### Fixed

- Fixes `Timezone._convert()` method for fixed timezones.
- Fixes `instances()` for some `tzinfo`.
- Fixes comparisons to incompatible objects raising an error.


## [0.6.0] - 2016-09-12

### Added

- Adds an option to control transition normalization behavior.
- Adds a separator keyword argument to `Interval.in_words()` method.
- Adds an alternative formatter.
- Adds support for pretty much any `tzinfo` instance in the `instance()` method.
- Adds an `intersect()` method to the `Period` class.

### Changed

- Improves meridians formatting by supporting minutes.
- Changes behavior of `create*()` methods (time now defaults to `00:00:00`)

### Fixed

- Fixes setters and modifiers (start_of/end_of) to properly apply transitions.
- Fixes issue when compiling on 32 bit systems. (Thanks to [guyzmo](https://github.com/guyzmo))
- Fixes NameError Exception on Python 3.2. (Thanks to [guyzmo](https://github.com/guyzmo))
- Fixes absolute intervals.


## [0.5.5] - 2016-09-01

### Fixed

- Fixes local timezone loading for unix systems.
- Fixes potential `AttributeError` in `between` method. (Thanks to [iv597](https://github.com/iv597))


## [0.5.4] - 2016-08-30

### Fixed

- Fixes broken previous release.


## [0.5.3] - 2016-08-29

### Fixed

- Fixes setters and modifiers (start_of/end_of) to properly apply DST transitions.
- Fixes timezone file loading on some installs (See [#34](https://github.com/sdispater/pendulum/issues/34))
(Thanks to [mayfield](https://github.com/mayfield))


## [0.5.2] - 2016-08-22

### Added

- Adds a small speedup when changing timezones.

### Changed

- Makes `.offset_hours` return a float. 

### Fixed

- Fixes `TimezoneInfo.utcoffset()` method.
- Fixes arithmetic operations on intervals not returning intervals.
- Allows Pendulum instances comparison to None . (Thanks to [jkeyes](https://github.com/jkeyes))


## [0.5.1] - 2016-08-18

### Fixed

- Fixes `now()` not behaving properly when given a timezone.
- Fixes double file opening when getting local timezone. (Thanks to [yggdr](https://github.com/yggdr))
- Fixes `pt_BR` locale. (Thanks to [YomoFuno](https://github.com/YomoFuno))
- Fixes `pl` locale. (Thanks to [MichalTHEDUDE](https://github.com/MichalTHEDUDE))


## [0.5] - 2016-08-15

This version introduces a new timezone library which improves
timezone switching and behavior around DST transition times.

### Added

- Adds a new timezone library to properly normalize and localize datetimes.
``Pendulum`` no longer relies on ``pytz``.
Check the [Documentation](https://pendulum.eustace.io/docs/#timezones) to see what has changed exactly.


## [0.4] - 2016-07-26

This version mostly brings the new ``Period`` class and improves performances overall.

### Added

- Adds the `Period` class, which basically is a datetime-aware interval.

### Changed

- Makes the `format()` method support a `locale` keyword argument.
- Changes custom directives. `%P` becomes `%_z` and `%t` becomes `%_t`.
Basically, all new custom directives will be in the form `%_{directive}`.

### Fixed

- Fixes singular for negative values of intervals.


## [0.3.1] - 2016-07-13

### Fixed

- Fixes parsing of string with partial offset.


## [0.3] - 2016-07-11

This version causes major breaking API changes to simplify it and making it more intuitive.

### Added

- Improves testing by providing a `test()` contextmanager.


### Changed

- Makes passing a naive `datetime` to `instance()` default to `UTC`.
- Reduces `add_xxx()`/`sub_xxx()` methods to `add(**kwargs)`/`subtract(**kwargs)`.
- Changes the `for_humans()` method of the `Interval` class to `in_words()` to avoid confusion with the `diff_for_humans()` method.
- Makes more constants and methods available at module level.
- Makes the constructor behave like the standard one. No more `Pendulum()`.
- Renames the `to()` method to `in_timezone()`.
- Removes the comparison methods to just stick with the basic operators.
- Reduces `first_of_xxx()`/`last_of_xxx()`/`nth_of_xxx()` methods to `first_of(unit)`/`last_of(unit)`/`nth_of(unit, nth)`.
- Reduces `start_of_xxx()`/`end_of_xxx()` methods to `start_of(unit)`/`end_of(unit)`.
- Removes the `diff_in_xxx()` methods from the `Pendulum` and adds `in_xxx()` methods to the `Interval` class.
- Renames the `PendulumInterval` class to simply `Interval`.
- Makes the `Pendulum` class immutable.

### Fixed

- Fixes "sl" locale.


## [0.2] - 2016-07-04

### Changed

- Makes the `Pendulum` class truly inherits from `datetime`.


## [0.1.1] - 2016-07-04

### Added

- Adds support for the `TZ` environment variable.
- Adds `closest()`/`farthest()` comparison methods.
- Adds min/max attributes. Renames min/max methods.

### Changed

- Makes `set_test_now()` available at module level.

### Fixed

- Fixes `diff_for_humans()` method when setting locale.


## [0.1] - 2016-07-04

Initial release



[Unreleased]: https://github.com/sdispater/pendulum/compare/1.2.4...master
[1.2.4]: https://github.com/sdispater/pendulum/releases/tag/1.2.4
[1.2.3]: https://github.com/sdispater/pendulum/releases/tag/1.2.3
[1.2.2]: https://github.com/sdispater/pendulum/releases/tag/1.2.2
[1.2.1]: https://github.com/sdispater/pendulum/releases/tag/1.2.1
[1.2.0]: https://github.com/sdispater/pendulum/releases/tag/1.2.0
[1.1.1]: https://github.com/sdispater/pendulum/releases/tag/1.1.1
[1.1.0]: https://github.com/sdispater/pendulum/releases/tag/1.1.0
[1.0.2]: https://github.com/sdispater/pendulum/releases/tag/1.0.2
[1.0.1]: https://github.com/sdispater/pendulum/releases/tag/1.0.1
[1.0.0]: https://github.com/sdispater/pendulum/releases/tag/1.0.0
[0.8.0]: https://github.com/sdispater/pendulum/releases/tag/0.8.0
[0.7.0]: https://github.com/sdispater/pendulum/releases/tag/0.7.0
[0.6.6]: https://github.com/sdispater/pendulum/releases/tag/0.6.6
[0.6.5]: https://github.com/sdispater/pendulum/releases/tag/0.6.5
[0.6.4]: https://github.com/sdispater/pendulum/releases/tag/0.6.4
[0.6.3]: https://github.com/sdispater/pendulum/releases/tag/0.6.3
[0.6.2]: https://github.com/sdispater/pendulum/releases/tag/0.6.2
[0.6.1]: https://github.com/sdispater/pendulum/releases/tag/0.6.1
[0.6.0]: https://github.com/sdispater/pendulum/releases/tag/0.6.0
[0.5.5]: https://github.com/sdispater/pendulum/releases/tag/0.5.5
[0.5.4]: https://github.com/sdispater/pendulum/releases/tag/0.5.4
[0.5.3]: https://github.com/sdispater/pendulum/releases/tag/0.5.3
[0.5.2]: https://github.com/sdispater/pendulum/releases/tag/0.5.2
[0.5.1]: https://github.com/sdispater/pendulum/releases/tag/0.5.1
[0.5]: https://github.com/sdispater/pendulum/releases/tag/0.5
[0.4]: https://github.com/sdispater/pendulum/releases/tag/0.4
[0.3.1]: https://github.com/sdispater/pendulum/releases/tag/0.3.1
[0.3]: https://github.com/sdispater/pendulum/releases/tag/0.3
[0.2]: https://github.com/sdispater/pendulum/releases/tag/0.2
[0.1.1]: https://github.com/sdispater/pendulum/releases/tag/0.1.1
[0.1]: https://github.com/sdispater/pendulum/releases/tag/0.1
