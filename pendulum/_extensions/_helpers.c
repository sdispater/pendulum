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

#if PY_MAJOR_VERSION < 3
    #define PyLong_FromLong PyInt_FromLong
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

#if PY_MAJOR_VERSION >= 3
    return PyUnicode_FromString(tzname);
#else
    return PyString_FromString(tzname);
#endif
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

#if PY_MAJOR_VERSION >= 3
static PyTypeObject FixedOffset_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "rfc3339.FixedOffset_type",             /* tp_name */
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
#else
static PyTypeObject FixedOffset_type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "_helpers.FixedOffset_type", /*tp_name*/
    sizeof(FixedOffset),       /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    0,                         /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    (reprfunc)FixedOffset_repr,/*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    (reprfunc)FixedOffset_repr,/*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT |
    Py_TPFLAGS_BASETYPE,       /*tp_flags*/
    "TZInfo with fixed offset",/* tp_doc */
};
#endif

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


PyObject* parse_iso8601(PyObject *self, PyObject *args) {
    char* str;
    char* c;
    PyObject *obj;
    PyObject *tzinfo;

    // day_first is only here for compatibility
    // It will be removed in the next major version
    // since it's not ISO 8601 compliant.
    int day_first;

    int year = 0;
    int month = 1;
    int day = 1;
    int hour = 0;
    int minute = 0;
    int second = 0;
    int subsecond = 0;
    int monthday = 0;
    int week = 0;
    int weekday = 1;
    int ordinal;
    int tz_sign = 0;
    int offset = 0;
    int leap = 0;
    int ambiguous_date = 0;
    int separators = 0;
    int time = 0;
    int has_time = 0;
    int has_hour = 0;
    int has_offset = 0;
    int i;
    int j;

    if (!PyArg_ParseTuple(args, "si", &str, &day_first)) {
        PyErr_SetString(
            PyExc_ValueError, "Invalid parameters"
        );
        return NULL;
    }

    c = str;

    // Year
    for (i = 0; i < 4; i++) {
        if (*c >= '0' && *c <= '9') {
            year = 10 * year + *c++ - '0';
        } else {
            PyErr_SetString(
                PyExc_ValueError, "Invalid ISO8601 string"
            );

            return NULL;
        }
    }

    leap = is_leap(year);

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
                    PyErr_SetString(
                        PyExc_ValueError, "Invalid week date"
                    );

                    return NULL;
                }

                weekday = week % 10;
                week /= 10;

                break;
            default:
                // Any other case is wrong
                PyErr_SetString(
                    PyExc_ValueError, "Invalid week date"
                );

                return NULL;
        }

        // Checks
        if (week > 53) {
            PyErr_SetString(
                PyExc_ValueError, "Invalid week number"
            );

            return NULL;
        }

        if (weekday > 7) {
            PyErr_SetString(
                PyExc_ValueError, "Invalid weekday number"
            );

            return NULL;
        }

        // Calculating ordinal day
        ordinal = week * 7 + weekday - (week_day(year, 1, 4) + 3);

        if (ordinal < 1) {
            // Previous year
            ordinal += days_in_year(year - 1);
            year -= 1;
            leap = is_leap(year);
        }

        if (ordinal > days_in_year(year)) {
            // Next year
            ordinal -= days_in_year(year);
            year += 1;
            leap = is_leap(year);
        }

        for (j = 1; j < 14; j++) {
            if (ordinal <= MONTHS_OFFSETS[leap][j]) {
                day = ordinal - MONTHS_OFFSETS[leap][j - 1];
                month = j - 1;

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
                PyErr_SetString(
                    PyExc_ValueError, "Invalid date"
                );

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
                    ambiguous_date = 1;
                }

                month = monthday;
                break;
            case 3:
                // Ordinal day
                if (separators > 1) {
                    PyErr_SetString(
                        PyExc_ValueError, "Invalid date"
                    );

                    return NULL;
                }

                if (monthday < 1 || monthday > MONTHS_OFFSETS[leap][13]) {
                    PyErr_SetString(
                        PyExc_ValueError, "Invalid ordinal day for year"
                    );

                    return NULL;
                }

                for (j = 1; j < 14; j++) {
                    if (monthday <= MONTHS_OFFSETS[leap][j]) {
                        day = monthday - MONTHS_OFFSETS[leap][j - 1];
                        month = j - 1;

                        break;
                    }
                }

                break;
            case 4:
                // Month and day
                if (day_first) {
                    month = monthday % 100;
                    day = monthday / 100;
                } else {
                    month = monthday / 100;
                    day = monthday % 100;
                }
                break;
            default:
                PyErr_SetString(
                    PyExc_ValueError, "Invalid month and/or day"
                );

                return NULL;
        }
    }

    // Checks
    if (separators && !monthday && !week) {
        PyErr_SetString(
            PyExc_ValueError, "Invalid date"
        );

        return NULL;
    }

    if (month > 12) {
        PyErr_SetString(
            PyExc_ValueError, "Invalid month"
        );

        return NULL;
    }

    if (day > DAYS_PER_MONTHS[leap][month]) {
        PyErr_SetString(
            PyExc_ValueError, "Day is invalid for month"
        );

        return NULL;
    }

    separators = 0;
    if (*c == 'T' || *c == ' ') {
        if (ambiguous_date) {
            PyErr_SetString(
                PyExc_ValueError, "Invalid date"
            );

            return NULL;
        }

        has_time = 1;
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
                PyErr_SetString(
                    PyExc_ValueError, "Invalid time"
                );

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
                    PyErr_SetString(
                        PyExc_ValueError, "Invalid time"
                    );

                    return NULL;
                }

                hour = time;
                has_hour = 1;
                break;
            case 4:
                // Hours and minutes
                if (separators > 1) {
                    // Extraneous separators
                    PyErr_SetString(
                        PyExc_ValueError, "Invalid time"
                    );

                    return NULL;
                }

                hour = time / 100;
                minute = time % 100;
                has_hour = 1;
                break;
            case 6:
                // Hours, minutes and seconds
                if (!(separators == 0 || separators == 2)) {
                    // We should have either two separators or none
                    PyErr_SetString(
                        PyExc_ValueError, "Invalid time"
                    );

                    return NULL;
                }
                hour = time / 10000;
                minute = time / 100 % 100;
                second = time % 100;
                has_hour = 1;
                break;
            default:
                // Any other case is wrong
                PyErr_SetString(
                    PyExc_ValueError, "Invalid time"
                );

                return NULL;
        }

        // Checks
        if (hour > 23) {
            PyErr_SetString(
                PyExc_ValueError, "Invalid hour"
            );

            return NULL;
        }

        if (minute > 59) {
            PyErr_SetString(
                PyExc_ValueError, "Invalid minute"
            );

            return NULL;
        }

        if (second > 59) {
            PyErr_SetString(
                PyExc_ValueError, "Invalid second"
            );

            return NULL;
        }

        // Subsecond
        if (*c == '.' || *c == ',') {
            c++;

            time = 0;
            i = 0;
            while (*c != '\0' && *c != 'Z' && *c != '+' && *c != '-') {
                if (!(*c >= '0' && *c <='9')) {
                    PyErr_SetString(
                        PyExc_ValueError, "Invalid subsecond"
                    );
                    return NULL;
                }

                time = 10 * time + *c++ - '0';
                i++;
            }

            if (i > 9) {
                subsecond = time / 1e9;
            } else if (i <= 9) {
                subsecond = time * pow(10, 9 - i);
            }
        }

        // Timezone
        if (*c == 'Z') {
            has_offset = 1;
            c++;
        } else if (*c == '+' || *c == '-') {
            tz_sign = 1;
            if (*c == '-') {
                tz_sign = -1;
            }

            has_offset = 1;
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
                    PyErr_SetString(
                        PyExc_ValueError, "Invalid timezone offset"
                    );
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
                        PyErr_SetString(
                            PyExc_ValueError, "Invalid timezone offset"
                        );
                        return NULL;
                    }

                    offset = tz_sign * (time * 3600);
                    break;
                case 4:
                    // hhmm Format
                    if (separators > 1) {
                        // Extraneous separators
                        PyErr_SetString(
                            PyExc_ValueError, "Invalid timezone offset"
                        );
                        return NULL;
                    }

                    offset = tz_sign * ((time / 100 * 3600) + (time % 100 * 60));
                    break;
                default:
                    // Wrong format
                    PyErr_SetString(
                        PyExc_ValueError, "Invalid timezone offset"
                    );
                    return NULL;
            }
        }
    }

    if (!has_time) {
        // Date only
        if (ambiguous_date) {
            // We can "safely" assume that the ambiguous
            // date was actually a time in the form hhmmss
            hour = year / 100;
            minute = year % 100;
            second = month;

            obj = PyDateTimeAPI->Time_FromTime(
                hour, minute, second, subsecond / 1000,
                Py_BuildValue(""),
                PyDateTimeAPI->TimeType
            );
        } else {
            obj = PyDateTimeAPI->Date_FromDate(
                year, month, day,
                PyDateTimeAPI->DateType
            );
        }
    } else {
        if (!has_offset) {
            tzinfo = Py_BuildValue("");
        } else {
            tzinfo = new_fixed_offset(offset);
        }

        obj = PyDateTimeAPI->DateTime_FromDateAndTime(
            year,
            month,
            day,
            hour,
            minute,
            second,
            subsecond / 1000,
            tzinfo,
            PyDateTimeAPI->DateTimeType
        );

        Py_DECREF(tzinfo);
    }

    return obj;
}

PyObject* parse(PyObject *self, PyObject *args) {
    char* str;
    char* c;
    int day_first;
    int separators = 0;
    PyObject *obj;

    if (!PyArg_ParseTuple(args, "si", &str, &day_first)) {
        PyErr_SetString(
            PyExc_ValueError, "Invalid parameters"
        );
        return NULL;
    }

    c = str;
    c++;
    separators++;

    obj = PyDateTimeAPI->Date_FromDate(
                2017, 3, 21,
                PyDateTimeAPI->DateType
            );

    return obj;
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
    {NULL}
};

/* ------------------------------------------------------------------------- */

#if PY_MAJOR_VERSION >= 3
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
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit__helpers(void)
#else
init_helpers(void)
#endif
{
    PyObject *module;

    PyDateTime_IMPORT;

#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&moduledef);
#else
    module = Py_InitModule3("_helpers", helpers_methods, NULL);
#endif

    if (module == NULL)
#if PY_MAJOR_VERSION >= 3
        return NULL;
#else
        return;
#endif

    FixedOffset_type.tp_new = PyType_GenericNew;
    FixedOffset_type.tp_base = PyDateTimeAPI->TZInfoType;
    FixedOffset_type.tp_methods = FixedOffset_methods;
    FixedOffset_type.tp_members = FixedOffset_members;
    FixedOffset_type.tp_init = (initproc)FixedOffset_init;

    if (PyType_Ready(&FixedOffset_type) < 0)
#if PY_MAJOR_VERSION >= 3
        return NULL;
#else
        return;
#endif

    Py_INCREF(&FixedOffset_type);

    PyModule_AddObject(module, "TZFixedOffset", (PyObject *)&FixedOffset_type);
#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
#endif
