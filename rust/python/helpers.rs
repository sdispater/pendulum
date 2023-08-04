use std::cmp::Ordering;

use pyo3::{
    intern,
    prelude::*,
    types::{PyDate, PyDateAccess, PyDateTime, PyDelta, PyDeltaAccess, PyString, PyTimeAccess},
    PyTypeInfo,
};

use crate::{
    constants::{DAYS_PER_MONTHS, SECS_PER_DAY, SECS_PER_HOUR, SECS_PER_MIN},
    helpers,
};

use crate::python::types::PreciseDiff;

struct DateTimeInfo<'py> {
    pub year: i32,
    pub month: i32,
    pub day: i32,
    pub hour: i32,
    pub minute: i32,
    pub second: i32,
    pub microsecond: i32,
    pub total_seconds: i32,
    pub offset: i32,
    pub tz: &'py str,
    pub is_datetime: bool,
}

impl PartialEq for DateTimeInfo<'_> {
    fn eq(&self, other: &Self) -> bool {
        (
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
        )
            .eq(&(
                other.year,
                other.month,
                other.day,
                other.hour,
                other.minute,
                other.second,
                other.microsecond,
            ))
    }
}

impl PartialOrd for DateTimeInfo<'_> {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        (
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second,
            self.microsecond,
        )
            .partial_cmp(&(
                other.year,
                other.month,
                other.day,
                other.hour,
                other.minute,
                other.second,
                other.microsecond,
            ))
    }
}

pub fn get_tz_name<'py>(py: Python, dt: &'py PyAny) -> PyResult<&'py str> {
    let tz: &str = "";

    if !PyDateTime::is_type_of(dt) {
        return Ok(tz);
    }

    let tzinfo = dt.getattr("tzinfo");

    match tzinfo {
        Err(_) => Ok(tz),
        Ok(tzinfo) => {
            if tzinfo.is_none() {
                return Ok(tz);
            }
            if tzinfo.hasattr(intern!(py, "key")).unwrap_or(false) {
                // zoneinfo timezone
                let tzname: &PyString = tzinfo
                    .getattr(intern!(py, "key"))
                    .unwrap()
                    .downcast()
                    .unwrap();

                return tzname.to_str();
            } else if tzinfo.hasattr(intern!(py, "name")).unwrap_or(false) {
                // Pendulum timezone
                let tzname: &PyString = tzinfo
                    .getattr(intern!(py, "name"))
                    .unwrap()
                    .downcast()
                    .unwrap();

                return tzname.to_str();
            } else if tzinfo.hasattr(intern!(py, "zone")).unwrap_or(false) {
                // pytz timezone
                let tzname: &PyString = tzinfo
                    .getattr(intern!(py, "zone"))
                    .unwrap()
                    .downcast()
                    .unwrap();

                return tzname.to_str();
            }

            Ok(tz)
        }
    }
}

pub fn get_offset(dt: &PyAny) -> PyResult<i32> {
    if !PyDateTime::is_type_of(dt) {
        return Ok(0);
    }

    let tzinfo = dt.getattr("tzinfo")?;

    if tzinfo.is_none() {
        return Ok(0);
    }

    let offset: &PyDelta = tzinfo.call_method1("utcoffset", (dt,))?.downcast()?;

    Ok(offset.get_days() * SECS_PER_DAY as i32 + offset.get_seconds())
}

#[pyfunction]
pub fn is_leap(year: i32) -> PyResult<bool> {
    Ok(helpers::is_leap(year))
}

#[pyfunction]
pub fn is_long_year(year: i32) -> PyResult<bool> {
    Ok(helpers::is_long_year(year))
}

#[pyfunction]
pub fn week_day(year: i32, month: u32, day: u32) -> PyResult<u32> {
    Ok(helpers::week_day(year, month, day))
}

#[pyfunction]
pub fn days_in_year(year: i32) -> PyResult<u32> {
    Ok(helpers::days_in_year(year))
}

#[pyfunction]
pub fn local_time(
    unix_time: f64,
    utc_offset: isize,
    microsecond: usize,
) -> PyResult<(usize, usize, usize, usize, usize, usize, usize)> {
    Ok(helpers::local_time(unix_time, utc_offset, microsecond))
}

#[pyfunction]
pub fn precise_diff<'py>(py: Python, dt1: &'py PyAny, dt2: &'py PyAny) -> PyResult<PreciseDiff> {
    let mut sign = 1;
    let mut dtinfo1 = DateTimeInfo {
        year: dt1.downcast::<PyDate>()?.get_year(),
        month: i32::from(dt1.downcast::<PyDate>()?.get_month()),
        day: i32::from(dt1.downcast::<PyDate>()?.get_day()),
        hour: 0,
        minute: 0,
        second: 0,
        microsecond: 0,
        total_seconds: 0,
        tz: get_tz_name(py, dt1)?,
        offset: get_offset(dt1)?,
        is_datetime: PyDateTime::is_type_of(dt1),
    };
    let mut dtinfo2 = DateTimeInfo {
        year: dt2.downcast::<PyDate>()?.get_year(),
        month: i32::from(dt2.downcast::<PyDate>()?.get_month()),
        day: i32::from(dt2.downcast::<PyDate>()?.get_day()),
        hour: 0,
        minute: 0,
        second: 0,
        microsecond: 0,
        total_seconds: 0,
        tz: get_tz_name(py, dt2)?,
        offset: get_offset(dt2)?,
        is_datetime: PyDateTime::is_type_of(dt2),
    };
    let in_same_tz: bool = dtinfo1.tz == dtinfo2.tz && !dtinfo1.tz.is_empty();
    let mut total_days = helpers::day_number(dtinfo2.year, dtinfo2.month as u8, dtinfo2.day as u8)
        - helpers::day_number(dtinfo1.year, dtinfo1.month as u8, dtinfo1.day as u8);

    if dtinfo1.is_datetime {
        let dt1dt: &PyDateTime = dt1.downcast()?;

        dtinfo1.hour = i32::from(dt1dt.get_hour());
        dtinfo1.minute = i32::from(dt1dt.get_minute());
        dtinfo1.second = i32::from(dt1dt.get_second());
        dtinfo1.microsecond = dt1dt.get_microsecond() as i32;

        if !in_same_tz && dtinfo1.offset != 0 || total_days == 0 {
            dtinfo1.hour -= dtinfo1.offset / SECS_PER_HOUR as i32;
            dtinfo1.offset %= SECS_PER_HOUR as i32;
            dtinfo1.minute -= dtinfo1.offset / SECS_PER_MIN as i32;
            dtinfo1.offset %= SECS_PER_MIN as i32;
            dtinfo1.second -= dtinfo1.offset;

            if dtinfo1.second < 0 {
                dtinfo1.second += 60;
                dtinfo1.minute -= 1;
            } else if dtinfo1.second > 60 {
                dtinfo1.second -= 60;
                dtinfo1.minute += 1;
            }

            if dtinfo1.minute < 0 {
                dtinfo1.minute += 60;
                dtinfo1.hour -= 1;
            } else if dtinfo1.minute > 60 {
                dtinfo1.minute -= 60;
                dtinfo1.hour += 1;
            }

            if dtinfo1.hour < 0 {
                dtinfo1.hour += 24;
                dtinfo1.day -= 1;
            } else if dtinfo1.hour > 24 {
                dtinfo1.hour -= 24;
                dtinfo1.day += 1;
            }
        }

        dtinfo1.total_seconds = dtinfo1.hour * SECS_PER_HOUR as i32
            + dtinfo1.minute * SECS_PER_MIN as i32
            + dtinfo1.second;
    }

    if dtinfo2.is_datetime {
        let dt2dt: &PyDateTime = dt2.downcast()?;

        dtinfo2.hour = i32::from(dt2dt.get_hour());
        dtinfo2.minute = i32::from(dt2dt.get_minute());
        dtinfo2.second = i32::from(dt2dt.get_second());
        dtinfo2.microsecond = dt2dt.get_microsecond() as i32;

        if !in_same_tz && dtinfo2.offset != 0 || total_days == 0 {
            dtinfo2.hour -= dtinfo2.offset / SECS_PER_HOUR as i32;
            dtinfo2.offset %= SECS_PER_HOUR as i32;
            dtinfo2.minute -= dtinfo2.offset / SECS_PER_MIN as i32;
            dtinfo2.offset %= SECS_PER_MIN as i32;
            dtinfo2.second -= dtinfo2.offset;

            if dtinfo2.second < 0 {
                dtinfo2.second += 60;
                dtinfo2.minute -= 1;
            } else if dtinfo2.second > 60 {
                dtinfo2.second -= 60;
                dtinfo2.minute += 1;
            }

            if dtinfo2.minute < 0 {
                dtinfo2.minute += 60;
                dtinfo2.hour -= 1;
            } else if dtinfo2.minute > 60 {
                dtinfo2.minute -= 60;
                dtinfo2.hour += 1;
            }

            if dtinfo2.hour < 0 {
                dtinfo2.hour += 24;
                dtinfo2.day -= 1;
            } else if dtinfo2.hour > 24 {
                dtinfo2.hour -= 24;
                dtinfo2.day += 1;
            }
        }

        dtinfo2.total_seconds = dtinfo2.hour * SECS_PER_HOUR as i32
            + dtinfo2.minute * SECS_PER_MIN as i32
            + dtinfo2.second;
    }

    if dtinfo1 > dtinfo2 {
        sign = -1;
        (dtinfo1, dtinfo2) = (dtinfo2, dtinfo1);

        total_days = -total_days;
    }

    let mut year_diff = dtinfo2.year - dtinfo1.year;
    let mut month_diff = dtinfo2.month - dtinfo1.month;
    let mut day_diff = dtinfo2.day - dtinfo1.day;
    let mut hour_diff = dtinfo2.hour - dtinfo1.hour;
    let mut minute_diff = dtinfo2.minute - dtinfo1.minute;
    let mut second_diff = dtinfo2.second - dtinfo1.second;
    let mut microsecond_diff = dtinfo2.microsecond - dtinfo1.microsecond;

    if microsecond_diff < 0 {
        microsecond_diff += 1_000_000;
        second_diff -= 1;
    }

    if second_diff < 0 {
        second_diff += 60;
        minute_diff -= 1;
    }

    if minute_diff < 0 {
        minute_diff += 60;
        hour_diff -= 1;
    }

    if hour_diff < 0 {
        hour_diff += 24;
        day_diff -= 1;
    }

    if day_diff < 0 {
        // If we have a difference in days,
        // we have to check if they represent months
        let mut year = dtinfo2.year;
        let mut month = dtinfo2.month;

        if month == 1 {
            month = 12;
            year -= 1;
        } else {
            month -= 1;
        }

        let leap = helpers::is_leap(year);

        let days_in_last_month = DAYS_PER_MONTHS[usize::from(leap)][month as usize];
        let days_in_month =
            DAYS_PER_MONTHS[usize::from(helpers::is_leap(dtinfo2.year))][dtinfo2.month as usize];

        match day_diff.cmp(&(days_in_month - days_in_last_month)) {
            Ordering::Less => {
                // We don't have a full month, we calculate days
                if days_in_last_month < dtinfo1.day {
                    day_diff += dtinfo1.day;
                } else {
                    day_diff += days_in_last_month;
                }
            }
            Ordering::Equal => {
                // We have exactly a full month
                // We remove the days difference
                // and add one to the months difference
                day_diff = 0;
                month_diff += 1;
            }
            Ordering::Greater => {
                // We have a full month
                day_diff += days_in_last_month;
            }
        }

        month_diff -= 1;
    }

    if month_diff < 0 {
        month_diff += 12;
        year_diff -= 1;
    }

    Ok(PreciseDiff {
        years: year_diff * sign,
        months: month_diff * sign,
        days: day_diff * sign,
        hours: hour_diff * sign,
        minutes: minute_diff * sign,
        seconds: second_diff * sign,
        microseconds: microsecond_diff * sign,
        total_days: total_days * sign,
    })
}
