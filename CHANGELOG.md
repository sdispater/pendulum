# Change Log

## [Unreleased]

### Fixed

- Fixed `from_format()` not recognizing input strings when the specified pattern had escaped elements.
- Fixed missing `x` token for string formatting.


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



[Unreleased]: https://github.com/sdispater/pendulum/compare/2.0.3...master
[2.0.3]: https://github.com/sdispater/pendulum/releases/tag/2.0.3
[2.0.2]: https://github.com/sdispater/pendulum/releases/tag/2.0.2
[2.0.1]: https://github.com/sdispater/pendulum/releases/tag/2.0.1
[2.0.0]: https://github.com/sdispater/pendulum/releases/tag/2.0.0
