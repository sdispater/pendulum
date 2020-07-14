# Change Log

## [2.1.1] - 2020-07-13

### Fixed

- Fixed errors where invalid timezones were matched in `from_format()` ([#374](https://github.com/sdispater/pendulum/pull/374)).
- Fixed errors when subtracting negative timedeltas ([#419](https://github.com/sdispater/pendulum/pull/419)).
- Fixed errors in total units computation for durations with years and months ([#482](https://github.com/sdispater/pendulum/pull/482)).
- Fixed an error where the `fold` attribute was overridden when using `replace()` ([#414](https://github.com/sdispater/pendulum/pull/414)).
- Fixed an error where `now()` was not returning the correct result on DST transitions ([#483](https://github.com/sdispater/pendulum/pull/483)).
- Fixed inconsistent typing annotation for the `parse()` function ([#452](https://github.com/sdispater/pendulum/pull/452)).

### Locales

- Added the `pl` locale ([#459](https://github.com/sdispater/pendulum/pull/459)).


## [2.1.0] - 2020-03-07

### Added

- Added better typing and PEP-561 compliance ([#320](https://github.com/sdispater/pendulum/pull/320)).
- Added the `is_anniversary()` method as an alias of `is_birthday()` ([#298](https://github.com/sdispater/pendulum/pull/298)).

### Changed

- Dropped support for Python 3.4.
- `is_utc()` will now return `True` for any datetime with an offset of 0, similar to the behavior in the `1.*` versions ([#295](https://github.com/sdispater/pendulum/pull/295))
- `Duration.in_words()` will now return `0 milliseconds` for empty durations.

### Fixed

- Fixed various issues with timezone transitions for some edge cases ([#321](https://github.com/sdispater/pendulum/pull/321), ([#350](https://github.com/sdispater/pendulum/pull/350))).
- Fixed out of bound detection for `nth_of("month")` ([#357](https://github.com/sdispater/pendulum/pull/357)).
- Fixed an error where extra text was accepted in `from_format()` ([#372](https://github.com/sdispater/pendulum/pull/372)).
- Fixed a recursion error when adding time to a `DateTime` with a fixed timezone ([#431](https://github.com/sdispater/pendulum/pull/431)).
- Fixed errors where `Period` instances were not properly compared to other classes, especially `timedelta` instances ([#427](https://github.com/sdispater/pendulum/pull/427)).
- Fixed deprecation warnings due to internal regexps ([#427](https://github.com/sdispater/pendulum/pull/427)).
- Fixed an error where the `test()` helper would not unset the test instance when an exception was raised ([#445](https://github.com/sdispater/pendulum/pull/445)).
- Fixed an error where the `week_of_month` attribute was not returning the correct value ([#446](https://github.com/sdispater/pendulum/pull/446)).
- Fixed an error in the way the `Z` ISO-8601 UTC designator was not parsed as UTC ([#448](https://github.com/sdispater/pendulum/pull/448)).

### Locales

- Added the `nl` locale.
- Added the `it` locale.
- Added the `id` locale.
- Added the `nb` locale.
- Added the `nn` locale.


## [2.0.5] - 2019-07-03

### Fixed

- Fixed ISO week dates not being parsed properly in `from_format()`.
- Fixed loading of some timezones with empty posix spec.
- Fixed deprecation warnings.

### Locales

- Added RU locale.


## [2.0.4] - 2018-10-30

### Fixed

- Fixed `from_format()` not recognizing input strings when the specified pattern had escaped elements.
- Fixed missing `x` token for string formatting.
- Fixed reading timezone files.
- Added support for parsing padded 2-digit days of the month with `from_format()`
- Fixed `from_format()` trying to parse escaped tokens.
- Fixed the `z` token timezone parsing in `from_format()` to allow underscores.
- Fixed C extensions build errors.
- Fixed `age` calculation for future dates.


## [2.0.3] - 2018-07-30

### Fixed

- Fixed handling of `pytz` timezones.
- Fixed some formatter's tokens handling.
- Fixed errors on some systems when retrieving timezone from localtime files.
- Fixed `diff` methods.
- Fixed `closest()/farthest()` methods.


## [2.0.2] - 2018-05-29

### Fixed

- Fixed the `weeks` property for negative `Period` instances.
- Fixed `start_of()` methods not setting microseconds to 0.
- Fixed errors on some systems when retrieving timezone from clock files.
- Fixed parsing of partial time.
- Fixed parsing not raising an error for week 53 for ordinary years.
- Fixed string formatting not supporting `strftime` format.


## [2.0.1] - 2018-05-10

### Fixed

- Fixed behavior of the `YY` token in `from_format()`.
- Fixed errors on some systems when retrieving timezone from clock files.


## [2.0.0] - 2018-05-08

### Added

- Added years and months support to durations.
- Added the `test_local_timezone()` and `set_local_timezone()` helpers to ease testing.
- Added support of ISO 8601 duration parsing.
- Added support of ISO 8601 interval parsing.
- Added a `local()` helper.
- Added a `naive()` helper and a `naive()` method.
- Added support for POSIX specification to extend timezones DST transitions.

### Changed

- `Pendulum` class has been renamed to `DateTime`.
- `Interval` class has been renamed to `Duration`.
- Changed and improved the timezone system.
- Removed the `create()` helper.
- Removed the `utcnow()` helper.
- `strict` keyword argument for `parse` has been renamed to `exact`.
- `at()` now supports setting partial time.
- `local`, `utc` and `is_dst` are now methods rather than properties (`is_local()`, `is_utc()`, `is_dst()`).
- Changed the `repr` of most common objects.
- Made the `strict` keyword argument for `parse` false by default, which means it will not fallback on the `dateutil` parser.
- Improved performances of the `precise_diff()` helper.
- The `alternative` formatter is now the default one.
- `set_to_string_format()/reset_to_string_format()` methods have been removed.
- `from_format()` now uses the alternative formatter tokens.
- Removed `xrange()` method of the `Period` class and made `range()` a generator.
- New locale system which uses CLDR data for most of the translations.
- `diff_for_humans()` now returns `a few seconds` where appropriate.
- Removed `Period.intersect()`.



[Unreleased]: https://github.com/sdispater/pendulum/compare/2.1.1...master
[2.1.1]: https://github.com/sdispater/pendulum/releases/tag/2.1.1
[2.1.0]: https://github.com/sdispater/pendulum/releases/tag/2.1.0
[2.0.5]: https://github.com/sdispater/pendulum/releases/tag/2.0.5
[2.0.4]: https://github.com/sdispater/pendulum/releases/tag/2.0.4
[2.0.3]: https://github.com/sdispater/pendulum/releases/tag/2.0.3
[2.0.2]: https://github.com/sdispater/pendulum/releases/tag/2.0.2
[2.0.1]: https://github.com/sdispater/pendulum/releases/tag/2.0.1
[2.0.0]: https://github.com/sdispater/pendulum/releases/tag/2.0.0
