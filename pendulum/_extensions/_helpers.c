/* ------------------------------------------------------------------------- */

#include <Python.h>
#include <stdint.h>
#include <datetime.h>

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

PyObject* local_time(PyObject *self, PyObject *args) {
    double unix_time;
    int32_t utc_offset;
    int32_t year;
    int64_t microsecond;
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

    if (!PyArg_ParseTuple(args, "di", &unix_time, &utc_offset)) {
        PyErr_SetString(
            PyExc_ValueError, "Invalid parameters"
        );
        return NULL;
    }

    year = EPOCH_YEAR;
    microsecond = (int64_t) (unix_time * 1000000) % 1000000;
    if (microsecond < 0) {
        microsecond += 1000000;
    }
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

    // Handle hours, minutes, seconds and microseconds
    hour = seconds / SECS_PER_HOUR;
    seconds %= SECS_PER_HOUR;
    minute = seconds / SECS_PER_MIN;
    second = seconds % SECS_PER_MIN;

    return PyTuple_Pack(
        7,
        PyLong_FromLong(year),
        PyLong_FromLong(month),
        PyLong_FromLong(day),
        PyLong_FromLong(hour),
        PyLong_FromLong(minute),
        PyLong_FromLong(second),
        PyLong_FromLong(microsecond)
    );
}

/* ------------------------------------------------------------------------- */

static PyMethodDef localtime_methods[] = {
    {
        "local_time",
        (PyCFunction) local_time,
        METH_VARARGS,
        PyDoc_STR("Returns a UNIX time as a broken down time for a particular transition type.")
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
    localtime_methods,
    NULL,
    NULL,
    NULL,
    NULL,
};
#endif

static PyObject *
moduleinit(void)
{
    PyObject *module;

#if PY_MAJOR_VERSION >= 3
    module = PyModule_Create(&moduledef);
#else
    module = Py_InitModule3("_helpers", localtime_methods, NULL);
#endif

    if (module == NULL)
        return NULL;

    return module;
}

#if PY_MAJOR_VERSION < 3
PyMODINIT_FUNC init_helpers(void)
{
    moduleinit();
}
#else
PyMODINIT_FUNC PyInit__helpers(void)
{
    return moduleinit();
}
#endif
