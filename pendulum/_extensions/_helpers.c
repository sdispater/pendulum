/* ------------------------------------------------------------------------- */

#include <Python.h>
#include <datetime.h>
#include <structmember.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifndef PyVarObject_HEAD_INIT
    #define PyVarObject_HEAD_INIT(type, size) PyObject_HEAD_INIT(type) size,
#endif

/* ------------------------------------------------------------------------- */

#define EPOCH_YEAR 1970

#define DAYS_PER_N_YEAR 365
#define DAYS_PER_L_YEAR 366

#define USECS_PER_SEC 1000000

#define SECS_PER_MIN 60
#define SECS_PER_HOUR (60 * SECS_PER_MIN)
#define SECS_PER_DAY (SECS_PER_HOUR * 24)

// 400-year chunks always have 146097 days (20871 weeks).
#define DAYS_PER_400_YEARS 146097L
#define SECS_PER_400_YEARS ((int64_t)DAYS_PER_400_YEARS * (int64_t)SECS_PER_DAY)

// The number of seconds in an aligned 100-year chunk, for those that
// do not begin with a leap year and those that do respectively.
const int64_t SECS_PER_100_YEARS[2] = {
    (uint64_t)(76L * DAYS_PER_N_YEAR + 24L * DAYS_PER_L_YEAR) * SECS_PER_DAY,
    (uint64_t)(75L * DAYS_PER_N_YEAR + 25L * DAYS_PER_L_YEAR) * SECS_PER_DAY
};

// The number of seconds in an aligned 4-year chunk, for those that
// do not begin with a leap year and those that do respectively.
const int32_t SECS_PER_4_YEARS[2] = {
    (4 * DAYS_PER_N_YEAR + 0 * DAYS_PER_L_YEAR) * SECS_PER_DAY,
    (3 * DAYS_PER_N_YEAR + 1 * DAYS_PER_L_YEAR) * SECS_PER_DAY
};

// The number of seconds in non-leap and leap years respectively.
const int32_t SECS_PER_YEAR[2] = {
    DAYS_PER_N_YEAR * SECS_PER_DAY,
    DAYS_PER_L_YEAR * SECS_PER_DAY
};

#define MONTHS_PER_YEAR 12

// The month lengths in non-leap and leap years respectively.
const int32_t DAYS_PER_MONTHS[2][13] = {
    {-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31},
    {-1, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
};

// The day offsets of the beginning of each (1-based) month in non-leap
// and leap years respectively.
// For example, in a leap year there are 335 days before December.
const int32_t MONTHS_OFFSETS[2][14] = {
    {-1, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365},
    {-1, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366}
};

const int DAY_OF_WEEK_TABLE[12] = {
    0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4
};

#define TM_SUNDAY 0
#define TM_MONDAY 1
#define TM_TUESDAY 2
#define TM_WEDNESDAY 3
#define TM_THURSDAY 4
#define TM_FRIDAY 5
#define TM_SATURDAY 6

#define TM_JANUARY 0
#define TM_FEBRUARY 1
#define TM_MARCH 2
#define TM_APRIL 3
#define TM_MAY 4
#define TM_JUNE 5
#define TM_JULY 6
#define TM_AUGUST 7
#define TM_SEPTEMBER 8
#define TM_OCTOBER 9
#define TM_NOVEMBER 10
#define TM_DECEMBER 11

// Parsing errors
const int PARSER_INVALID_ISO8601 = 0;
const int PARSER_INVALID_DATE = 1;
const int PARSER_INVALID_TIME = 2;
const int PARSER_INVALID_WEEK_DATE = 3;
const int PARSER_INVALID_WEEK_NUMBER = 4;
const int PARSER_INVALID_WEEKDAY_NUMBER = 5;
const int PARSER_INVALID_ORDINAL_DAY_FOR_YEAR = 6;
const int PARSER_INVALID_MONTH_OR_DAY = 7;
const int PARSER_INVALID_MONTH = 8;
const int PARSER_INVALID_DAY_FOR_MONTH = 9;
const int PARSER_INVALID_HOUR = 10;
const int PARSER_INVALID_MINUTE = 11;
const int PARSER_INVALID_SECOND = 12;
const int PARSER_INVALID_SUBSECOND = 13;
const int PARSER_INVALID_TZ_OFFSET = 14;

/* ------------------------------------------------------------------------- */

int is_leap(int year) {
    return year % 4 == 0 && (year % 100 != 0 || year % 400 == 0);
}

int week_day(int year, int month, int day) {
    int y;
    int w;

    y = year - (month < 3);

    w = (y + y/4 - y/100 + y /400 + DAY_OF_WEEK_TABLE[month - 1] + day) % 7;

    if (!w) {
        w = 7;
    }

    return w;
}

int days_in_year(int year) {
    if (is_leap(year)) {
        return DAYS_PER_L_YEAR;
    }

    return DAYS_PER_N_YEAR;
}

/* ------------------------ Custom Types ------------------------------- */

#if defined(PY_MAJOR_VERSION)
/*
 * class FixedOffset(tzinfo):
 */
typedef struct {
    PyObject_HEAD
    int offset;
} FixedOffset;

/*
 * def __init__(self, offset):
 *     self.offset = offset
*/
static int FixedOffset_init(FixedOffset *self, PyObject *args, PyObject *kwargs) {
    int offset;
    if (!PyArg_ParseTuple(args, "i", &offset))
        return -1;

    self->offset = offset;
    return 0;
}

/*
 * def utcoffset(self, dt):
 *     return timedelta(seconds=self.offset * 60)
 */
static PyObject *FixedOffset_utcoffset(FixedOffset *self, PyObject *args) {
    return PyDelta_FromDSU(0, self->offset, 0);
}

/*
 * def dst(self, dt):
 *     return timedelta(seconds=self.offset * 60)
 */
static PyObject *FixedOffset_dst(FixedOffset *self, PyObject *args) {
    return PyDelta_FromDSU(0, self->offset, 0);
}

/*
 * def tzname(self, dt):
 *     sign = '+'
 *     if self.offset < 0:
 *         sign = '-'
 *     return "%s%d:%d" % (sign, self.offset / 60, self.offset % 60)
 */
static PyObject *FixedOffset_tzname(FixedOffset *self, PyObject *args) {
    char tzname[7] = {0};
    char sign = '+';
    int offset = self->offset;

    if (offset < 0) {
        sign = '-';
        offset *= -1;
    }

    sprintf(
        tzname,
        "%c%02d:%02d",
        sign,
        offset / SECS_PER_HOUR,
        offset / SECS_PER_MIN % SECS_PER_MIN
    );

    return PyUnicode_FromString(tzname);
}

/*
 * def __repr__(self):
 *     return self.tzname()
 */
static PyObject *FixedOffset_repr(FixedOffset *self) {
    return FixedOffset_tzname(self, NULL);
}

/*
 * Class member / class attributes
 */
static PyMemberDef FixedOffset_members[] = {
    {"offset", T_INT, offsetof(FixedOffset, offset), 0, "UTC offset"},
    {NULL}
};

/*
 * Class methods
 */
static PyMethodDef FixedOffset_methods[] = {
    {"utcoffset", (PyCFunction)FixedOffset_utcoffset, METH_VARARGS, ""},
    {"dst",       (PyCFunction)FixedOffset_dst,       METH_VARARGS, ""},
    {"tzname",    (PyCFunction)FixedOffset_tzname,    METH_VARARGS, ""},
    {NULL}
};

static PyTypeObject FixedOffset_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "helpers.FixedOffset_type",             /* tp_name */
    sizeof(FixedOffset),                    /* tp_basicsize */
    0,                                      /* tp_itemsize */
    0,                                      /* tp_dealloc */
    0,                                      /* tp_print */
    0,                                      /* tp_getattr */
    0,                                      /* tp_setattr */
    0,                                      /* tp_as_async */
    (reprfunc)FixedOffset_repr,             /* tp_repr */
    0,                                      /* tp_as_number */
    0,                                      /* tp_as_sequence */
    0,                                      /* tp_as_mapping */
    0,                                      /* tp_hash  */
    0,                                      /* tp_call */
    (reprfunc)FixedOffset_repr,             /* tp_str */
    0,                                      /* tp_getattro */
    0,                                      /* tp_setattro */
    0,                                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE, /* tp_flags */
    "TZInfo with fixed offset",             /* tp_doc */
};

/*
 * Instantiate new FixedOffset_type object
 * Skip overhead of calling PyObject_New and PyObject_Init.
 * Directly allocate object.
 */
static PyObject *new_fixed_offset_ex(int offset, PyTypeObject *type) {
    FixedOffset *self = (FixedOffset *) (type->tp_alloc(type, 0));

    if (self != NULL)
        self->offset = offset;

    return (PyObject *) self;
}

#define new_fixed_offset(offset) new_fixed_offset_ex(offset, &FixedOffset_type)


/*
 * class Diff():
 */
typedef struct {
    PyObject_HEAD
    int years;
    int months;
    int days;
    int hours;
    int minutes;
    int seconds;
    int microseconds;
} Diff;

/*
 * def __init__(self, years, months, days, hours, minutes, seconds, microseconds):
 *     self.years = years
 *     # ...
*/
static int Diff_init(Diff *self, PyObject *args, PyObject *kwargs) {
    int years;
    int months;
    int days;
    int hours;
    int minutes;
    int seconds;
    int microseconds;

    if (!PyArg_ParseTuple(args, "iiiiiii", &years, &months, &days, &hours, &minutes, &seconds, &microseconds))
        return -1;

    self->years = years;
    self->months = months;
    self->days = days;
    self->hours = hours;
    self->minutes = minutes;
    self->seconds = seconds;
    self->microseconds = microseconds;

    return 0;
}

/*
 * def __repr__(self):
 *     return '{} years {} months {} days {} hours {} minutes {} seconds {} microseconds'.format(
 *         self.years, self.months, self.days, self.minutes, self.hours, self.seconds, self.microseconds
 *     )
 */
static PyObject *Diff_repr(Diff *self) {
    char repr[82] = {0};

    sprintf(
        repr,
        "%d years %d months %d days %d hours %d minutes %d seconds %d microseconds",
        self->years,
        self->months,
        self->days,
        self->hours,
        self->minutes,
        self->seconds,
        self->microseconds
    );

    return PyUnicode_FromString(repr);
}

/*
 * Instantiate new Diff_type object
 * Skip overhead of calling PyObject_New and PyObject_Init.
 * Directly allocate object.
 */
static PyObject *new_diff_ex(int years, int months, int days, int hours, int minutes, int seconds, int microseconds, PyTypeObject *type) {
    Diff *self = (Diff *) (type->tp_alloc(type, 0));

    if (self != NULL) {
        self->years = years;
        self->months = months;
        self->days = days;
        self->hours = hours;
        self->minutes = minutes;
        self->seconds = seconds;
        self->microseconds = microseconds;
    }

    return (PyObject *) self;
}

/*
 * Class member / class attributes
 */
static PyMemberDef Diff_members[] = {
    {"years", T_INT, offsetof(Diff, years), 0, "years in diff"},
    {"months", T_INT, offsetof(Diff, months), 0, "months in diff"},
    {"days", T_INT, offsetof(Diff, days), 0, "days in diff"},
    {"hours", T_INT, offsetof(Diff, hours), 0, "hours in diff"},
    {"minutes", T_INT, offsetof(Diff, minutes), 0, "minutes in diff"},
    {"seconds", T_INT, offsetof(Diff, seconds), 0, "seconds in diff"},
    {"microseconds", T_INT, offsetof(Diff, microseconds), 0, "microseconds in diff"},
    {NULL}
};

static PyTypeObject Diff_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "PreciseDiff",                  /* tp_name */
    sizeof(Diff),                           /* tp_basicsize */
    0,                                      /* tp_itemsize */
    0,                                      /* tp_dealloc */
    0,                                      /* tp_print */
    0,                                      /* tp_getattr */
    0,                                      /* tp_setattr */
    0,                                      /* tp_as_async */
    (reprfunc)Diff_repr,                    /* tp_repr */
    0,                                      /* tp_as_number */
    0,                                      /* tp_as_sequence */
    0,                                      /* tp_as_mapping */
    0,                                      /* tp_hash  */
    0,                                      /* tp_call */
    (reprfunc)Diff_repr,                    /* tp_str */
    0,                                      /* tp_getattro */
    0,                                      /* tp_setattro */
    0,                                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT|Py_TPFLAGS_BASETYPE, /* tp_flags */
    "Precise difference between two datetime objects",             /* tp_doc */
};

#define new_diff(years, months, days, hours, minutes, seconds, microseconds) new_diff_ex(years, months, days, hours, minutes, seconds, microseconds, &Diff_type)


/*
 * class Parsed():
 */
typedef struct {
    int is_date;
    int is_time;
    int is_datetime;
    int is_duration;
    int is_period;
    int ambiguous;
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
    int microsecond;
    int offset;
    int has_offset;
    int years;
    int months;
    int weeks;
    int days;
    int hours;
    int minutes;
    int seconds;
    int microseconds;
    int error;
} Parsed;


Parsed* new_parsed() {
    Parsed *parsed;

    if((parsed = malloc(sizeof *parsed)) != NULL) {
        parsed->is_date = 0;
        parsed->is_time = 0;
        parsed->is_datetime = 0;
        parsed->is_duration = 0;
        parsed->is_period = 0;

        parsed->ambiguous = 0;
        parsed->year = 0;
        parsed->month = 1;
        parsed->day = 1;
        parsed->hour = 0;
        parsed->minute = 0;
        parsed->second = 0;
        parsed->microsecond = 0;
        parsed->offset = 0;
        parsed->has_offset = 0;

        parsed->years = 0;
        parsed->months = 0;
        parsed->weeks = 0;
        parsed->days = 0;
        parsed->hours = 0;
        parsed->minutes = 0;
        parsed->seconds = 0;
        parsed->microseconds = 0;

        parsed->error = -1;
    }

    return parsed;
}

/* -------------------------- Functions --------------------------*/

PyObject* local_time(PyObject *self, PyObject *args) {
    double unix_time;
    int32_t utc_offset;
    int32_t year;
    int32_t microsecond;
    int64_t seconds;
    int32_t leap_year;
    int64_t sec_per_100years;
    int64_t sec_per_4years;
    int32_t sec_per_year;
    int32_t month;
    int32_t day;
    int32_t month_offset;
    int32_t hour;
    int32_t minute;
    int32_t second;

    if (!PyArg_ParseTuple(args, "dii", &unix_time, &utc_offset, &microsecond)) {
        PyErr_SetString(
            PyExc_ValueError, "Invalid parameters"
        );
        return NULL;
    }

    year = EPOCH_YEAR;
    seconds = (int64_t) unix_time;

    // Shift to a base year that is 400-year aligned.
    if (seconds >= 0) {
        seconds -= 10957L * SECS_PER_DAY;
        year += 30;  // == 2000;
    } else {
        seconds += (int64_t)(146097L - 10957L) * SECS_PER_DAY;
        year -= 370;  // == 1600;
    }

    seconds += utc_offset;

    // Handle years in chunks of 400/100/4/1
    year += 400 * (seconds / SECS_PER_400_YEARS);
    seconds %= SECS_PER_400_YEARS;
    if (seconds < 0) {
        seconds += SECS_PER_400_YEARS;
        year -= 400;
    }

    leap_year = 1;  // 4-century aligned

    sec_per_100years = SECS_PER_100_YEARS[leap_year];

    while (seconds >= sec_per_100years) {
        seconds -= sec_per_100years;
        year += 100;
        leap_year = 0;  // 1-century, non 4-century aligned
        sec_per_100years = SECS_PER_100_YEARS[leap_year];
    }

    sec_per_4years = SECS_PER_4_YEARS[leap_year];
    while (seconds >= sec_per_4years) {
        seconds -= sec_per_4years;
        year += 4;
        leap_year = 1;  // 4-year, non century aligned
        sec_per_4years = SECS_PER_4_YEARS[leap_year];
    }

    sec_per_year = SECS_PER_YEAR[leap_year];
    while (seconds >= sec_per_year) {
        seconds -= sec_per_year;
        year += 1;
        leap_year = 0;  // non 4-year aligned
        sec_per_year = SECS_PER_YEAR[leap_year];
    }

    // Handle months and days
    month = TM_DECEMBER + 1;
    day = seconds / SECS_PER_DAY + 1;
    seconds %= SECS_PER_DAY;
    while (month != TM_JANUARY + 1) {
        month_offset = MONTHS_OFFSETS[leap_year][month];
        if (day > month_offset) {
            day -= month_offset;
            break;
        }

        month -= 1;
    }

    // Handle hours, minutes and seconds
    hour = seconds / SECS_PER_HOUR;
    seconds %= SECS_PER_HOUR;
    minute = seconds / SECS_PER_MIN;
    second = seconds % SECS_PER_MIN;

    return Py_BuildValue("NNNNNNN",
        PyLong_FromLong(year),
        PyLong_FromLong(month),
        PyLong_FromLong(day),
        PyLong_FromLong(hour),
        PyLong_FromLong(minute),
        PyLong_FromLong(second),
        PyLong_FromLong(microsecond)
    );
}


Parsed* _parse_iso8601_datetime(char *str, Parsed *parsed) {
    char* c;
    int monthday = 0;
    int week = 0;
    int weekday = 1;
    int ordinal;
    int tz_sign = 0;
    int leap = 0;
    int separators = 0;
    int time = 0;
    int has_hour = 0;
    int i;
    int j;

    // Assuming date only for now
    parsed->is_date = 1;

    c = str;

    for (i = 0; i < 4; i++) {
        if (*c >= '0' && *c <= '9') {
            parsed->year = 10 * parsed->year + *c++ - '0';
        } else {
            parsed->error = PARSER_INVALID_ISO8601;

            return NULL;
        }
    }

    leap = is_leap(parsed->year);

    // Optional separator
    if (*c == '-') {
        separators++;
        c++;
    }

    // Checking for week dates
    if (*c == 'W') {
        c++;

        i = 0;
        while (*c != '\0' && *c != ' ' && *c != 'T') {
            if (*c == '-') {
                separators++;
                c++;
                continue;
            }

            week = 10 * week + *c++ - '0';

            i++;
        }

        switch (i) {
            case 2:
                // Only week number
                break;
            case 3:
                // Week with weekday
                if (!(separators == 0 || separators == 2)) {
                    // We should have 2 or no separator
                    parsed->error = PARSER_INVALID_WEEK_DATE;

                    return NULL;
                }

                weekday = week % 10;
                week /= 10;

                break;
            default:
                // Any other case is wrong
                parsed->error = PARSER_INVALID_WEEK_DATE;

                return NULL;
        }

        // Checks
        if (week > 53) {
            parsed->error = PARSER_INVALID_WEEK_NUMBER;

            return NULL;
        }

        if (weekday > 7) {
            parsed->error = PARSER_INVALID_WEEKDAY_NUMBER;

            return NULL;
        }

        // Calculating ordinal day
        ordinal = week * 7 + weekday - (week_day(parsed->year, 1, 4) + 3);

        if (ordinal < 1) {
            // Previous year
            ordinal += days_in_year(parsed->year - 1);
            parsed->year -= 1;
            leap = is_leap(parsed->year);
        }

        if (ordinal > days_in_year(parsed->year)) {
            // Next year
            ordinal -= days_in_year(parsed->year);
            parsed->year += 1;
            leap = is_leap(parsed->year);
        }

        for (j = 1; j < 14; j++) {
            if (ordinal <= MONTHS_OFFSETS[leap][j]) {
                parsed->day = ordinal - MONTHS_OFFSETS[leap][j - 1];
                parsed->month = j - 1;

                break;
            }
        }
    } else {
        // At this point we need to check the number
        // of characters until the end of the date part
        // (or the end of the string).
        //
        // If two, we have only a month if there is a separator, it may be a time otherwise.
        // If three, we have an ordinal date.
        // If four, we have a complete date
        i = 0;
        while (*c != '\0' && *c != ' ' && *c != 'T') {
            if (*c == '-') {
                separators++;
                c++;
                continue;
            }

            if (!(*c >= '0' && *c <='9')) {
                parsed->error = PARSER_INVALID_DATE;

                return NULL;
            }

            monthday = 10 * monthday + *c++ - '0';

            i++;
        }

        switch (i) {
            case 0:
                // No month/day specified (only a year)
                break;
            case 2:
                if (!separators) {
                    // The date looks like 201207
                    // which is invalid for a date
                    // But it might be a time in the form hhmmss
                    parsed->ambiguous = 1;
                }

                parsed->month = monthday;
                break;
            case 3:
                // Ordinal day
                if (separators > 1) {
                    parsed->error = PARSER_INVALID_DATE;

                    return NULL;
                }

                if (monthday < 1 || monthday > MONTHS_OFFSETS[leap][13]) {
                    parsed->error = PARSER_INVALID_ORDINAL_DAY_FOR_YEAR;

                    return NULL;
                }

                for (j = 1; j < 14; j++) {
                    if (monthday <= MONTHS_OFFSETS[leap][j]) {
                        parsed->day = monthday - MONTHS_OFFSETS[leap][j - 1];
                        parsed->month = j - 1;

                        break;
                    }
                }

                break;
            case 4:
                // Month and day
                parsed->month = monthday / 100;
                parsed->day = monthday % 100;

                break;
            default:
                parsed->error = PARSER_INVALID_MONTH_OR_DAY;

                return NULL;
        }
    }

    // Checks
    if (separators && !monthday && !week) {
        parsed->error = PARSER_INVALID_DATE;

        return NULL;
    }

    if (parsed->month > 12) {
        parsed->error = PARSER_INVALID_MONTH;

        return NULL;
    }

    if (parsed->day > DAYS_PER_MONTHS[leap][parsed->month]) {
        parsed->error = PARSER_INVALID_DAY_FOR_MONTH;

        return NULL;
    }

    separators = 0;
    if (*c == 'T' || *c == ' ') {
        if (parsed->ambiguous) {
            parsed->error = PARSER_INVALID_DATE;

            return NULL;
        }

        // We have time so we have a datetime
        parsed->is_datetime = 1;
        parsed->is_date = 0;

        c++;

        // Grabbing time information
        i = 0;
        while (*c != '\0' && *c != '.' && *c != ',' && *c != 'Z' && *c != '+' && *c != '-') {
            if (*c == ':') {
                separators++;
                c++;
                continue;
            }

            if (!(*c >= '0' && *c <='9')) {
                parsed->error = PARSER_INVALID_TIME;

                return NULL;
            }

            time = 10 * time + *c++ - '0';
            i++;
        }

        switch (i) {
            case 2:
                // Hours only
                if (separators > 0) {
                    // Extraneous separators
                    parsed->error = PARSER_INVALID_TIME;

                    return NULL;
                }

                parsed->hour = time;
                has_hour = 1;
                break;
            case 4:
                // Hours and minutes
                if (separators > 1) {
                    // Extraneous separators
                    parsed->error = PARSER_INVALID_TIME;

                    return NULL;
                }

                parsed->hour = time / 100;
                parsed->minute = time % 100;
                has_hour = 1;
                break;
            case 6:
                // Hours, minutes and seconds
                if (!(separators == 0 || separators == 2)) {
                    // We should have either two separators or none
                    parsed->error = PARSER_INVALID_TIME;

                    return NULL;
                }

                parsed->hour = time / 10000;
                parsed->minute = time / 100 % 100;
                parsed->second = time % 100;
                has_hour = 1;
                break;
            default:
                // Any other case is wrong
                parsed->error = PARSER_INVALID_TIME;

                return NULL;
        }

        // Checks
        if (parsed->hour > 23) {
            parsed->error = PARSER_INVALID_HOUR;

            return NULL;
        }

        if (parsed->minute > 59) {
            parsed->error = PARSER_INVALID_MINUTE;

            return NULL;
        }

        if (parsed->second > 59) {
            parsed->error = PARSER_INVALID_SECOND;

            return NULL;
        }

        // Subsecond
        if (*c == '.' || *c == ',') {
            c++;

            time = 0;
            i = 0;
            while (*c != '\0' && *c != 'Z' && *c != '+' && *c != '-') {
                if (!(*c >= '0' && *c <='9')) {
                    parsed->error = PARSER_INVALID_SUBSECOND;

                    return NULL;
                }

                time = 10 * time + *c++ - '0';
                i++;
            }

            // adjust to microseconds
            if (i > 6) {
                parsed->microsecond = time / pow(10, i - 6);
            } else if (i <= 6) {
                parsed->microsecond = time * pow(10, 6 - i);
            }
        }

        // Timezone
        if (*c == 'Z') {
            parsed->has_offset = 1;
            c++;
        } else if (*c == '+' || *c == '-') {
            tz_sign = 1;
            if (*c == '-') {
                tz_sign = -1;
            }

            parsed->has_offset = 1;
            c++;

            i = 0;
            time = 0;
            separators = 0;
            while (*c != '\0') {
                if (*c == ':') {
                    separators++;
                    c++;
                    continue;
                }

                if (!(*c >= '0' && *c <= '9')) {
                    parsed->error = PARSER_INVALID_TZ_OFFSET;

                    return NULL;
                }

                time = 10 * time + *c++ - '0';
                i++;
            }

            switch (i) {
                case 2:
                    // hh Format
                    if (separators) {
                        // Extraneous separators
                        parsed->error = PARSER_INVALID_TZ_OFFSET;

                        return NULL;
                    }

                    parsed->offset = tz_sign * (time * 3600);
                    break;
                case 4:
                    // hhmm Format
                    if (separators > 1) {
                        // Extraneous separators
                        parsed->error = PARSER_INVALID_TZ_OFFSET;

                        return NULL;
                    }

                    parsed->offset = tz_sign * ((time / 100 * 3600) + (time % 100 * 60));
                    break;
                default:
                    // Wrong format
                    parsed->error = PARSER_INVALID_TZ_OFFSET;

                    return NULL;
            }
        }
    }

    return parsed;
}


PyObject* parse_iso8601(PyObject *self, PyObject *args) {
    char* str;
    PyObject *obj;
    PyObject *tzinfo;
    Parsed *parsed = new_parsed();

    if (!PyArg_ParseTuple(args, "s", &str)) {
        PyErr_SetString(
            PyExc_ValueError, "Invalid parameters"
        );
        return NULL;
    }

    if (_parse_iso8601_datetime(str, parsed) == NULL) {
        char error[80];
        sprintf(error, "%i", parsed->error);

        PyErr_SetString(
            PyExc_ValueError, error
        );

        return NULL;
    }

    if (parsed->is_date) {
        // Date only
        if (parsed->ambiguous) {
            // We can "safely" assume that the ambiguous
            // date was actually a time in the form hhmmss
            parsed->hour = parsed->year / 100;
            parsed->minute = parsed->year % 100;
            parsed->second = parsed->month;

            obj = PyDateTimeAPI->Time_FromTime(
                parsed->hour, parsed->minute, parsed->second, parsed->microsecond,
                Py_BuildValue(""),
                PyDateTimeAPI->TimeType
            );
        } else {
            obj = PyDateTimeAPI->Date_FromDate(
                parsed->year, parsed->month, parsed->day,
                PyDateTimeAPI->DateType
            );
        }
    } else {
        if (!parsed->has_offset) {
            tzinfo = Py_BuildValue("");
        } else {
            tzinfo = new_fixed_offset(parsed->offset);
        }

        obj = PyDateTimeAPI->DateTime_FromDateAndTime(
            parsed->year,
            parsed->month,
            parsed->day,
            parsed->hour,
            parsed->minute,
            parsed->second,
            parsed->microsecond,
            tzinfo,
            PyDateTimeAPI->DateTimeType
        );

        Py_DECREF(tzinfo);
    }

    free(parsed);

    return obj;
}

// Calculate a precise difference between two datetimes.
PyObject* precise_diff(PyObject *self, PyObject *args) {
    PyObject* dt1;
    PyObject* dt2;

    if (!PyArg_ParseTuple(args, "OO", &dt1, &dt2)) {
        PyErr_SetString(
            PyExc_ValueError, "Invalid parameters"
        );
        return NULL;
    }

    int year_diff = 0;
    int month_diff = 0;
    int day_diff = 0;
    int hour_diff = 0;
    int minute_diff = 0;
    int second_diff = 0;
    int microsecond_diff = 0;
    int sign = 1;
    int year;
    int month;
    int leap;
    int days_in_last_month;
    int days_in_month;
    int dt1_year = PyDateTime_GET_YEAR(dt1);
    int dt2_year = PyDateTime_GET_YEAR(dt2);
    int dt1_month = PyDateTime_GET_MONTH(dt1);
    int dt2_month = PyDateTime_GET_MONTH(dt2);
    int dt1_day = PyDateTime_GET_DAY(dt1);
    int dt2_day = PyDateTime_GET_DAY(dt2);
    int dt1_hour = 0;
    int dt2_hour = 0;
    int dt1_minute = 0;
    int dt2_minute = 0;
    int dt1_second = 0;
    int dt2_second = 0;
    int dt1_microsecond = 0;
    int dt2_microsecond = 0;
    int dt1_total_seconds = 0;
    int dt2_total_seconds = 0;
    int dt1_offset = 0;
    int dt2_offset = 0;
    int dt1_is_datetime = PyDateTime_Check(dt1);
    int dt2_is_datetime = PyDateTime_Check(dt2);
    PyObject *offset;
    PyObject *tzinfo;

    // If we have datetimes (and not only dates) we get the information
    // we need
    if (dt1_is_datetime) {
        // Retrieving offset, if any
        if (((_PyDateTime_BaseTZInfo *)(dt1))->hastzinfo) {
            tzinfo = ((PyDateTime_DateTime *)(dt1))->tzinfo;
            if (tzinfo != Py_None) {
                offset = PyObject_CallMethod(tzinfo, "utcoffset", "O", dt1);
                dt1_offset = PyDateTime_DELTA_GET_SECONDS(offset);
            }
        }

        dt1_hour = PyDateTime_DATE_GET_HOUR(dt1);
        dt1_minute = PyDateTime_DATE_GET_MINUTE(dt1);
        dt1_second = PyDateTime_DATE_GET_SECOND(dt1);
        dt1_microsecond = PyDateTime_DATE_GET_MICROSECOND(dt1);

        // Adjusting if offset
        if (dt1_offset) {
            dt1_hour -= dt1_offset / SECS_PER_HOUR;
            dt1_offset %= SECS_PER_HOUR;
            dt1_minute -= dt1_offset / SECS_PER_MIN;
            dt1_offset %= SECS_PER_MIN;
            dt1_second -= dt1_offset;

            if (dt1_second < 0) {
                dt1_second += 60;
                dt1_minute -= 1;
            } else if (dt1_second > 60) {
                dt1_second -= 60;
                dt1_minute += 1;
            }

            if (dt1_minute < 0) {
                dt1_minute += 60;
                dt1_hour -= 1;
            } else if (dt1_minute > 60) {
                dt1_minute -= 60;
                dt1_hour += 1;
            }

            if (dt1_hour < 0) {
                dt1_hour += 24;
                dt1_day -= 1;
            } else if (dt1_hour > 24) {
                dt1_hour -= 24;
                dt1_day += 1;
            }
        }
        
        dt1_total_seconds = (
            dt1_hour * SECS_PER_HOUR
            + dt1_minute * SECS_PER_MIN
            + dt1_second
        );
    }

    if (dt2_is_datetime) {
        if (((_PyDateTime_BaseTZInfo *)(dt2))->hastzinfo) {
            tzinfo = ((PyDateTime_DateTime *)(dt2))->tzinfo;
            if (tzinfo != Py_None) {
                offset = PyObject_CallMethod(tzinfo, "utcoffset", "O", dt2);
                dt2_offset = PyDateTime_DELTA_GET_SECONDS(offset);
            }
        }

        dt2_hour = PyDateTime_DATE_GET_HOUR(dt2);
        dt2_minute = PyDateTime_DATE_GET_MINUTE(dt2);
        dt2_second = PyDateTime_DATE_GET_SECOND(dt2);
        dt2_microsecond = PyDateTime_DATE_GET_MICROSECOND(dt2);

        // Adjusting if offset
        if (dt2_offset) {
            dt2_hour -= dt2_offset / SECS_PER_HOUR;
            dt2_offset %= SECS_PER_HOUR;
            dt2_minute -= dt2_offset / SECS_PER_MIN;
            dt2_offset %= SECS_PER_MIN;
            dt2_second -= dt2_offset;

            if (dt2_second < 0) {
                dt2_second += 60;
                dt2_minute -= 1;
            } else if (dt2_second > 60) {
                dt2_second -= 60;
                dt2_minute += 1;
            }

            if (dt2_minute < 0) {
                dt2_minute += 60;
                dt2_hour -= 1;
            } else if (dt2_minute > 60) {
                dt2_minute -= 60;
                dt2_hour += 1;
            }

            if (dt2_hour < 0) {
                dt2_hour += 24;
                dt2_day -= 1;
            } else if (dt2_hour > 24) {
                dt2_hour -= 24;
                dt2_day += 1;
            }
        }

        dt2_total_seconds = (
            dt2_hour * SECS_PER_HOUR
            + dt2_minute * SECS_PER_MIN
            + dt2_second
        );
    }

    // Direct comparison between two datetimes does not work
    // so we need to check by properties
    int dt1_gt_dt2 = (
        dt1_year > dt2_year
        || (dt1_year == dt2_year && dt1_month > dt2_month)
        || (
            dt1_year == dt2_year
            && dt1_month == dt2_month
            && dt1_day > dt2_day
        )
        || (
            dt1_year == dt2_year
            && dt1_month == dt2_month
            && dt1_day == dt2_day
            && dt1_total_seconds > dt2_total_seconds
        )
        || (
            dt1_year == dt2_year
            && dt1_month == dt2_month
            && dt1_day == dt2_day
            && dt1_total_seconds == dt2_total_seconds
            && dt1_microsecond > dt2_microsecond
        )
    );

    if (dt1_gt_dt2) {
        PyObject* temp;   
        temp = dt1;
        dt1 = dt2;
        dt2 = temp;
        sign = -1;

        // Retrieving properties
        dt1_year = PyDateTime_GET_YEAR(dt1);
        dt2_year = PyDateTime_GET_YEAR(dt2);
        dt1_month = PyDateTime_GET_MONTH(dt1);
        dt2_month = PyDateTime_GET_MONTH(dt2);
        dt1_day = PyDateTime_GET_DAY(dt1);
        dt2_day = PyDateTime_GET_DAY(dt2);

        if (dt2_is_datetime) {
            dt1_hour = PyDateTime_DATE_GET_HOUR(dt1);
            dt1_minute = PyDateTime_DATE_GET_MINUTE(dt1);
            dt1_second = PyDateTime_DATE_GET_SECOND(dt1);
            dt1_microsecond = PyDateTime_DATE_GET_MICROSECOND(dt1);
        }

        if (dt1_is_datetime) {
            dt2_hour = PyDateTime_DATE_GET_HOUR(dt2);
            dt2_minute = PyDateTime_DATE_GET_MINUTE(dt2);
            dt2_second = PyDateTime_DATE_GET_SECOND(dt2);
            dt2_microsecond = PyDateTime_DATE_GET_MICROSECOND(dt2);
        }
    }

    year_diff = dt2_year - dt1_year;
    month_diff = dt2_month - dt1_month;
    day_diff = dt2_day - dt1_day;
    hour_diff = dt2_hour - dt1_hour;
    minute_diff = dt2_minute - dt1_minute;
    second_diff = dt2_second - dt1_second;
    microsecond_diff = dt2_microsecond - dt1_microsecond;

    if (microsecond_diff < 0) {
        microsecond_diff += 1e6;
        second_diff -= 1;
    }

    if (second_diff < 0) {
        second_diff += 60;
        minute_diff -= 1;
    }

    if (minute_diff < 0) {
        minute_diff += 60;
        hour_diff -= 1;
    }

    if (hour_diff < 0) {
        hour_diff += 24;
        day_diff -= 1;
    }

    if (day_diff < 0) {
        // If we have a difference in days,
        // we have to check if they represent months
        year = dt2_year;
        month = dt2_month;

        if (month == 1) {
            month = 12;
            year -= 1;
        } else {
            month -= 1;
        }

        leap = is_leap(year);

        days_in_last_month = DAYS_PER_MONTHS[leap][month];
        days_in_month = DAYS_PER_MONTHS[is_leap(dt2_year)][dt2_month];

        if (day_diff < days_in_month - days_in_last_month) {
            // We don't have a full month, we calculate days
            if (days_in_last_month < dt1_day) {
                day_diff += dt1_day;
            } else {
                day_diff += days_in_last_month;
            }
        } else if (day_diff == days_in_month - days_in_last_month) {
            // We have exactly a full month
            // We remove the days difference
            // and add one to the months difference
            day_diff = 0;
            month_diff += 1;
        } else {
            // We have a full month
            day_diff += days_in_last_month;
        }

        month_diff -= 1;
    }

    if (month_diff < 0) {
        month_diff += 12;
        year_diff -= 1;
    }

    return new_diff(
        year_diff * sign,
        month_diff * sign,
        day_diff * sign,
        hour_diff * sign,
        minute_diff * sign,
        second_diff * sign,
        microsecond_diff * sign
    );
}

/* ------------------------------------------------------------------------- */

static PyMethodDef helpers_methods[] = {
    {
        "local_time",
        (PyCFunction) local_time,
        METH_VARARGS,
        PyDoc_STR("Returns a UNIX time as a broken down time for a particular transition type.")
    },
    {
        "parse_iso8601",
        (PyCFunction) parse_iso8601,
        METH_VARARGS,
        PyDoc_STR("Parses a ISO8601 string into a tuple.")
    },
    {
        "precise_diff",
        (PyCFunction) precise_diff,
        METH_VARARGS,
        PyDoc_STR("Calculate a precise difference between two datetimes.")
    },
    {NULL}
};

/* ------------------------------------------------------------------------- */

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "_helpers",
    NULL,
    -1,
    helpers_methods,
    NULL,
    NULL,
    NULL,
    NULL,
};

PyMODINIT_FUNC
PyInit__helpers(void)
{
    PyObject *module;

    PyDateTime_IMPORT;

    module = PyModule_Create(&moduledef);

    if (module == NULL)
        return NULL;

    // FixedOffset declaration
    FixedOffset_type.tp_new = PyType_GenericNew;
    FixedOffset_type.tp_base = PyDateTimeAPI->TZInfoType;
    FixedOffset_type.tp_methods = FixedOffset_methods;
    FixedOffset_type.tp_members = FixedOffset_members;
    FixedOffset_type.tp_init = (initproc)FixedOffset_init;

    if (PyType_Ready(&FixedOffset_type) < 0)
        return NULL;

    // Diff declaration
    Diff_type.tp_new = PyType_GenericNew;
    Diff_type.tp_members = Diff_members;
    Diff_type.tp_init = (initproc)Diff_init;

    if (PyType_Ready(&Diff_type) < 0)
        return NULL;

    Py_INCREF(&FixedOffset_type);
    Py_INCREF(&Diff_type);

    PyModule_AddObject(module, "TZFixedOffset", (PyObject *)&FixedOffset_type);
    PyModule_AddObject(module, "PreciseDiff", (PyObject *)&Diff_type);

    return module;
}
#endif
