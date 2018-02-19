# Change Log

## [Unreleased]

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



[Unreleased]: https://github.com/sdispater/pendulum/compare/1.x...2.0
