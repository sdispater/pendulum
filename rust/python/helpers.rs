use pyo3::prelude::*;

use crate::helpers;

#[pyfunction]
pub fn is_leap(year: u32) -> PyResult<bool> {
    Ok(helpers::is_leap(year))
}

#[pyfunction]
pub fn is_long_year(year: u32) -> PyResult<bool> {
    Ok(helpers::is_long_year(year))
}

#[pyfunction]
pub fn week_day(year: u32, month: u32, day: u32) -> PyResult<u32> {
    Ok(helpers::week_day(year, month, day))
}

#[pyfunction]
pub fn local_time(
    unix_time: isize,
    utc_offset: isize,
    microsecond: usize,
) -> PyResult<(usize, usize, usize, usize, usize, usize, usize)> {
    Ok(helpers::local_time(unix_time, utc_offset, microsecond))
}
