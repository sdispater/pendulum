# String formatting

The `__str__` magic method is defined to allow `DateTime` instances to be printed
as a pretty date string when used in a string context.

The default string representation is the same as the one returned by the `isoformat()` method.

```python
>>> import pendulum

>>> dt = pendulum.datetime(1975, 12, 25, 14, 15, 16)
>>> print(dt)
'1975-12-25T14:15:16+00:00'

>>> dt.to_date_string()
'1975-12-25'

>>> dt.to_formatted_date_string()
'Dec 25, 1975'

>>> dt.to_time_string()
'14:15:16'

>>> dt.to_datetime_string()
'1975-12-25 14:15:16'

>>> dt.to_day_datetime_string()
'Thu, Dec 25, 1975 2:15 PM'

# You can also use the format() method
>>> dt.format('dddd Do [of] MMMM YYYY HH:mm:ss A')
'Thursday 25th of December 1975 02:15:16 PM'

# Of course, the strftime method is still available
>>> dt.strftime('%A %-d%t of %B %Y %I:%M:%S %p')
'Thursday 25th of December 1975 02:15:16 PM'
```

!!!note

    For localization support see the [Localization](#localization) section.

## Common Formats


The following are methods to display a `DateTime` instance as a common format:

```python
>>> import pendulum

>>> dt = pendulum.now()

>>> dt.to_atom_string()
'1975-12-25T14:15:16-05:00'

>>> dt.to_cookie_string()
'Thursday, 25-Dec-1975 14:15:16 EST'

>>> dt.to_iso8601_string()
'1975-12-25T14:15:16-0500'

>>> dt.to_rfc822_string()
'Thu, 25 Dec 75 14:15:16 -0500'

>>> dt.to_rfc850_string()
'Thursday, 25-Dec-75 14:15:16 EST'

>>> dt.to_rfc1036_string()
'Thu, 25 Dec 75 14:15:16 -0500'

>>> dt.to_rfc1123_string()
'Thu, 25 Dec 1975 14:15:16 -0500'

>>> dt.to_rfc2822_string()
'Thu, 25 Dec 1975 14:15:16 -0500'

>>> dt.to_rfc3339_string()
'1975-12-25T14:15:16-05:00'

>>> dt.to_rss_string()
'Thu, 25 Dec 1975 14:15:16 -0500'

>>> dt.to_w3c_string()
'1975-12-25T14:15:16-05:00'
```

## Formatter

Pendulum uses its own formatter when using the `format()` method.

This format is more intuitive to use than the one used with `strftime()`
and supports more directives.

```python
>>> import pendulum

>>> dt = pendulum.datetime(1975, 12, 25, 14, 15, 16)
>>> dt.format('YYYY-MM-DD HH:mm:ss')
'1975-12-25 14:15:16'
```

### Tokens

The following tokens are currently supported:


|                              | Token         | Output                                       | `strftime` Code       |
| ---------------------------- | ------------- | -------------------------------------------- | --------------------- |
| **Year**                     | YYYY          | 2000, 2001, 2002, ..., 2012, 2013            | %Y                    |
|                              | YY            | 00, 01, 02, ..., 12, 13                      | %y                    |
|                              | Y             | 2000, 2001, 2002, ..., 2012, 2013            | %Y                    |
| **Quarter**                  | Q             | 1, 2, 3, 4                                   |                       |
|                              | Qo            | 1st, 2nd, 3rd, 4th                           |                       |
| **Month**                    | MMMM          | January, February, March, ...                | %B                    |
|                              | MMM           | Jan, Feb, Mar, ...                           | %b                    |
|                              | MM            | 01, 02, 03, ..., 11, 12                      | %m                    |
|                              | M             | 1, 2, 3, ..., 11, 12                         | %-m*                  |
|                              | Mo            | 1st, 2nd, ..., 11th, 12th                    |                       |
| **Day of Year**              | DDDD          | 001, 002, 003 ... 364, 365                   | %j                    |
|                              | DDD           | 1, 2, 3, ..., 4, 5                           | %-j*                  |
| **Day of Month**             | DD            | 01, 02, 03, ..., 30, 31                      | %d                    |
|                              | D             | 1, 2, 3, ..., 30, 31                         | %-d*                  |
|                              | Do            | 1st, 2nd, 3rd, ..., 30th, 31st               |                       |
| **Day of Week**              | dddd          | Monday, Tuesday, Wednesday, ...              | %A                    |
|                              | ddd           | Mon, Tue, Wed, ...                           | %a                    |
|                              | dd            | Mo, Tu, We, ...                              |                       |
|                              | d             | 0, 1, 2, ..., 6                              | %w                    |
| **Day of ISO Week**          | E             | 1, 2, 3, ..., 7                              | %u                    |
| **Week of Year**             | WW            | 00, 01, 02, ..., 52, 53                      | %U                    |
|                              | W             | 0, 1, 2, ..., 52, 53                         | %W                    |
| **Hour**                     | HH            | 00, 01, 02, ..., 23, 24                      | %H                    |
|                              | H             | 0, 1, 2, ..., 23, 24                         | %-H*                  |
|                              | hh            | 01, 02, 03, ..., 11, 12                      | %I                    |
|                              | h             | 1, 2, 3, ..., 11, 12                         | %-I*                  |
| **Minute**                   | mm            | 00, 01, 02, ..., 58, 59                      | %M                    |
|                              | m             | 0, 1, 2, ..., 58, 59                         | %-M*                  |
| **Second**                   | ss            | 00, 01, 02, ..., 58, 59                      | %S                    |
|                              | s             | 0, 1, 2, ..., 58, 59                         | %-S*                  |
| **Fractional Second**        | S             | 0, 1, ..., 8, 9                              |                       |
|                              | SS            | 00, 01, 02, ..., 98, 99                      |                       |
|                              | SSS           | 000, 001, ..., 998, 999                      |                       |
|                              | SSSS          | 0000, 0001, ..., 9998, 9999                  |                       |
|                              | SSSSS         | 00000, 00001, ..., 99998, 99999              |                       |
|                              | SSSSSS        | 000000, 000001, ..., 999998, 999999          | %f                    |
| **AM / PM**                  | A             | AM, PM                                       | %p                    |
| **Timezone**                 | Z             | -07:00, -06:00, ..., +06:00, +07:00          |                       |
|                              | ZZ            | -0700, -0600, ..., +0600, +0700              | %z                    |
|                              | z             | Asia/Baku, Europe/Warsaw, GMT ...            |                       |
|                              | zz            | EST, CST, ..., MST, PST                      | %Z                    |
| **Seconds timestamp**        | X             | 1381685817, 1234567890.123                   |                       |
| **Milliseconds timestamp**   | x             | 1234567890123                                |                       |

\* _`strftime` directive depends on platform support. See [strftime.org](https://strftime.org#platforms) for details._

### Localized Formats

Because preferred formatting differs based on locale,
there are a few tokens that can be used to format an instance based on its locale.

|                                                        |               |                                            |
| ------------------------------------------------------ | ------------- | ------------------------------------------ |
| **Time**                                               | LT            | 8:30 PM                                    |
| **Time with seconds**                                  | LTS           | 8:30:25 PM                                 |
| **Month numeral, day of month, year**                  | L             | 09/04/1986                                 |
| **Month name, day of month, year**                     | LL            | September 4 1986                           |
| **Month name, day of month, year, time**               | LLL           | September 4 1986 8:30 PM                   |
| **Month name, day of month, day of week, year, time**  | LLLL          | Thursday, September 4 1986 8:30 PM         |

### Escaping Characters

To escape characters in format strings, you can wrap the characters in square brackets.

```python
>>> import pendulum

>>> dt = pendulum.now()
>>> dt.format('[today] dddd')
'today Sunday'
```
